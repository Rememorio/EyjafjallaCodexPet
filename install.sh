#!/usr/bin/env bash
set -eu

# EXIT must retain this state even when Bash unwinds main after an error.
target=''
lock=''
stage=''
backup=''

usage() {
  cat <<'EOF'
Install the Eyjafjalla Codex pet.

Usage: bash install.sh [--source DIRECTORY | --ref REF] [--uninstall]
  --source DIRECTORY  Install a local pet bundle without network access.
  --ref REF           GitHub branch, tag or commit (default: main).
  --uninstall         Move the installed pet to pet-backups.
  --help              Show this help.

Destination: ${CODEX_HOME:-$HOME/.codex}/pets/eyjafjalla
Existing versions are preserved in the same Codex home's pet-backups directory.
EOF
}

fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }

digest() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    fail 'sha256sum or shasum is required.'
  fi
}

verify_bundle() {
  local name expected actual
  for name in pet.json spritesheet.webp; do
    [ -f "$stage/$name" ] || fail "Missing $name."
    expected=$(awk -v name="$name" '$2 == name {print $1}' "$stage/checksums.sha256")
    [ "${#expected}" -eq 64 ] || fail "Invalid checksum entry for $name."
    case "$expected" in *[!0-9a-f]*) fail "Invalid checksum for $name." ;; esac
    actual=$(digest "$stage/$name")
    [ "$actual" = "$expected" ] || fail "Checksum mismatch: $name."
  done
}

cleanup() {
  local result=$?
  trap - EXIT
  # Restore the previous directory if replacement failed after backup.
  if [ "$result" -ne 0 ] && [ -n "$backup" ] && [ -d "$backup/pet" ] && [ ! -e "$target" ] && [ ! -L "$target" ]; then
    mv "$backup/pet" "$target" || printf 'Restore manually from: %s/pet\n' "$backup" >&2
  fi
  [ -z "$stage" ] || rm -rf "$stage"
  rmdir "$lock" 2>/dev/null || true
  exit "$result"
}

backup_current() {
  mkdir -p "$codex_root/pet-backups"
  backup=$(mktemp -d "$codex_root/pet-backups/eyjafjalla.XXXXXX")
  mv "$target" "$backup/pet"
  printf 'Previous pet saved to: %s/pet\n' "$backup"
}

main() {
  local source_dir='' ref=main remove=false explicit_ref=false name base
  local codex_root pets_root
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --source)
        [ "$#" -ge 2 ] && [ -n "$2" ] || fail '--source requires a directory.'
        source_dir=$2; shift 2 ;;
      --ref)
        [ "$#" -ge 2 ] && [ -n "$2" ] || fail '--ref requires a value.'
        ref=$2; explicit_ref=true; shift 2 ;;
      --uninstall) remove=true; shift ;;
      --help|-h) usage; return ;;
      *) fail "Unknown argument: $1" ;;
    esac
  done
  [ -z "$source_dir" ] || [ "$explicit_ref" = false ] || fail 'Use either --source or --ref.'
  if [ "$remove" = true ]; then
    [ -z "$source_dir" ] && [ "$explicit_ref" = false ] || fail '--uninstall cannot be combined with --source or --ref.'
  fi
  case "$ref" in *[!a-zA-Z0-9._/-]*|'') fail 'Invalid ref.' ;; esac
  codex_root=${CODEX_HOME:-${HOME:?HOME or CODEX_HOME must be set}/.codex}
  case "$codex_root" in /*) ;; *) codex_root="$PWD/$codex_root" ;; esac
  pets_root="$codex_root/pets"
  target="$pets_root/eyjafjalla"
  lock="$pets_root/.eyjafjalla-install.lock"
  mkdir -p "$pets_root"
  mkdir "$lock" 2>/dev/null || fail "Another install may be running. Lock: $lock"
  trap cleanup EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  [ ! -L "$target" ] || fail 'The destination is a symlink; refusing to replace it.'
  [ ! -e "$target" ] || [ -d "$target" ] || fail 'The destination is not a directory.'
  if [ "$remove" = true ]; then
    if [ -d "$target" ]; then backup_current; else printf 'Eyjafjalla is not installed.\n'; fi
    printf 'Uninstalled. Refresh the pets list in the desktop app.\n'
  else
    stage=$(mktemp -d "$pets_root/.eyjafjalla-stage.XXXXXX")
    if [ -n "$source_dir" ]; then
      [ -d "$source_dir" ] || fail "Source directory not found: $source_dir"
      for name in pet.json spritesheet.webp checksums.sha256; do
        cp "$source_dir/$name" "$stage/$name"
      done
    else
      command -v curl >/dev/null 2>&1 || fail 'curl is required.'
      base="https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/$ref/pets/eyjafjalla"
      for name in pet.json spritesheet.webp checksums.sha256; do
        curl --fail --silent --show-error --location --retry 2 "$base/$name" -o "$stage/$name"
      done
    fi
    verify_bundle
    if [ -f "$target/pet.json" ] && [ -f "$target/spritesheet.webp" ] && cmp -s "$stage/pet.json" "$target/pet.json" && cmp -s "$stage/spritesheet.webp" "$target/spritesheet.webp"; then
      printf 'Eyjafjalla is already up to date.\n'
    else
      [ ! -d "$target" ] || backup_current
      mv "$stage" "$target"
      stage=''
      printf 'Installed: %s\n' "$target"
    fi
    printf 'Open Settings > Pets > Refresh, then select 艾雅法拉 · Eyjafjalla.\n'
  fi
  exit 0
}

main "$@"
