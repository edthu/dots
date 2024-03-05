# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

ZSH_THEME="powerlevel10k/powerlevel10k"

HISTFILE=~/.zsh/history
HISTSIZE=1000
SAVEHIST=1000
setopt appendhistory

function fuzzy_find() { 
  BUFFER="fzf --print0 | xargs -0 -o nvim"
  zle accept-line
}

zle -N fuzzy_find

bindkey '^f' fuzzy_find

source ~/.zsh/catppuccin_macchiato-zsh-syntax-highlighting.zsh

source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
source ~/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
bindkey '^n' autosuggest-accept

export PATH="$PATH:/home/eax/.local/share/coursier/bin"
export DENO_INSTALL="/home/eax/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"
