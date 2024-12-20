vim.g.mapleader = " "

-- Netrw
vim.keymap.set("n", "<leader>er", vim.cmd.Ex)

-- Esc remaps
vim.keymap.set("i", '<A-j>', '<Esc>')
vim.keymap.set("i", '<A-k>', '<Esc>')
vim.keymap.set("v", '<A-k>', '<Esc>')
vim.keymap.set("v", '<A-j>', '<Esc>')

-- C-u and C-d center the view automatically
vim.keymap.set("n", '<C-d>', '<C-d>zz')
vim.keymap.set("n", '<C-u>', '<C-u>zz')

-- Removes highlights
vim.keymap.set("n", '<leader>n', vim.cmd.noh)

-- Move one line downwards
vim.keymap.set("n", '<C-t>', '<C-e>')

-- Save and quit
vim.keymap.set("n", '<leader>w', vim.cmd.w)
vim.keymap.set("n", '<leader>q', vim.cmd.q)

-- Paste without yanking the replaced text
vim.api.nvim_set_keymap('x', '<leader>p', '"_dP', { noremap = true, silent = true })

-- Search and replace in current visual selection
vim.keymap.set("x", "<leader>s", ":s/")

-- Yank to clipboard
vim.keymap.set('v', '<leader>y', '"+y')

-- Redo
vim.keymap.set("n", 'r', vim.cmd.red)

-- Yank to end of line
vim.keymap.set("v", 'e', '$y')
vim.keymap.set("v", '<leader>e', '$"+y')

-- Diagnostic keymaps
vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, { desc = 'Go to previous [D]iagnostic message' })
vim.keymap.set('n', ']d', vim.diagnostic.goto_next, { desc = 'Go to next [D]iagnostic message' })
vim.keymap.set('n', '<leader>e', vim.diagnostic.open_float, { desc = 'Show diagnostic [E]rror messages' })

-- Centering
vim.keymap.set('n', '<leader>fs', vim.cmd.NoNeckPain)
