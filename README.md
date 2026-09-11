# 艾雅法拉 · Eyjafjalla

**让艾雅法拉陪你写代码。** 为 Codex 桌面应用制作的《明日方舟》同人宠物。

**简体中文** · [English](README.en.md) · [日本語](README.ja.md)

[![Validate](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml/badge.svg)](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml)
[![License: MIT — code & docs](https://img.shields.io/badge/code_%26_docs-MIT-blue.svg)](LICENSE)

<p align="center">
  <img src="docs/previews/idle.gif" width="192" height="208" alt="艾雅法拉轻轻呼吸，等待与你一起工作">
  <img src="docs/previews/waving.gif" width="192" height="208" alt="艾雅法拉挥手">
  <img src="docs/previews/look-loop.gif" width="192" height="208" alt="艾雅法拉环视不同方向">
</p>

棕色卷发、羊角、红色眼睛与红白裙装，保留熟悉的角色细节。包含 **9 组状态动画、16 个注视方向**和透明背景，采用 Codex v2 宠物格式。

## 一键安装

在终端运行：

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash
```

随后打开 **设置 → 宠物 → 刷新**，选择 **艾雅法拉 · Eyjafjalla**。可通过命令菜单或 `/pet` 唤出宠物。若列表没有更新，重启桌面应用再试。入口随应用版本可能不同，参见[官方宠物说明](https://learn.chatgpt.com/zh-Hans/docs/pets)。

需要支持自定义 **v2** 宠物的 Codex 桌面应用。安装脚本适用于 macOS / Linux 的 Bash 环境，依赖 `curl` 和 `shasum` 或 `sha256sum`；安装成功不代表当前平台或应用版本一定提供宠物功能。本包是桌面本地宠物，不适用于网页端的 1536 × 1872 上传格式，也不会自动同步到网页端。

默认安装到 `~/.codex/pets/eyjafjalla/`，设置了 `CODEX_HOME` 时使用 `$CODEX_HOME/pets/eyjafjalla/`。无需 `sudo`、Python 或 API 密钥。

<details>
<summary>先查看脚本、离线安装或手动安装</summary>

克隆后可先阅读脚本，再从本地素材安装：

```bash
git clone https://github.com/Rememorio/EyjafjallaCodexPet.git
cd EyjafjallaCodexPet
bash install.sh --source ./pets/eyjafjalla
```

手动安装时，将 `pets/eyjafjalla/` 整个文件夹复制到你的 Codex 数据目录下的 `pets/` 中。目录内的 `pet.json` 与 `spritesheet.webp` 必须放在一起。

也可以固定到自己已核验的提交：下载该提交的 `install.sh`，再执行 `bash install.sh --ref <完整提交哈希>`。`--ref` 同样接受已有分支或标签。

</details>

## 它会做什么

| 动作 | 对应状态 |
| --- | --- |
| 待机、向右走、向左走 | 平时陪伴与移动 |
| 挥手、跳跃 | 问候与庆祝 |
| 失败、等待 | 任务遇到问题或等待输入 |
| 工作、审查 | 执行任务与检查结果 |
| 16 向注视 | 跟随方向变化，另有中性视线帧 |

具体触发方式由桌面应用控制。部分相邻注视方向的差异较细微，适合在动画预览中观察。

<p align="center">
  <img src="docs/previews/jumping.gif" width="192" height="208" alt="跳跃动画">
  <img src="docs/previews/running-right.gif" width="192" height="208" alt="向右移动动画">
</p>

[查看完整动作图](docs/spritesheet-preview.png) · [查看 16 向注视图](docs/look-directions.png) · [查看状态切换](docs/previews/state-transitions.gif)

## 更新与卸载

**更新：**重新运行安装命令即可。相同版本不会重复安装；有变化时，旧目录会完整备份到 Codex 数据目录的 `pet-backups/eyjafjalla.*/pet/`，具体位置会在终端打印。下载或校验失败不会覆盖现有宠物。

**卸载：**

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash -s -- --uninstall
```

卸载同样保留备份。需要恢复时，先移走当前 `pets/eyjafjalla/`（如有），再把备份中的 `pet/` 复制回去并命名为 `eyjafjalla`。确认不再需要旧版本后，可以自行删除对应备份。

## 仓库结构与贡献

```text
pets/eyjafjalla/     可直接安装的宠物包与 SHA-256 校验清单
assets/reference/   原始角色参考图
docs/previews/      README 动画预览
docs/               精灵图预览、注视图和开发说明
scripts/            宠物包校验
tests/              安装、更新、卸载及失败恢复测试
install.sh          安装入口
```

欢迎提交动画修正、安装兼容性反馈和翻译改进。开发与验证方式见[开发说明](docs/development.md)；反馈问题时请附上系统、应用版本和复现步骤，隐藏个人路径及敏感信息。

## 许可与声明

脚本和文档采用 [MIT 许可证](LICENSE)。**角色、美术及动画素材不在 MIT 授权范围内**，详见[素材权利说明](ASSETS.md)。本项目是非官方同人作品，与《明日方舟》及 Codex 的开发或发行方无隶属关系。
