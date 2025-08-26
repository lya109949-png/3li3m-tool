#!/usr/bin/env bash
set -euo pipefail

SESS_DIR="sessions"
mkdir -p "$SESS_DIR"

green="\e[1;92m"; yellow="\e[1;93m"; red="\e[1;91m"; reset="\e[0m"

banner() {
  echo -e "${green}== SAFE DEMO (no TOR, VPN handled by OS) ==${reset}"
}

save_session() {
  local user="$1" pass="$2" wl_pass="$3"
  local f="$SESS_DIR/store.session.$user"
  printf 'user="%s"\npass="%s"\nwl_pass="%s"\n' "$user" "$pass" "$wl_pass" > "$f"
  echo -e "${yellow}Session saved -> ${f}${reset}"
}

resume_session() {
  local user="$1"
  local f="$SESS_DIR/store.session.$user"
  [[ -f "$f" ]] || { echo -e "${red}No session for ${user}${reset}"; exit 1; }
  # shellcheck disable=SC1090
  source "$f"
  echo -e "${green}Resumed: ${user}${reset}"
}

simulate_loop() {
  local user="$1" wl="$2"
  local total=1
  [[ -f "$wl" ]] && total=$(wc -l < "$wl")
  echo -e "${green}Username:${reset} $user"
  echo -e "${green}Wordlist:${reset} ${wl:-none} (${total})"
  echo -e "${yellow}Demo only. No network requests.${reset}"
  if [[ -f "$wl" ]]; then
    local i=0
    while IFS= read -r pw || [[ -n "$pw" ]]; do
      ((i++))
      printf "\r[demo] trying %d/%d ..." "$i" "$total"
      sleep 0.03
    done < "$wl"
    echo -e "\n${yellow}Done.${reset}"
  else
    echo -e "${yellow}Single-password demo done.${reset}"
  fi
}

main() {
  banner
  if [[ "${1:-}" == "--resume" && -n "${2:-}" ]]; then
    resume_session "$2"
  else
    read -rp $'\e[1;92mEnter username: \e[0m' user
    echo "1) Single password"
    echo "2) Wordlist file"
    read -rp "Select 1/2: " mode
    pass=""; wl=""
    if [[ "$mode" == "1" ]]; then
      read -rsp $'\e[1;92mEnter password: \e[0m' pass; echo
    elif [[ "$mode" == "2" ]]; then
      read -rp $'\e[1;92mPath to wordlist: \e[0m' wl
      [[ -f "$wl" ]] || { echo -e "${red}Wordlist not found${reset}"; exit 1; }
    else
      echo -e "${red}Invalid choice${reset}"; exit 1
    fi
    read -rp $'\e[1;93mSave session? [y/N]: \e[0m' s; s=${s:-N}
    [[ "$s" =~ ^(y|Y|yes|Yes)$ ]] && save_session "$user" "$pass" "$wl"
  fi
  echo -e "${yellow}No TOR used. If your system VPN is ON, traffic goes through it by default.${reset}"
  simulate_loop "${user:-$USER}" "${wl:-/dev/null}"
}

trap 'echo -e "\n'"$yellow"'Exiting.'"$reset"'' INT
main "$@"
