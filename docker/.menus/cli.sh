#!/usr/bin/env bash
# shellcheck disable=SC2034
set -euo pipefail

cli() {
  local PARSED_ARGS=
  local DELIM=

  for arg in "$@" ; do
    shift
    case "$arg" in
      --prereq)
        PARSED_ARGS="${PARSED_ARGS:-}-p "
      ;;
      --apps)
        PARSED_ARGS="${PARSED_ARGS:-}-a "
      ;;
      --env)
        PARSED_ARGS="${PARSED_ARGS:-}-e "
      ;;
      --compose)
        PARSED_ARGS="${PARSED_ARGS:-}-c "
      ;;
      --update)
        PARSED_ARGS="${PARSED_ARGS:-}-u "
      ;;
      --prune)
        PARSED_ARGS="${PARSED_ARGS:-}-P "
      ;;
      --test)
        PARSED_ARGS="${PARSED_ARGS:-}-t "
      ;;
      --verbose)
        PARSED_ARGS="${PARSED_ARGS:-}-v "
      ;;
      --debug)
        PARSED_ARGS="${PARSED_ARGS:-}-x "
      ;;
      --logLevel)
        PARSED_ARGS="${PARSED_ARGS:-}-l "
      ;;
      --help)
        PARSED_ARGS="${PARSED_ARGS:-}-h "
      ;;
      *)
        [[ "${arg:0:1}" == "-" ]] || DELIM="\""
        PARSED_ARGS="${PARSED_ARGS:-}${DELIM}${arg}${DELIM} "
      ;;
    esac
  done

  eval set -- "${PARSED_ARGS:-}"

  while getopts ":p:aec:uPt:vxl:h" SELECTED ; do
    case $SELECTED in
      p)
        case ${OPTARG} in
          noremove)
            run_sh "$SCRIPTDIR" "prereq_install" "Y"
          ;;
          test)
            run_sh "$SCRIPTDIR" "yq_install"
          ;;
          *)
            usage
          ;;
        esac
        exit
      ;;
      a)
        run_sh "$SCRIPTDIR" "editor_open" "${BASEDIR}/.apps"
        exit
      ;;
      e)
        run_sh "$SCRIPTDIR" "editor_open" "${BASEDIR}/.env"
        exit
      ;;
      c)
        case ${OPTARG} in
          up)
            run_sh "$SCRIPTDIR" "compose_create"
            run_sh "$SCRIPTDIR" "compose_up"
          ;;
          pull)
            run_sh "$SCRIPTDIR" "compose_create"
            run_sh "$SCRIPTDIR" "compose_pull"
          ;;
          restart)
            run_sh "$SCRIPTDIR" "compose_create"
            run_sh "$SCRIPTDIR" "compose_restart"
          ;;
          down)
            run_sh "$SCRIPTDIR" "compose_down"
          ;;
          create)
            run_sh "$SCRIPTDIR" "compose_create"
          ;;
          *)
            usage
          ;;
        esac
        exit
      ;;
      u)
        run_sh "$SCRIPTDIR" "self_update" "${BASEDIR}"
        exit
      ;;
      P)
        run_sh "$SCRIPTDIR" "docker_prune"
        exit
      ;;
      t)
        case ${OPTARG} in
          t_unit)
            sudo chmod +x "${TESTDIR}/${OPTARG}.sh"
            sudo "${TESTDIR}/${OPTARG}.sh"
          ;;
          *)
            run_sh "$TESTDIR" "${OPTARG}"
          ;;
        esac
        exit
      ;;
      v)
        _VERBOSE=6
      ;;
      x)
        _VERBOSE=7
      ;;
      l)
        local level
        if ! [[ "${OPTARG}" =~ ^[0-9]+$ ]] ; then
          log 4 "Log level must be a number, but you passed: ${OPTARG}."
          level=6
        else
          level=${OPTARG}
        fi

        log 6 "Setting log level to ${level}."
        _VERBOSE=$level
      ;;
      h)
        usage
        exit
      ;;
      :)
        case ${OPTARG} in
          c)
            run_sh "$SCRIPTDIR" "compose_create"
            run_sh "$SCRIPTDIR" "compose_up"
            exit
          ;;
          p)
            run_sh "$SCRIPTDIR" "prereq_install"
            exit
          ;;
          *)
            log 3 "${OPTARG} requires an argument."
            exit
          ;;
        esac
      ;;
      *)
        usage
        exit
      ;;
    esac
  done
  return 0
}
