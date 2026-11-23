#!/usr/bin/env zsh
# Check Python code with the Ruff version pinned in framework_tool.
# Usage (any directory):
#   <framework>/framework_tool/scripts/scpt_check_python.sh [--fix] [<dir>]
# Examples from a product root next to python-framework:
#   ../python-framework/framework_tool/scripts/scpt_check_python.sh
#   ../python-framework/framework_tool/scripts/scpt_check_python.sh --fix src/ileague_api
#
# Without --fix: ruff check and ruff format --check; nothing is modified.
# With --fix: ruff check --fix, then ruff format.
# Rules come from the ruff.toml found above each checked file, which extends
# framework_tool/ruff.toml. Exits with 1 when any step fails.

set -u

bol_fix=false
if [[ "${1:-}" == "--fix" ]]; then
    bol_fix=true
    shift
fi

str_tool_dir="${0:A:h:h}"
str_target="${1:-.}"
str_target="${str_target:A}"

if $bol_fix; then
    lst_steps=("check --fix" "format")
else
    lst_steps=("check" "format --check")
fi

int_failed=0
for str_step in "${lst_steps[@]}"; do
    print "ruff $str_step $str_target"
    uv run --project "$str_tool_dir" ruff ${=str_step} "$str_target" || int_failed=$((int_failed + 1))
done

if (( int_failed > 0 )); then
    exit 1
fi
