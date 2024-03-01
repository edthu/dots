local nvim_metals_group = vim.api.nvim_create_augroup("nvim-metals", { clear = true })

vim.api.nvim_create_autocmd("FileType", {
	pattern = { "scala", "sbt", "java" },
	callback = function()
	  require("metals").initialize_or_attach({})
	end,
	group = nvim_metals_group,
})

local metals_config = require("metals").bare_config()
metals_config.init_options.statusBarProvider = "on"
