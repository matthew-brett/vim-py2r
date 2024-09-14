""" Python code supporting R2Rewrite
"""

import re

import vim


def find_python_block(lines, line_i):
    """ Find, return surrounding block of Python code
    """
    # Track back in `lines` to find ```{python} marker
    i = line_i
    while i >= 0:
        line = lines[i].rstrip()
        if line == '```':  # End marker before start marker.
            return None, None, None
        if line.startswith('```{python'):  # Found start marker.
            start_i = i
            break
        if line.startswith('```{'):  # Found start marker of other code.
            return None, None, None
        i -= 1
    else:  # Never found a start marker.
        return None, None, None
    # Track forward to find ``` marker.
    for i in range(line_i + 1, len(lines)):
        line = lines[i].rstrip()
        if line.startswith('```{'):  # Found start marker of other code.
            return None, None, None
        if line.rstrip() == '```':  # End marker.
            break
    else:  # Never found an end marker.
        return None, None, None
    py_code = '\n'.join(lines[start_i + 1:i])
    return py_code, start_i, i


FOR_PRELUDE = re.compile(
        r'''
        (?P<indent>\s*)
        for\s+
        (?P<lvar>\w+)\s+
        in\s+
        range\(
        (?P<lseq>\w+)
        \):
        ''',
        flags=re.VERBOSE)


def py2r(py_code):
    out_code = re.sub(
        r'''
        np\.array\(
        [\n\t ]*
        \[
        (.*?)
        \]\)
        ''', r'c(\1)', py_code,
            flags=re.MULTILINE | re.VERBOSE
    )
    out_code = re.sub(
        r'''
        len\(
        [\n\t ]*
        (.*?)
        \)
        ''', r'length(\1)', out_code,
            flags=re.MULTILINE | re.VERBOSE
    )
    out_code = re.sub(r' = ', ' <- ', out_code, flags=re.MULTILINE)
    out_code = re.sub(r'\d+_[0-9_]+',
        lambda m : m.group().replace('_', ''),
        out_code)
    out_code = re.sub(
        r'''
        plt\.
        (\w+)
        \(
        (.*?)
        ,\s*
        bins\s*
        =\s*
        (\w+)
        (.*?)
        \)
        \n*
        plt\.title\(
        (.*?)
        \)
        \n*
        plt\.xlabel\(
        (.*?)
        \)
        ''',
        r'\1(\2, breaks=\3\4,\n     main=\5,\n     xlab=\6)', out_code,
        flags=re.VERBOSE
    )
    out_code = re.sub(
        r'''
        (\s+)\[
        (.*?)
        ]
        ''',
        r'\1c(\2)', out_code,
        flags=re.VERBOSE
    )
    out_code = re.sub(
        r'''
        print\(
        (['"])
        (.*?)
        (['"])
        ,\s*
        (.*?)\)
        ''',
        r'message(\1\2 \3, \4)', out_code,
        flags=re.VERBOSE | re.MULTILINE | re.DOTALL
    )
    out_code = re.sub(
        r'''
        print\(
        (['"])
        (.*?)
        (['"])
        \)
        ''',
        r'message(\1\2\3)', out_code,
        flags=re.VERBOSE | re.MULTILINE | re.DOTALL
    )
    out_code = re.sub(
        r'''
        rnd\.choice\(
        (.*?)\)
        ''',
        r'sample(\1, replace=TRUE)', out_code,
        flags=re.VERBOSE | re.MULTILINE | re.DOTALL
    )
    out_code = re.sub(
        r'''
        rnd\.permuted\(
        (.*?)\)
        ''',
        r'sample(\1)', out_code,
        flags=re.VERBOSE | re.MULTILINE | re.DOTALL
    )
    out_code = re.sub(r'np\.zeros', r'numeric', out_code)
    out_code = re.sub('True', 'TRUE', out_code)
    out_code = re.sub('False', 'FALSE', out_code)
    r_lines = []
    indents = []
    for line in out_code.splitlines():
        if line.startswith('import ') or line.startswith('from '):
            continue
        if 'np.random.default_rng' in line:
            continue
        m = FOR_PRELUDE.match(line)
        if m:
            gvars = m.groupdict()
            line = "{indent}for ({lvar} in 1:{lseq}) {{".format(**gvars)
            indents.append(gvars['indent'])
        elif indents:
            if not line.startswith(indents[-1] + ' '):
                indent = indents.pop()
                r_lines.append(indent + '}')
        r_lines.append(line)
    assert not indents
    out_code = '\n'.join(r_lines)
    return re.sub(r'np\.(\w+)', r'\1', out_code).strip()


def rewrite():
    row, col = vim.current.window.cursor
    buf = vim.current.buffer
    lines = buf[:]
    py_code, start_i, end_i = find_python_block(lines, row - 1)
    if py_code is None:   # No surrounding Python block.
        return
    next_i = end_i + 1
    r_code = py2r(py_code)
    r_lines = ['', '```{r}'] + r_code.splitlines() + ['```', '']
    buf[:] = buf[:next_i] + r_lines + buf[next_i:]
    vim.current.window.cursor = (next_i + 2, col)
