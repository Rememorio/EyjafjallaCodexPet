# エイヤフィヤトラ · Eyjafjalla

デスクトップに、エイヤフィヤトラを。

『アークナイツ』のエイヤフィヤトラを題材にした非公式の Codex ペットです。カーソルを目で追い、手を振り、小さく跳ねながら、作業の時間に寄り添います。

<p align="center">
  <img src="docs/previews/look-loop.png" width="96" height="104" alt="Eyjafjalla">
</p>

[![Validate](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml/badge.svg)](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml) [![Pet v2](https://img.shields.io/badge/Codex_Pet-v2-f2a1a8)](pets/eyjafjalla/pet.json) [![License: MIT — code & docs](https://img.shields.io/badge/code_%26_docs-MIT-blue.svg)](LICENSE)

## インストール

ターミナルに貼り付けて実行します。リポジトリのクローンは不要です。

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash
```

<strong>設定 → ペット → 更新</strong>を開き、<strong>艾雅法拉 · Eyjafjalla</strong>を選択します。コマンドメニューまたは `/pet` から呼び出せます。古い動作が表示される場合は、ペットを選び直すか、アプリを再起動してください。

カスタム v2 ペット対応の Codex デスクトップアプリが必要です。インストーラーは macOS / Linux の Bash 環境で、`curl` とシステムの SHA-256 ツールを使います。`sudo`、Python、API キーは不要です。

## デスクトップで一緒に

9 種類の状態アニメーションと、16 方向の頭・視線の動きを収録しています。プレビューは配布パッケージと同じフレーム・再生間隔です。

<table>
<tr>
<td align="center" width="240"><strong>待機</strong><br><img src="docs/previews/idle.png" width="96" height="104" alt="待機"></td>
<td align="center" width="240"><strong>右へ移動</strong><br><img src="docs/previews/running-right.png" width="96" height="104" alt="右へ移動"></td>
<td align="center" width="240"><strong>左へ移動</strong><br><img src="docs/previews/running-left.png" width="96" height="104" alt="左へ移動"></td>
</tr>
<tr>
<td align="center" width="240"><strong>手を振る</strong><br><img src="docs/previews/waving.png" width="96" height="104" alt="手を振る"></td>
<td align="center" width="240"><strong>小さなジャンプ</strong><br><img src="docs/previews/jumping.png" width="96" height="104" alt="小さなジャンプ"></td>
<td align="center" width="240"><strong>しょんぼり</strong><br><img src="docs/previews/failed.png" width="96" height="104" alt="しょんぼり"></td>
</tr>
<tr>
<td align="center" width="240"><strong>返事を待つ</strong><br><img src="docs/previews/waiting.png" width="96" height="104" alt="返事を待つ"></td>
<td align="center" width="240"><strong>作業中</strong><br><img src="docs/previews/running.png" width="96" height="104" alt="作業中"></td>
<td align="center" width="240"><strong>確認中</strong><br><img src="docs/previews/review.png" width="96" height="104" alt="確認中"></td>
</tr>
</table>

カーソルの方向へ顔を向け、重ねると小さくジャンプします。作業中・返事待ち・完了などの状態は Codex が切り替えます。プレビューは可逆圧縮の APNG で、半透明の輪郭を保ち、ライト・ダーク両方のテーマに対応します。

## 更新とアンインストール

<strong>更新</strong>：インストールコマンドを再実行します。同じファイルはそのまま保持します。新版は検証後に入れ替え、旧フォルダー全体のバックアップ先を表示します。

<strong>アンインストール</strong>：

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash -s -- --uninstall
```

既定の保存先は `~/.codex/pets/eyjafjalla/` です。`CODEX_HOME` を設定している場合は、その配下を使います。アンインストール時も復元用に旧ペットを残します。オフラインでの導入、リビジョン指定、復元は[インストールの詳細](docs/installation.md)をご覧ください。

## 改善への参加

不自然な動き、インストールの不具合、翻訳の改善を歓迎します。Issue には OS、Codex のバージョン、操作手順、対象の動作や視線方向を添えてください。配布用ペットは `pets/eyjafjalla/` にあります。検証方法は[開発ガイド](docs/development.md)をご覧ください。

## ライセンス

スクリプトと文書は [MIT](LICENSE) で提供します。キャラクター、美術素材、アニメーションは対象外です。[素材の権利について](ASSETS.md)をご確認ください。本プロジェクトは非公式のファン作品であり、『アークナイツ』および Codex の開発元・提供元による公認や支援を受けていません。

---

[简体中文](README.md) · [English](README.en.md)
