#!/usr/bin/env bash
set -euo pipefail

version="0.66.0"
release_url="https://github.com/prefix-dev/pixi/releases/download/v${version}"

case "$(uname -s):$(uname -m)" in
  Darwin:arm64)
    asset="pixi-aarch64-apple-darwin"
    expected_sha256="6bce870c2126cc4ad0c8ba8d58f22a8031cd7c9e875e5f6659a06410d1c755e5"
    ;;
  Linux:x86_64)
    asset="pixi-x86_64-unknown-linux-musl"
    expected_sha256="4d8124d3fbe6c201482437873bc67e735e35f3506568e706136c4e079c26929e"
    ;;
  *)
    printf 'Unsupported bootstrap platform: %s:%s\n' "$(uname -s)" "$(uname -m)" >&2
    exit 2
    ;;
esac

install_dir="${PIXI_INSTALL_DIR:-${HOME}/.local/bin}"
temporary_file="$(mktemp "${TMPDIR:-/tmp}/pixi.XXXXXX")"
trap 'rm -f "$temporary_file"' EXIT

curl --fail --location --proto '=https' --tlsv1.2 \
  "${release_url}/${asset}" --output "$temporary_file"

if command -v sha256sum >/dev/null 2>&1; then
  actual_sha256="$(sha256sum "$temporary_file" | cut -d ' ' -f 1)"
else
  actual_sha256="$(shasum -a 256 "$temporary_file" | cut -d ' ' -f 1)"
fi

if [[ "$actual_sha256" != "$expected_sha256" ]]; then
  printf 'Pixi checksum mismatch: expected %s, got %s\n' \
    "$expected_sha256" "$actual_sha256" >&2
  exit 1
fi

mkdir -p "$install_dir"
install -m 0755 "$temporary_file" "$install_dir/pixi"
"$install_dir/pixi" --version
