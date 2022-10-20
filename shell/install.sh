#!/usr/bin/env bash
#
# install.sh
# @author awdev
# @since 2022-09-04 20:42:52
# @desc
#

__intro__="Install scripts to your machine"
__help__=`basename $0`
. "$(dirname $0)/funcs.sh"

filename="$(basename $0)"

if [ "$(which $filename)" != "" ]; then
    warn "Already installed, run help.sh to get installed commands!"
fi

cd "$(dirname $0)"

if [ "$(cat ~/.bash_profile | grep $(pwd) | wc -l)" -gt 0 ]; then
    error "You have already installed scripts, please restart your shell and do not install twice!"
fi

echo "
export PATH=$(pwd):\$PATH
" >> ~/.bash_profile
. ~/.bash_profile

if [ "$(which $filename)" == "" ]; then
    error "Install failed, please check your ~/.bash_profile file content!"
fi

pw "Scripts installed, please restasrt your terminal or run . ~/.bash_profile to load scripts in current terminal"
info "You can run help.sh to get installed commands list!"
