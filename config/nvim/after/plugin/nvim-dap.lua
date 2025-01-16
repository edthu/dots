-- debug adapter
local dap = require("dap")
local dapui = require("dapui")
dap.adapters.gdb = {
	type = "executable",
	command = "gdb",
	args = {"--interpreter=dap", "--eval-command", "set print pretty on"}
}

dap.adapters.codelldb = {
  type = "executable",
  command = "codelldb", -- or if not in $PATH: "/absolute/path/to/codelldb"
}

require('dapui').setup()
require("nvim-dap-virtual-text").setup()

-- connect to a debugger
---
--dap.configurations.cpp = {
--	{
--		name = "Launch",
--		type = "gdb",
--		request = "launch",
--		program = function()
--				return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/', 'file') -- ??
--		end,
--		cwd = "${workspaceFolder}",
--		stopAtBeginngingOfMainSubprogram = false,
--	}
--}
dap.configurations.cpp = {
  {
    name = "Launch file",
    type = "codelldb",
    request = "launch",
    program = function()
      return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/', 'file')
    end,
    cwd = '${workspaceFolder}',
    stopOnEntry = false,
  },
}
dap.configurations.c = dap.configurations.cpp
dap.configurations.rust = dap.configurations.cpp

-- Eval var under cursor
vim.keymap.set("n", "<space>?", function()
	require("dapui").eval(nil, { enter = true })
end)

vim.keymap.set('n', '<leader>h', dap.toggle_breakpoint)

vim.keymap.set('n', '<F1>', dap.continue)
vim.keymap.set('n', '<F2>', dap.step_into)
vim.keymap.set('n', '<F3>', dap.step_over)
vim.keymap.set('n', '<F4>', dap.step_out)
vim.keymap.set('n', '<F5>', dap.step_back)
vim.keymap.set('n', '<F6>', dap.restart)

dap.listeners.before.attach.dapui_config = function ()
	dapui.open()
end
require('dap').listeners.before.launch.dapui_config = function ()
	dapui.open()
end
dap.listeners.before.event_terminated.dapui_config = function ()
	dapui.close()
end
dap.listeners.before.event_exited.dapui_config = function ()
	dapui.close()
end

vim.keymap.set('n', '<leader>d', function ()
	require('dapui').toggle();
end)
