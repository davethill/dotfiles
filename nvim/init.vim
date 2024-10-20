
"####################################################################
"##                         VIM AutoCMD                            ##      
"####################################################################

autocmd VimEnter * NERDTree

"####################################################################
"##                         VIM AutoCMD                            ##      
"####################################################################


"####################################################################
"##                         VIM Basics                             ##      
"####################################################################

set nocompatible            " disable compatibility to old-time vi
set showmatch               " show matching 
set ignorecase              " case insensitive 
set mouse=v                 " middle-click paste with 
set hlsearch                " highlight search 
set incsearch               " incremental search
set tabstop=4               " number of columns occupied by a tab 
set softtabstop=4           " see multiple spaces as tabstops so <BS> does the right thing
set expandtab               " converts tabs to white space
set shiftwidth=4            " width for autoindents
set autoindent              " indent a new line the same amount as the line just typed
set number                  " add line numbers
set wildmode=longest,list   " get bash-like tab completions
set cc=80                  " set an 80 column border for good coding style
filetype plugin indent on   "allow auto-indenting depending on file type
syntax on                   " syntax highlighting
set mouse=a                 " enable mouse click
set clipboard=unnamedplus   " using system clipboard
filetype plugin on
set cursorline              " highlight current cursorline
set ttyfast                 " Speed up scrolling in Vim
set encoding=utf8
" set spell                 " enable spell check (may need to download language package)
" set noswapfile            " disable creating swap file
" set backupdir=~/.cache/vim " Directory to store backup files.

"####################################################################
"##                         VIM Basics                             ##      
"####################################################################



"####################################################################
"##                         VIM Plug                               ##      
"####################################################################

call plug#begin()
 Plug 'scrooloose/nerdtree'
 Plug 'jistr/vim-nerdtree-tabs'
 Plug 'ryanoasis/vim-devicons'
 Plug 'vim-airline/vim-airline'
 Plug 'vim-airline/vim-airline-themes'
 Plug 'yegappan/grep'
 Plug 'godlygeek/csapprox'
 Plug 'Raimondi/delimitMate'
 Plug 'majutsushi/tagbar'
 Plug 'w0rp/ale'
 Plug 'Yggdroot/indentLine'
 Plug 'avelino/vim-bootstrap-updater'
 Plug 'tpope/vim-rhubarb' " required by fugitive to :Gbrowse
 Plug 'morhetz/gruvbox'
 Plug 'rust-lang/rust.vim'
 Plug 'nlknguyen/vim-docker-compose-syntax'
 Plug 'elkowar/yuck.vim'
call plug#end()

"####################################################################
"##                         VIM Plug                               ##      
"####################################################################



"####################################################################
"##                     Visual Settings                            ## 
"####################################################################

syntax on
set ruler
set number
let NERDTreeShowHidden=1
let no_buffers_menu=1
let g:airline_powerline_fonts = 1
colorscheme gruvbox
set mousemodel=popup
set t_Co=256
set guioptions=egmrti
set gfn=Monospace\ 10
set guifont=JetBrainsMono\ Nerd\ Font\ 12
"####################################################################
"##                     Visual Settings                            ## 
"####################################################################


"####################################################################
"##                     VIM KeyBindings                            ##      
"####################################################################


"####################################################################
"##                     VIM KeyBindings                            ##      
"####################################################################
