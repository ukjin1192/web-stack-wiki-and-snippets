" Pre-requirements
  " $ sudo apt-get install vim ctags cmake python-dev
" Install Vundle
  " $ mkdir -p ~/.vim/bundle/
  " $ cd ~/.vim/bundle/
  " $ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
" Install Plugins
  " $ vim [:PluginInstall]
" Compile YouCompleteMe
  " $ cd ~/.vim/bundle/YouCompleteMe
  " $ ./install.sh
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
  Plugin 'gmarik/Vundle.vim'                  " Manage Vundle Package
  Plugin 'Valloric/YouCompleteMe'             " Auto complete
  Plugin 'majutsushi/tagbar'                  " Check function and global variable at side bar
  Plugin 'scrooloose/nerdtree'                " Show directory tree at side bar
  Plugin 'scrooloose/syntastic'               " Check Syntax error when save (includes PEP)
  Plugin 'scrooloose/nerdcommenter'           " Annotate block (\cc) or delete block (\cu)
  Plugin 'nathanaelkane/vim-indent-guides'    " Indent Guides
  Plugin 'altercation/vim-colors-solarized'   " Color scheme
  Plugin 'bling/vim-airline'                  " Status bar
  Plugin 'kien/ctrlp.vim'                     " File finder and manage buffers
call vundle#end()
filetype plugin indent on

" Use solarized color scheme
syntax enable
set background=dark
if !has('gui_running')
  let g:solarized_termtrans=1       " Compatibility for Terminal
  if !(&t_Co >= 256 || $TERM == 'xterm-256color')
    set t_Co=16
    let g:solarized_termcolors=16   " Make Solarized use 16 colors for Terminal support
  endif
endif
colorscheme solarized

" Indent Guides
let g:indent_guides_enable_on_vim_startup=1
let g:indent_guides_start_level=2
let g:indent_guides_auto_colors=0
autocmd VimEnter,Colorscheme * :hi IndentGuidesEven ctermbg=0

" Default settings
set autoindent      " Auto indentation
set smartindent     " Smart indentation
set tabstop=2
set shiftwidth=2
set softtabstop=2
set hlsearch        " Highlight search keywords
set encoding=utf-8  " Encoding
set fileencodings=utf-8,euckr
set laststatus=2    " Show status bar always
set splitright      " Position vertically split window to right

" Filetype customization
autocmd Filetype html setlocal tabstop=2 shiftwidth=2 expandtab
autocmd Filetype ruby setlocal tabstop=2 shiftwidth=2 expandtab
autocmd Filetype javascript setlocal tabstop=2 shiftwidth=2 softtabstop=0 expandtab
autocmd Filetype python setlocal tabstop=8 shiftwidth=4 softtabstop=4 expandtab

" CtrlP ignoring list
let g:ctrlp_custom_ignore = {
  \ 'dir':  '\v[\/](\.git|node_modules|\.sass-cache|bower_components|build|_site)$',
  \ 'file': '\v\.(exe|so|dll)$'}

" Memorize cursor position
au BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\ exe "norm g`\"" |
\ endif   

" Vim Key Mapping
nmap <F1> :tabprev<CR>
nmap <F2> :tabnext<CR>
nmap <F3> gg=G<CR>
nmap <F4> :wq<CR>
nmap <F5> :!reset<CR>
nmap <F6> :TagbarToggle<CR>
nmap <F7> :set paste!<CR>
nmap <F8> :set paste<CR>
nmap <F9> :CtrlP<CR>
nmap <F10> :NERDTree<CR>
