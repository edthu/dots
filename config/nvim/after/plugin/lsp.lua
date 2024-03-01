local lsp = require('lsp-zero').preset({})

lsp.on_attach(function(client, bufnr)
  -- see :help lsp-zero-keybindings
  -- to learn the available actions
  lsp.default_keymaps({buffer = bufnr})
end)

lsp.setup()

-- You need to setup `cmp` after lsp-zero
local cmp = require('cmp')
local cmp_action = require('lsp-zero').cmp_action()
local cmp_select = {behavior = cmp.SelectBehavior.Select}

cmp.setup({
  mapping = {
    -- `Enter` key to confirm completion
    ['<CR>'] = cmp.mapping.confirm({select = true}),

    -- Ctrl+Space to trigger completion menu
    ['<C-l'] = cmp.mapping.complete(),

    -- Navigate between snippet placeholder
    ['<C-j>'] = cmp.mapping.select_next_item(cmp_select),
    ['<C-k>'] = cmp.mapping.select_prev_item(cmp_select),
  }
})
