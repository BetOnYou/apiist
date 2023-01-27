export ZSH=$HOME/.oh-my-zsh

ZSH_THEME="agnoster"
plugins=(
    git
    colored-man-pages
    docker-compose
    golang
    colorize
)

source $ZSH/oh-my-zsh.sh

# Default git aliases
alias commit="git commit -a"
alias push="git push"
alias status="git status"
alias pull="git pull"
alias stash="git stash"
alias rebase="git rebase"
alias fpush="git push --force-with-lease"
alias checkout="git checkout"
alias new_branch="git checkout -b"
alias amend="git commit --amend"
alias ls="ls -lAFG"

export PROMPT_COMMAND='history -a'
export HISTFILE=$HOME/commandhistory/.zsh_history
export PATH="/home/vscode/.local/share/solana/install/active_release/bin:$PATH"