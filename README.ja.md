# エイヤフィヤトラ · Eyjafjalla

**コードを書く時間に、エイヤフィヤトラを。** Codex デスクトップアプリ向けの『アークナイツ』非公式ファン制作ペットです。

[简体中文](README.md) · [English](README.en.md) · **日本語**

[![Validate](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml/badge.svg)](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml)
[![License: MIT — code & docs](https://img.shields.io/badge/code_%26_docs-MIT-blue.svg)](LICENSE)

<p align="center">
  <img src="docs/previews/idle.gif" width="192" height="208" alt="待機中のエイヤフィヤトラ">
  <img src="docs/previews/waving.gif" width="192" height="208" alt="手を振るエイヤフィヤトラ">
  <img src="docs/previews/look-loop.gif" width="192" height="208" alt="周囲を見回すエイヤフィヤトラ">
</p>

茶色の巻き髪、角、赤い瞳、そして赤と白の衣装。おなじみの特徴を残した、**9 種類の状態アニメーションと 16 方向の視線**を持つペットです。背景透過・Codex v2 形式に対応しています。

## インストール

ターミナルで実行してください。

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash
```

**設定 → ペット → 更新**を開き、**艾雅法拉 · Eyjafjalla** を選択します。コマンドメニューまたは `/pet` からペットを呼び出せます。一覧に表示されない場合は、デスクトップアプリを再起動してください。項目名はアプリのバージョンによって異なる場合があります。[公式ガイド](https://learn.chatgpt.com/en/docs/pets)も参照できます。

カスタム **v2** ペットに対応した Codex デスクトップアプリが必要です。Bash インストーラーは macOS / Linux 向けで、`curl` と `shasum` または `sha256sum` を使用します。ファイルのインストールが成功しても、その環境でペット機能を利用できるとは限りません。本パッケージはデスクトップ用です。Web 版の 1536 × 1872 アップロード形式には対応せず、Web 版へ自動同期されません。

インストール先は `~/.codex/pets/eyjafjalla/` です。`CODEX_HOME` を設定している場合は `$CODEX_HOME/pets/eyjafjalla/` を使用します。`sudo`、Python、API キーは不要です。

<details>
<summary>スクリプトの確認・オフラインでのインストール・手動インストール</summary>

リポジトリを取得すると、スクリプトを確認してからローカルの素材をインストールできます。

```bash
git clone https://github.com/Rememorio/EyjafjallaCodexPet.git
cd EyjafjallaCodexPet
bash install.sh --source ./pets/eyjafjalla
```

手動の場合は、`pets/eyjafjalla/` フォルダー全体を Codex データディレクトリの `pets/` 内にコピーしてください。`pet.json` と `spritesheet.webp` は同じフォルダーに配置します。

確認済みのリビジョンを使うには、そのコミットの `install.sh` を取得し、`bash install.sh --ref <完全なコミットハッシュ>` を実行します。既存のブランチ名やタグ名も指定できます。

</details>

## アニメーション

| 動作 | 状態 |
| --- | --- |
| 待機・右移動・左移動 | 普段の待機や移動 |
| 手を振る・ジャンプ | 挨拶やお祝い |
| 失敗・入力待ち | タスクの問題や入力の待機 |
| 作業・レビュー | タスクの実行や結果の確認 |
| 16 方向の視線 | 方向に応じた視線とニュートラルな視線 |

各アニメーションの再生タイミングはデスクトップアプリが制御します。隣り合う視線の一部は変化が小さいため、アニメーションプレビューでご確認ください。

<p align="center">
  <img src="docs/previews/jumping.gif" width="192" height="208" alt="ジャンプ">
  <img src="docs/previews/running-right.gif" width="192" height="208" alt="右への移動">
</p>

[全アニメーションの一覧](docs/spritesheet-preview.png) · [16 方向の視線](docs/look-directions.png) · [状態の切り替え](docs/previews/state-transitions.gif)

## 更新とアンインストール

**更新：**インストールコマンドを再実行します。同じファイルは置き換えません。更新がある場合、元のフォルダー全体を Codex データディレクトリ内の `pet-backups/eyjafjalla.*/pet/` に保存し、保存先を表示します。ダウンロードやチェックサムの検証に失敗しても、既存のペットは保持されます。

**アンインストール：**

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash -s -- --uninstall
```

アンインストール時もバックアップを残します。復元する場合は、現在の `pets/eyjafjalla/` があれば別の場所に移し、バックアップ内の `pet/` をコピーして `eyjafjalla` に名前を変更してください。不要になったバックアップは手動で削除できます。

## 構成とコントリビューション

```text
pets/eyjafjalla/     インストール用パッケージと SHA-256 チェックサム
assets/reference/   元のキャラクター参考画像
docs/previews/      README 用アニメーション
docs/               スプライト一覧・視線一覧・開発ガイド
scripts/            パッケージの検証
tests/              インストール・更新・削除・復元のテスト
install.sh          インストーラー
```

アニメーションの修正、互換性の報告、翻訳の改善を歓迎します。検証方法は[開発ガイド](docs/development.md)をご覧ください。不具合を報告する際は OS、アプリのバージョン、再現手順を添え、個人のパスや機密情報は伏せてください。

## ライセンス

スクリプトと文書は [MIT ライセンス](LICENSE)で提供します。**キャラクター、美術素材、アニメーションは MIT の対象外です。** 詳細は[素材の権利について](ASSETS.md)をご確認ください。本プロジェクトは非公式のファン作品であり、『アークナイツ』および Codex の開発元・提供元とは関係ありません。
