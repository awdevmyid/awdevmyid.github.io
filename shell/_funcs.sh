#!/usr/bin/env bash
#
# funcs.sh
# @author awdev
# @since 2022-09-04 20:42:52
# @desc
#

# short help message
__help__=${__help__:-"util functions for other shell commands"}
# long introduction
__intro__=${__intro__:-"util functions"}
# args specification
# __args__="
#   short_name:long_name:default:kind:optional:max:desc
#   _:_:default:string:1:desc
# "
#
# kind: s(string), b(bool) -> "0"/"1"
#
# example
# __args="
#   f:follow::bool:1:follow the redirects -> boolean value, it is optional
#   f:follow:hello:1:string:follow the redirects -> string value with defaults, it is optional
#   f:follow::string:1:follow the redirects -> string value without defaults, it is required
# "
#
__args__=${__args__:-""}
__global_args__="
    _:debug:0:bool:0:1:debug mode
    h:help:0:bool:0:1:show help message
"

export SCRIPT_ROOT="$(dirname "$(realpath $0)")"

set -e

echo_error() {
    if [ -t 1 ]; then
        echo -e "\033[31mERROR: $@\033[0m"
    else
        echo "ERROR: $@"
    fi
}

echo_lines() {
    for arg in $@
    do
        echo -e "$arg"
    done
}

echo_warn() {
    if [ -t 1 ]; then
        echo -e "\033[33mWARN: $@\033[0m"
    else
        echo "WARN: $@"
    fi
}

echo_info() {
    if [ -t 1 ]; then
        echo -e "\033[32mINFO: $@\033[0m"
    else
        echo "INFO: $@"
    fi
}

echo_bold() {
    if [ -t 1 ]; then
        echo -e "\033[1m$@\033[0m"
    else
        echo "$@"
    fi
}

exit_error() {
    echo_error "$@"
    exit 1
}

git_user() {
    name="$(git config --get user.name | tr -d '[:space:]')"
    echo -n ${name:-`whoami`}
}

git_email() {
    name="$(git config --get user.email | tr -d '[:space:]')"
    echo -n ${name}
}

export now="$(date '+%Y-%m-%d %H:%M:%S')"

_debug=

debug() {
    if [ "$_debug" = "1" ]; then
        echo_bold "DEBUG: $@"
    fi
}

__opt_mask__="                           "

show_options() {
    if [ "$__opt_short__" = "_" ]; then
        content="        --${__opt_long__}"
    elif [ "$__opt_short__" = "__" ]; then
        content="    [$__opt_long__...]"
    else
        content="    -${__opt_short__}, --${__opt_long__}"
    fi
    content="$(printf "%-.${#__opt_mask__}s" "$content$__opt_mask__")"
    if [ "$__opt_default__" != "" ]; then
        content="$content[$__opt_kind__=$__opt_default__]"
    else
        content="$content$__opt_kind__"
    fi
    while read -r line; do
        content="$content\n$__opt_mask__$__opt_desc__"
    done < <(echo "$__opt_desc__")
    echo -e "$content"
}

echo_indent() {
    local indent="$1"
    shift
    while [ $# -gt 0 ]; do
        while IFS= read -r line; do
            printf "%${indent}s${line}\n" ""
        done < <(echo "$1")
        shift
    done
}

show_usage() {
    if [ $# -gt 0 ]; then
        echo_error "$@"
        echo
    fi
    echo_bold $(basename $0):
    echo_indent 4 "$__intro__"
    echo
    echo_bold "Usage:"
    echo_indent 4 "$__help__"
    echo
    echo_bold "Options:"
    while read -r options; do
        parse_options "$options"
        if [ "$__opt_long__" != "" ]; then
            show_options
        fi
    done < <(echo "$__global_args__")
    while read -r options; do
        parse_options "$options"
        if [ "$__opt_long__" != "" ]; then
            show_options
        fi
    done < <(echo "$__args__")
    if [ $# -gt 0 ]; then
        exit 1
    else 
        exit 0
    fi
}

show_intro() {
    echo "$__intro__"
    exit 0
}

parse_name() {
    echo "$1" | sed -E 's/^-+//'
}

export __arg_mode__=""

__opt_short__=""
__opt_long__=""
__OPT_short__=""
__OPT_long__=""
__opt_default__=""
__opt_kind__=""
__opt_optional__=""
__opt_max__=""
__opt_desc__=""

parse_options() {
    local opt="$(echo "$1" | sed -E 's/^ +| +$//g')"
    __opt_short__="$(echo "$opt" | awk -F: '{print $1}')"
    __opt_long__="$(echo "$opt" | awk -F: '{print $2}')"
    __OPT_short__="OPT_$(echo "$opt" | awk -F: '{print $1}')"
    __OPT_long__="OPT_$(echo "$opt" | awk -F: '{print $2}')"
    __opt_default__="$(echo "$opt" | awk -F: '{print $3}')"
    __opt_kind__="$(echo "$opt" | awk -F: '{print $4}')"
    __opt_optional__="$(echo "$opt" | awk -F: '{print $5}')"
    __opt_max__="$(echo "$opt" | awk -F: '{print $6}')"
    __opt_desc__="$(echo "$opt" | awk -F: '{print $7}')"
    eval "
        if [ \${#__val__$__opt_short__[@]} -eq 0 ]; then
            __val__$__opt_short__=()
            __val__$__opt_long__=()
        fi
    "
}

process_args() {
    local name="$1"
    local value="$2"
    __arg_mode__="0" # 0: name not exist, 1: no value, 2: use value, 3: need value
    while read -r options; do
        parse_options "$options"
        if [ "$__opt_long__" = "_val_" ]; then
            continue
        fi
        if [ "$__opt_long__" != "$name" ] && [ "$__opt_short__" != "$name" ]; then
            continue
        fi
        case "$__opt_kind__" in
            bool)
                eval "__val__$__opt_short__=1; __val__$__opt_long__=1"
                __arg_mode__="1"
                ;;
            string)
                case "$value" in
                    -*)
                        __arg_mode__="3"
                        break
                        ;;
                    \*)
                        # --foo \--bar -> foo:--bar
                        local value="$(echo "$value" | sed -E 's/^\\//')"
                        ;;
                esac
                eval "__val__$__opt_short__+=('$value'); __val__$__opt_long__+=('$value');"
                __arg_mode__="2"
                ;;
            *)
                exit_error "Unknown opt kind: $__opt_kind__ -> $options"
                ;;
        esac
        break
    done < <(echo "$__args__")
    debug "--> done $__arg_mode__"
}

check_args() {
    while read -r options; do
        parse_options "$options"
        if [ "$__opt_long__" = "" ]; then
            continue
        fi
        eval "
            if [ \${#__val__$__opt_short__[@]} -eq 0 ]; then
                if [ '$__opt_optional__' != '1' ]; then
                    show_usage 'Argument $__opt_long__ is required'
                fi
                $__OPT_short__="$__opt_default__"
                $__OPT_long__="$__opt_default__"
            else
                $__OPT_short__=(\"\${__val__$__opt_short__[@]}\")
                $__OPT_long__=(\"\${__val__$__opt_long__[@]}\")
            fi
            export $__OPT_short__
            export $__OPT_long__
        "
    done < <(echo "$__args__")
}

parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            -h | --help | ?)
                show_usage
                ;;
            -i | --intro)
                show_intro
                ;;
            --debug)
                _debug=1
                set -x
                ;;
            -*)
                process_args "$(parse_name "$1")" "$2"
                case "$__arg_mode__" in
                    0)
                        show_usage "Unknown argument: $1"
                        ;;
                    1)
                        ;;
                    2)
                        if [ $# = 1 ]; then
                            show_usage "Value of argument $1 is required"
                        else
                            shift
                        fi
                        ;;
                    3)
                        show_usage "Value of argument $1 is required"
                        ;;
                esac
                ;;
            *)
                process_args "__" "$1"
                if [ "$__arg_mode__" = "0" ]; then
                    show_usage "Positional argument $1 is not allowed"
                fi
                ;;
        esac
        shift
    done
}

parse_args "$@"
check_args
debug "after check _val_filename: ${#_val_filename[@]}"
debug "after check OPT_filename: ${#OPT_filename[@]}"
