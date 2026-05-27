#!/usr/bin/env bash
set -euo pipefail

: "${NO_UPDATE_NOTIFIER:=1}"
export NO_UPDATE_NOTIFIER

failed=0

run_check() {
  local name="$1"
  shift
  if output="$("$@" 2>&1)"; then
    printf 'OK    %s\t%s\n' "$name" "$(printf '%s' "$output" | head -n 1)"
  else
    printf 'FAIL  %s\t%s\n' "$name" "$(printf '%s' "$output" | head -n 1)"
    failed=1
  fi
}

run_check "node" node --version
run_check "npm" npm --version
run_check "m365 version" m365 version --output text
run_check "m365 status" m365 status --output text
run_check "m365 help" bash -lc 'm365 --help | awk "NF{print; exit}"'

exit "$failed"
