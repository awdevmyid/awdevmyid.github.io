#!/usr/bin/env bash
#
# readme.sh
# @author awdev
# @since 2022-09-04 20:42:52
# @desc
#

__intro__="[Internal] generate readme for the project"
__help__=`basename $0`

cd `dirname $0`
. _funcs.sh

file=README.md

echo "# Utils commands for developer

This is a project hold on some useful shell/python scripts for developer

## Install

\`\`\`bash
gh repo clone awdev-corporation/awdev


sh ./scripts/install.sh
\`\`\`

## Index
" > $file

cmds="$(find . -type f | grep -v '/\.')"

for cmd in $cmds
do
    cmd=`basename $cmd`
    if [ -x "$cmd" ] && [ "$(git check-ignore $cmd)" == "" ]; then
        echo "- [$cmd](#$(echo $cmd | sed -E 's/\.//')) - $("$cmd" -i)" >> $file
    fi
done

echo "
## Commands

" >> $file

for cmd in $cmds
do
    if [ -x $cmd ] && [ "$(git check-ignore $cmd)" == "" ]; then
        echo "### $(basename $cmd)

$($cmd -i) [source]($cmd)

\`\`\`bash
$($cmd -h)
\`\`\`

[top](#index)
" >> $file
    fi
done

echo "## License

[MIT](./LICENSE)

" >> $file

