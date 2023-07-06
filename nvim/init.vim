" This line makes pacman-installed global Arch Linux vim packages work.
source /usr/share/nvim/archlinux.vim

lua require ('plugins')
lua << END
require('lualine').setup()
END

colorscheme catppuccin-macchiato

set relativenumber
set nu rnu

syntax on

set ignorecase
