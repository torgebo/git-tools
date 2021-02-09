#!/usr/bin/env bash

alias g='git status'
alias ga='git add'
alias gm='git commit -v'
alias gmnotest='git commit -v --no-verify'
alias gd='git diff --submodule=diff'
alias gl='git log'
alias gg='git grep --recurse-submodules'
alias gb='git branch --color -r -vv --sort=-committerdate'
alias gbb="git for-each-ref --sort=-committerdate refs/heads --format='%(HEAD)%(color:yellow)%(refname:short)|%(color:bold green)%(committerdate:relative)|%(color:blue)%(subject)|%(color:magenta)%(authorname)%(color:reset)' --color=always | column -ts'|'"


alias gresmas='git reset --soft $(git merge-base master HEAD)'
