" Python to R plugin
" Language:     Python (ft=python)
" Maintainer:   Matthew Brett
" Version:      0.2
" URL:          http://github.com/mathew-brett/vim-py2r
"
" VimVersion:   Vim 7 (may work with lower Vim versions, but not tested)
"
" I got the structure of this plugin from
" http://github.com/nvie/vim-rst-tables by Vincent Driessen
" <vincent@datafox.nl>, with thanks.

" Only do this when not done yet for this buffer
if exists("g:loaded_py2r_ftplugin")
    finish
endif
let loaded_py2r_ftplugin = 1

let py_cmd_ver = 'python3'
if !has(py_cmd_ver)
    echoerr "Error: Requires Vim compiled with +python3"
    finish
endif

" Vim script filename.
" https://vi.stackexchange.com/a/7362
let s:curfile = expand('<sfile>:p')

function! P2Rewrite()

python3 << endpython
import vim
import sys
from pathlib import Path

our_pth = Path(vim.eval('s:curfile')).parent.resolve()
sys.path.insert(0, str(our_pth))

import py2r

py2r.rewrite()
endpython
endfunction

" Add mappings, unless the user didn't want this.
" The default mapping is registered, unless the user remapped it already.
if !exists("no_plugin_maps") && !exists("no_py2r_maps")
    if !hasmapto('P2Rewrite(')
        noremap <silent> <leader><leader>r :call P2Rewrite()<CR>
    endif
endif
