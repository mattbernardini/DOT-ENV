#!/usr/bin/env bash
set -euo pipefail

timezone_set() {
  local NEWZONE

  NEWZONE=${1:-}

  sudo timedatectl set-timezone "${NEWZONE}" \
    > /dev/null 2>&1 \
    || log 3 "Error setting timezone."
}
