""" Tests for P2R

It's a bit nasty, but we pull out the python from the vim file, and test that

Run with pytest
"""

import sys
from pathlib import Path
import re
import types

THIS_DIR = Path(__file__).parent
CODE_DIR = THIS_DIR.parent
VIM_FILE = CODE_DIR / 'py2r.vim'

# Pull python code out of vim file
_all_code = VIM_FILE.read_text()
_match = re.search(r"python3 << endpython(.*)endpython", _all_code, flags=re.DOTALL)
if not _match:
    raise RuntimeError('Could not find python code in file %s' % VIM_FILE)
PY_CODE = _match.groups()[0]

# Make something that looks like the vim module
assert "vim" not in sys.modules
sys.path.insert(0, str(THIS_DIR))
import fakevim
sys.modules["vim"] = fakevim
# And something that looks like the vim_bridge module.  This only needs to give
# a null decorator.
vim_bridge = types.ModuleType('vim_bridge')
vim_bridge.bridged = lambda x : x
sys.modules['vim_bridge'] = vim_bridge

exec(PY_CODE)

def test_rewrite():
    py_code = (THIS_DIR / 'prog1.py').read_text()
    r_code = (THIS_DIR / 'prog1.R').read_text()
    assert py2r(py_code) == r_code.strip()
