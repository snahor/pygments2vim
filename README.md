pygments2vim
============

Convert a pygments style to a vim colorscheme.

Usage:
```
python pygments2vim.py [ Pygments style or class to import ] [ output file ]
```

Print to stdout:

* Using a existing pygments style name:
```
python pygments2vim.py vim
```
* From class
```
python pygments2vim.py 'pygments.styles.vim.VimStyle'
```

Print to file:
```
python pygments2vim.py vim ~/.vim/colors/foo.vim
```
