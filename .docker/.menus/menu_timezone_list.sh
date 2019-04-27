#!/usr/bin/env bash
set -euo pipefail

menu_timezone_list() {
  local CURRTZ
  local -a TIMEZONES
  local -a OPTIONS

  TIMEZONES=$(run_sh "$SCRIPTDIR" "timezone_list")
  CURRTZ=$(run_sh "$SCRIPTDIR" "timezone_get")

  for tz in $TIMEZONES ; do
    if [ "$tz" = "$CURRTZ" ] ; then
      OPTIONS=("${OPTIONS[@]}" "$tz" "" "ON")
    else
      OPTIONS=("${OPTIONS[@]}" "$tz" "" "OFF")
    fi
  done

  log 7 "Opening timezone list menu."
  local SELECTION
  SELECTION=$(whiptail --title "media-docker Configuration" --radiolist \
    "Select the desired timezone." 0 0 0 \
    "${OPTIONS[@]}" 3>&1 1>&2 2>&3 || echo "$CURRTZ")

  case $SELECTION in
    *)
      log 7 "Timezone: ${SELECTION} selected."
      echo "$SELECTION"
    ;;
  esac
}
