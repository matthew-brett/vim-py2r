""" Tests for P2R
"""

import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
CODE_DIR = THIS_DIR.parent

# Make something that looks like the vim module
assert "vim" not in sys.modules
sys.path.insert(0, str(THIS_DIR))
import fakevim
sys.modules["vim"] = fakevim
sys.path.insert(0, str(CODE_DIR))

from py2r import py2r, find_python_block

PY_PROG = (THIS_DIR / 'prog1.py').read_text().rstrip()
R_PROG = (THIS_DIR / 'prog1.R').read_text().rstrip()


def test_rewrite():
    assert py2r(PY_PROG) == R_PROG


def test_find_python_block():
    rmd_lines = (THIS_DIR / 'nb1.Rmd').read_text().splitlines()
    for i in range(0, 24):
        assert find_python_block(rmd_lines, 23) == (None, None, None)
    for i in range(24, 50):
        assert find_python_block(rmd_lines, 24) == (PY_PROG, 24, 49)
    for i in range(50, len(rmd_lines)):
        assert find_python_block(rmd_lines, 23) == (None, None, None)
    rmd_lines = """\
```{python}
a = 10
```""".splitlines()
    for i in range(len(rmd_lines)):
        assert find_python_block(rmd_lines, 0) == ('a = 10', 0, 2)
