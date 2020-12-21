#!/usr/bin/env bash

alias g='git status'
alias ga='git add'
alias gm='git commit -v'
alias gmnotest='git commit -v --no-verify'
alias gd='git diff --submodule=diff'
alias gl='git log'
alias gg='git grep --recurse-submodules'
alias gb='git branch'

alias gresmas='git reset --soft $(git merge-base master HEAD)'
