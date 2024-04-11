require('remap')
require('plugins')
require('colorscheme')
require('lualine-config')

vim.wo.relativenumber = true
vim.wo.number = true
vim.opt.ignorecase = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4

-- Highlight when yanking (copying) text
--  Try it with `yap` in normal mode
--  See `:help vim.highlight.on_yank()`
vim.api.nvim_create_autocmd('TextYankPost', {
  desc = 'Highlight when yanking (copying) text',
  group = vim.api.nvim_create_augroup('kickstart-highlight-yank', { clear = true }),
  callback = function()
    vim.highlight.on_yank()
  end,
})
