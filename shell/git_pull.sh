#!/usr/bin/env bash
# Copyright 2022 awdev <cs@awdev.my.id>. All rights reserved.
## @author awdev
# @since 2022-09-04 20:42:52
[ "1" = "0" ] && . ./_funcs.sh

__FILE__=$(basename $0)
__DIR__=$(dirname $0)
__intro__="pull the latest revision of the current branch"
__help__="$__FILE__ [args]"
__args__="
    T:trunk:release:string:1:1:the trunk branch to merge into
    R:remote:origin:string:1:1:the remote ref name
"
OPT_trunk="release"
OPT_remote="origin"
. "$__DIR__/_funcs.sh" "$@"
set -e

branch="$(git rev-parse --abbrev-ref HEAD)"

if [ "$branch" = "HEAD" ]; then
    echo_warn "You are not in a local branch, please checkout before run this"
    exit 1
fi

git fetch -apt "$OPT_remote"
git rebase "$OPT_remote/$branch"

if [ "$OPT_trunk" != "" ] && [ "$OPT_trunk" != "$branch" ]; then
    if [ $(git log --oneline "$branch..$OPT_remote/$OPT_trunk" | wc -l) -gt 0 ]; then
        git merge "$OPT_remote/$OPT_trunk"
    fi
fi
