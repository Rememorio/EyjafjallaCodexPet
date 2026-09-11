# 安装选项 / Installation options / インストールの詳細

[中文](../README.md) · [English](../README.en.md) · [日本語](../README.ja.md)

## 离线安装 / Local installation

克隆仓库后，可以先阅读 `install.sh`，再从本地素材安装。The local bundle needs no network access during installation. ローカルの素材から導入できます。

```bash
git clone https://github.com/Rememorio/EyjafjallaCodexPet.git
cd EyjafjallaCodexPet
bash install.sh --source ./pets/eyjafjalla
```

手动安装时，把 `pets/eyjafjalla/` 整个文件夹复制到 Codex 数据目录的 `pets/` 下。Keep `pet.json` and `spritesheet.webp` together. 2 つのファイルは同じフォルダーに置いてください。

## 固定版本 / Pin a revision

下载已核验提交中的 `install.sh`，并使用同一提交哈希：Download the installer from a reviewed commit and pass the same revision. 確認済みのコミットからスクリプトを取得し、同じハッシュを指定します。

```bash
bash install.sh --ref <full-commit-hash>
```

`--ref` 也接受已有分支或标签。Existing branches and tags are supported. 既存のブランチやタグも指定できます。

## 备份与恢复 / Recovery

更新、卸载都会将旧目录移到 Codex 数据目录下的 `pet-backups/eyjafjalla.*/pet/`。安装器打印确切路径。

要恢复旧版，先移开当前 `pets/eyjafjalla/`（如有），再把备份的 `pet/` 复制回来并改名为 `eyjafjalla`，然后刷新宠物列表。确认不再需要后，可自行删除旧备份。

Updates and uninstalls preserve the entire previous directory under `pet-backups/eyjafjalla.*/pet/`. To restore it, move the current installation aside, copy the backup's `pet/` into `pets/` as `eyjafjalla`, and refresh the app. Delete old backups when no longer needed.

更新・削除時には旧フォルダー全体を保存します。復元するには現在のペットを別の場所へ移し、バックアップの `pet/` を `pets/eyjafjalla/` としてコピーして、一覧を更新してください。不要なバックアップは手動で削除できます。

## 兼容性 / Compatibility

- 本包是桌面本地 v2 宠物，图集为 1536 × 2288；网页上传要求的 1536 × 1872 格式不同，不能直接上传，也不会自动同步。
- This is a local desktop v2 bundle. It does not fit the web uploader's 1536 × 1872 format and does not sync automatically to the web.
- デスクトップ用の v2 パッケージです。Web 版のアップロード形式とは異なり、自動同期されません。

## 常见问题 / Troubleshooting

<strong>安装后未出现或仍显示旧动画：</strong>刷新宠物列表、重新选择，再尝试重启支持 v2 的桌面应用。Refresh the pets list, reselect the pet, or restart a v2-compatible desktop app. 一覧を更新して選び直すか、アプリを再起動してください。

<strong>校验失败：</strong>本次安装不会覆盖现有宠物。稍后重试；仓库刚更新时，静态下载缓存可能短暂不一致。A failed checksum leaves the current pet intact. Retry after the download cache refreshes. 検証に失敗した場合は既存のペットを保持します。少し待って再試行してください。

<strong>为什么不能直接换成更大的图：</strong>当前 v2 格式固定 192 × 208 像素一格、8 列 × 11 行。单纯放大或追加帧不属于兼容格式。Current v2 cells and frame counts are fixed; upscaling the atlas or adding frames is not a compatible format. 現行の v2 形式ではセルの大きさとフレーム数が固定されています。
