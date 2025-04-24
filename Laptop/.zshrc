# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

ZSH_THEME="powerlevel10k/powerlevel10k"

bindkey '^p' history-search-backward
bindkey '^n' history-search-forward
bindkey '^l' autosuggest-accept

HISTFILE=~/.zsh/history
HISTSIZE=1000
SAVEHIST=1000
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

setopt AUTO_CD
export PATH="$PATH:/home/eax/.local/share/coursier/bin"

alias ga="git add"
alias gc="git commit -m"
alias gs="git status"
alias gp="git push"
alias gpu="git pull"

alias cdlear="clear && cd"

eval "$(fzf --zsh)"

function fuzzy_find() { 
  BUFFER="fzf --print0 | xargs -0 -o nvim"
  zle accept-line
}

zle -N fuzzy_find

# bindkey '^g' fuzzy_find never ended up using this

source ~/.zsh/catppuccin_macchiato-zsh-syntax-highlighting.zsh
source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
source /home/eax/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
