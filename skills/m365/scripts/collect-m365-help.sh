#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "${script_dir}/.." && pwd)"
out_dir="${skill_root}/references/generated"
mkdir -p "$out_dir"

version="$(m365 version)"
m365 --help > "${out_dir}/m365-help.txt"

{
  printf '# Generated m365 Help Snapshot\n\n'
  printf -- '- Version: %s\n' "$version"
  printf -- '- Generated: %s\n\n' "$(date +%F)"
} > "${out_dir}/index.md"

grep -E '^[[:space:]]{2}[a-z0-9]+ \* ' "${out_dir}/m365-help.txt" | awk '{print $1}' | while read -r group; do
  m365 "$group" --help > "${out_dir}/${group}-help.txt"
  printf -- '- `%s` -> `references/generated/%s-help.txt`\n' "$group" "$group" >> "${out_dir}/index.md"
done

