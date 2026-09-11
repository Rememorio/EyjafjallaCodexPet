# Eyjafjalla · 艾雅法拉

**A little company while you code.** An unofficial Arknights fan pet for the Codex desktop app.

[简体中文](README.md) · **English** · [日本語](README.ja.md)

[![Validate](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml/badge.svg)](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml)
[![License: MIT — code & docs](https://img.shields.io/badge/code_%26_docs-MIT-blue.svg)](LICENSE)

<p align="center">
  <img src="docs/previews/idle.gif" width="192" height="208" alt="Eyjafjalla idling">
  <img src="docs/previews/waving.gif" width="192" height="208" alt="Eyjafjalla waving">
  <img src="docs/previews/look-loop.gif" width="192" height="208" alt="Eyjafjalla looking around">
</p>

Familiar brown curls, horns, red eyes, and a red-and-white outfit. Includes **9 animation states, 16 gaze directions**, and a transparent background, packaged in the Codex v2 pet format.

## Install

Run in a terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash
```

Open **Settings → Pets → Refresh** and select **艾雅法拉 · Eyjafjalla**. Use the command menu or `/pet` to bring it up. Restart the desktop app if the list does not refresh. Menu names may vary by app version; see the [official pet guide](https://learn.chatgpt.com/en/docs/pets).

Requires a Codex desktop version that supports custom **v2** pets. The Bash installer supports macOS / Linux and requires `curl` and either `shasum` or `sha256sum`. A successful file installation does not guarantee pet support on your platform or app version. This is a local desktop bundle, incompatible with the web uploader's 1536 × 1872 format; it does not sync automatically to the web.

The destination is `~/.codex/pets/eyjafjalla/`, or `$CODEX_HOME/pets/eyjafjalla/` when configured. No `sudo`, Python, or API key is needed.

<details>
<summary>Review the script, install offline, or install manually</summary>

Clone the repository to review the script and install the local bundle:

```bash
git clone https://github.com/Rememorio/EyjafjallaCodexPet.git
cd EyjafjallaCodexPet
bash install.sh --source ./pets/eyjafjalla
```

For manual installation, copy the entire `pets/eyjafjalla/` folder into `pets/` in your Codex data directory. Keep `pet.json` and `spritesheet.webp` together.

To pin a reviewed revision, download `install.sh` from that commit and run `bash install.sh --ref <full-commit-hash>`. Existing branches and tags are also accepted.

</details>

## Animations

| Animation | State |
| --- | --- |
| Idle, move right, move left | Everyday company and movement |
| Wave, jump | Greetings and celebration |
| Failed, waiting | Task trouble or waiting for input |
| Working, reviewing | Executing tasks and checking results |
| 16-direction gaze | Directional looks, plus a neutral frame |

The desktop app determines when each animation plays. Some adjacent gaze directions differ subtly; the animated preview makes these transitions easier to see.

<p align="center">
  <img src="docs/previews/jumping.gif" width="192" height="208" alt="Jump animation">
  <img src="docs/previews/running-right.gif" width="192" height="208" alt="Move-right animation">
</p>

[All animation frames](docs/spritesheet-preview.png) · [16 gaze directions](docs/look-directions.png) · [State transitions](docs/previews/state-transitions.gif)

## Update and uninstall

**Update:** run the install command again. Identical files are left in place. Changed installations are backed up in full to `pet-backups/eyjafjalla.*/pet/` under your Codex data directory; the script prints the exact location. Download or checksum failures leave the current pet intact.

**Uninstall:**

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash -s -- --uninstall
```

Uninstalling also preserves a backup. To restore, move any current `pets/eyjafjalla/` aside, copy the backup's `pet/` directory there, and rename it to `eyjafjalla`. Remove old backups manually when no longer needed.

## Repository and contributions

```text
pets/eyjafjalla/     Installable bundle and SHA-256 checksums
assets/reference/   Original character reference image
docs/previews/      Animated README previews
docs/               Sprite previews, gaze chart, development notes
scripts/            Bundle validation
tests/              Install, update, uninstall, and recovery tests
install.sh          Installer entry point
```

Animation fixes, compatibility reports, and translations are welcome. See the [development guide](docs/development.md) for validation commands. Include your OS, app version, and reproduction steps in bug reports; redact private paths and sensitive information.

## License and attribution

Scripts and documentation are [MIT licensed](LICENSE). **Character designs, artwork, and animations are excluded from MIT**; see [artwork rights](ASSETS.md). This is an unofficial fan project, unaffiliated with the developers or publishers of Arknights and Codex.
