vim.keymap.set("n", "<leader>u", vim.cmd.UndotreeToggle)
vim.cmd [[
hi UndotreeNormal guibg=NONE
]]

-- Make undotree history persistent
vim.opt.undofile = true
vim.opt.undodir = vim.fn.expand("$HOME/.local/share/nvim/undo")
vim.opt.undolevels = 1000
vim.opt.undoreload = 10000
