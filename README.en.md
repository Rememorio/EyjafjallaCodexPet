# Eyjafjalla · 艾雅法拉

A little company on your desktop.

An unofficial Arknights fan pet for Codex. Eyjafjalla follows your cursor, waves, takes a little hop, and keeps you company while you work.

<p align="center">
  <img src="docs/previews/look-loop.png" width="96" height="104" alt="Eyjafjalla">
</p>

[![Validate](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml/badge.svg)](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml) [![Pet v2](https://img.shields.io/badge/Codex_Pet-v2-f2a1a8)](pets/eyjafjalla/pet.json) [![License: MIT — code & docs](https://img.shields.io/badge/code_%26_docs-MIT-blue.svg)](LICENSE)

## Install

Paste this into your terminal. No clone required:

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash
```

Open <strong>Settings → Pets → Refresh</strong> and choose <strong>艾雅法拉 · Eyjafjalla</strong>. Bring her up with the command menu or `/pet`. If an older animation remains visible, select the pet again or restart the app.

Requires a Codex desktop version with custom v2 pet support. The Bash installer runs on macOS / Linux using `curl` and a system SHA-256 tool. No `sudo`, Python, or API key is needed.

## Your desktop companion

9 animation states, plus head-and-eye tracking in 16 directions. These previews use the actual packaged frames and playback timings.

<table>
<tr>
<td align="center" width="240"><strong>Idle</strong><br><img src="docs/previews/idle.png" width="96" height="104" alt="Idle"></td>
<td align="center" width="240"><strong>Move right</strong><br><img src="docs/previews/running-right.png" width="96" height="104" alt="Move right"></td>
<td align="center" width="240"><strong>Move left</strong><br><img src="docs/previews/running-left.png" width="96" height="104" alt="Move left"></td>
</tr>
<tr>
<td align="center" width="240"><strong>Wave</strong><br><img src="docs/previews/waving.png" width="96" height="104" alt="Wave"></td>
<td align="center" width="240"><strong>Hop</strong><br><img src="docs/previews/jumping.png" width="96" height="104" alt="Hop"></td>
<td align="center" width="240"><strong>Blocked</strong><br><img src="docs/previews/failed.png" width="96" height="104" alt="Blocked"></td>
</tr>
<tr>
<td align="center" width="240"><strong>Waiting</strong><br><img src="docs/previews/waiting.png" width="96" height="104" alt="Waiting"></td>
<td align="center" width="240"><strong>Working</strong><br><img src="docs/previews/running.png" width="96" height="104" alt="Working"></td>
<td align="center" width="240"><strong>Reviewing</strong><br><img src="docs/previews/review.png" width="96" height="104" alt="Reviewing"></td>
</tr>
</table>

Move the cursor to have her look your way; hover for a little hop. Codex controls the working, waiting, and completion states. Lossless APNG previews preserve translucent edges on both light and dark themes.

## Update and uninstall

<strong>Update</strong>: run the install command again. Identical files stay in place. A new version is verified before the previous directory is backed up and replaced; the installer prints the backup location.

<strong>Uninstall</strong>:

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash -s -- --uninstall
```

The default location is `~/.codex/pets/eyjafjalla/`, or the corresponding location under `CODEX_HOME`. Uninstalling also preserves the previous pet for recovery. See [installation options](docs/installation.md) for offline installation, pinned revisions, and restoration.

## Contribute

Reports of awkward animations, installation issues, and translation improvements are welcome. Include your OS, Codex version, trigger, and the affected animation or gaze direction. The installable bundle is in `pets/eyjafjalla/`; see the [development guide](docs/development.md) for validation rules.

## License

Scripts and documentation are [MIT licensed](LICENSE). Character designs, artwork, and animations are excluded; see [artwork rights](ASSETS.md). This is an unofficial fan project, unaffiliated with or endorsed by the developers or publishers of Arknights and Codex.

---

[简体中文](README.md) · [日本語](README.ja.md)
