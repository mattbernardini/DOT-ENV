#!/usr/bin/env bash
set -euo pipefail

init_detect() {
  local INITSYS
  if [[ $(/sbin/init --version > /dev/null 2>&1) =~ upstart ]]; then
    INITSYS="upstart"
  elif [[ $(systemctl) =~ -\.mount ]]; then
    INITSYS="systemd"
  elif [[ -f /etc/init.d/cron && ! -h /etc/init.d/cron ]]; then
    INITSYS="sysv-init";
  elif [[ $(ps 1) =~ 'launchd' ]] ; then
    INITSYS="launchd"
  else
    log 3 "Could not determine init system."
  fi
  log 6 "Detected init system as: ${INITSYS}."
  echo "$INITSYS"
}