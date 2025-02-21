local ensure_packer = function()
  local fn = vim.fn
  local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd [[packadd packer.nvim]]
    return true
  end
  return false
end

local packer_bootstrap = ensure_packer()

return require('packer').startup(function(use)
  use {'wbthomason/packer.nvim'}

  use {
      'nvim-lualine/lualine.nvim',
      requires = { 'nvim-tree/nvim-web-devicons', opt = true }
  }

  use { "catppuccin/nvim", as = "catppuccin",
  	opts =  {
	  transparent = true
	}}

  use {"B4mbus/oxocarbon-lua.nvim", as = "oxocarbon"}

  use {
        'nvim-treesitter/nvim-treesitter',
        run = function()
            local ts_update = require('nvim-treesitter.install').update({ with_sync = true })
            ts_update()
        end,
    }

  use 'nvim-tree/nvim-web-devicons'

  use 'nvim-treesitter/playground'

  use {
  'nvim-telescope/telescope.nvim', tag = '0.1.2',
  requires = { {'nvim-lua/plenary.nvim'} }
  }

  use({'scalameta/nvim-metals', requires = { "nvim-lua/plenary.nvim" }})

  use {
  'VonHeikemen/lsp-zero.nvim',
  branch = 'v2.x',
  requires = {
    -- LSP Support
    {'neovim/nvim-lspconfig'},             -- Required
    {                                      -- Optional
      'williamboman/mason.nvim',
      run = function()
        pcall(vim.api.nvim_command, 'MasonUpdate')
      end,
    },
    {'williamboman/mason-lspconfig.nvim'}, -- Optional

    -- Autocompletion
    {'hrsh7th/nvim-cmp'},     -- Required
    {'hrsh7th/cmp-nvim-lsp'}, -- Required
    {'L3MON4D3/LuaSnip'},     -- Required
   }
  }

  use 'christoomey/vim-tmux-navigator'

  use {
	"windwp/nvim-autopairs",
    config = function() require("nvim-autopairs").setup {} end
  }

  use 'ThePrimeagen/harpoon'

  use 'mbbill/undotree'

  use 'xiyaowong/transparent.nvim'

	use {'shortcuts/no-neck-pain.nvim'}


  use {
	"echasnovski/mini.hipatterns",
	config = require('mini.hipatterns').setup({
		highlighters = {
			hex_color = require('mini.hipatterns').gen_highlighter.hex_color(),
	}})
  }

  use {
		"mfussenegger/nvim-dap",
		requires = {
			{'theHamsta/nvim-dap-virtual-text'}
		}
	}

	use {
		'rcarriga/nvim-dap-ui',
		requires = {'nvim-neotest/nvim-nio',
								'mfussenegger/nvim-dap'},
	}

	use 'folke/neodev.nvim'

  -- Automatically set up your configuration after cloning packer.nvim
  -- Put this at the end after all plugins
  if packer_bootstrap then
    require('packer').sync()
  end
end)
