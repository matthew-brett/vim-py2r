############
rst-sections
############

This is a small vim extension to rewrite simple Python programs in R.

It derives from https://github.com/matthew-brett/vim-rst-sections, that, in
turn, is inspired by the nice https://github.com/nvie/vim-rst-tables extension by
Vincent Driessen.

For install instructions see the ``Install`` section at the end.

************
Requirements
************

You'll need python compiled into your vim (`:version` in vim will tell you).

I've tested the Python tests with Python 3.10.

**************
Latest version
**************

Should be at https://github.com/matthew-brett/vim-py2r

*******
License
*******

I could not see a license for ``vim-rst-tables``. ``vim-py2r`` contains
some structure, but very little code, from ``vim-rst-tables``.

Assuming that that the ``vim-rst-tables`` code is in the public domain or BSD
licensed, I (Matthew Brett) release this code under the 2-clause BSD license.
The full text is in the ``LICENSE`` file in the same directory as this README.
Thanks to Vincent Driessen for sharing.

******
In use
******

Once you've installed the extension, then you can access it with your
``<leader>`` key in vim.  I believe the default is ``\``, for me it is mapped to
``,``.  You can also call the various functions directly with commands such as
``:call P2Rewrite()``.

The same function should also be accessible with the key combination
``<leader><leader>r`` ("r" for R).

*******
Install
*******

To get started, get all the code you need in some directory::

    git clone https://github.com/matthew-brett/vim-py2r
    cd vim-py2r
    git submodule update --init

Now to install.

I hope you are using vim ``pathogen``!

If you are using pathogen
=========================

* Change into your `~/.vim/bundle`` directory and::

    git clone https://github.com/matthew-brett/vim-py2r
    cd vim-py2r
    git submodule update --init --recursive

If you aren't using pathogen
============================

It's a really good idea to use pathogen, but if you aren't::

    mkdir some_directory
    cd some_directory
    git clone https://github.com/matthew-brett/vim-py2r
    cd vim-py2r
    git submodule update --init --recursive

Now copy the contents of the ``ftplugin`` directory into your
``~/.vim/ftplugin`` directory (e.g ``cp -r ftplugin/* ~/.vim/ftplugin``).

.. vim: ft=rst
