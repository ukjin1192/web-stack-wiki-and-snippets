export ZSH=/root/.oh-my-zsh

ZSH_THEME="robbyrussell"

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

source $ZSH/oh-my-zsh.sh

setopt PROMPT_SUBST
PROMPT='%(!.%F{red}.%F{cyan})%n%f@%F{yellow}%m%f%(!.%F{red}.)%} ➜ %{$(pwd|grep --color=always /)%${#PWD}G%} %{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[blue]%} % %{$reset_color%}'
