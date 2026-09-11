# 艾雅法拉 · Eyjafjalla

把艾雅法拉接到你的桌面上。

《明日方舟》艾雅法拉的非官方 Codex 宠物。会望向鼠标、挥手、小跳，也会在你工作时安静陪伴。

<p align="center">
  <img src="docs/previews/look-loop.png" width="96" height="104" alt="Eyjafjalla">
</p>

[![Validate](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml/badge.svg)](https://github.com/Rememorio/EyjafjallaCodexPet/actions/workflows/validate.yml) [![Pet v2](https://img.shields.io/badge/Codex_Pet-v2-f2a1a8)](pets/eyjafjalla/pet.json) [![License: MIT — code & docs](https://img.shields.io/badge/code_%26_docs-MIT-blue.svg)](LICENSE)

## 安装

在终端粘贴这一行，无需克隆仓库：

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash
```

安装后打开 <strong>设置 → 宠物 → 刷新</strong>，选择 <strong>艾雅法拉 · Eyjafjalla</strong>。通过命令菜单或 `/pet` 唤出；如果还显示旧效果，重新选择宠物或重启应用。

需要支持自定义 v2 宠物的 Codex 桌面版本。脚本适用于 macOS / Linux 的 Bash 环境，使用 `curl` 与系统自带的 SHA-256 工具，无需 `sudo`、Python 或 API 密钥。

## 在桌面上陪你

9 组状态动画，另有 16 个方向的头眼跟随。下面直接展示宠物包里的真实帧与播放节奏。

<table>
<tr>
<td align="center" width="240"><strong>待机</strong><br><img src="docs/previews/idle.png" width="96" height="104" alt="待机"></td>
<td align="center" width="240"><strong>向右移动</strong><br><img src="docs/previews/running-right.png" width="96" height="104" alt="向右移动"></td>
<td align="center" width="240"><strong>向左移动</strong><br><img src="docs/previews/running-left.png" width="96" height="104" alt="向左移动"></td>
</tr>
<tr>
<td align="center" width="240"><strong>挥手</strong><br><img src="docs/previews/waving.png" width="96" height="104" alt="挥手"></td>
<td align="center" width="240"><strong>小跳</strong><br><img src="docs/previews/jumping.png" width="96" height="104" alt="小跳"></td>
<td align="center" width="240"><strong>失落</strong><br><img src="docs/previews/failed.png" width="96" height="104" alt="失落"></td>
</tr>
<tr>
<td align="center" width="240"><strong>等待回应</strong><br><img src="docs/previews/waiting.png" width="96" height="104" alt="等待回应"></td>
<td align="center" width="240"><strong>认真工作</strong><br><img src="docs/previews/running.png" width="96" height="104" alt="认真工作"></td>
<td align="center" width="240"><strong>检查结果</strong><br><img src="docs/previews/review.png" width="96" height="104" alt="检查结果"></td>
</tr>
</table>

鼠标移到不同位置时，她会转头看向你；悬停时轻轻小跳。工作、等待与完成时的状态切换由 Codex 控制。预览使用无损 APNG，保留半透明边缘，在浅色、深色主题下都可显示。

## 更新与卸载

<strong>更新</strong>：重新执行安装命令。同版本不重复替换；新版本会先校验，再备份旧目录并安装。安装器会打印备份位置。

<strong>卸载</strong>：

```bash
curl -fsSL https://raw.githubusercontent.com/Rememorio/EyjafjallaCodexPet/main/install.sh | bash -s -- --uninstall
```

默认目录是 `~/.codex/pets/eyjafjalla/`；设置 `CODEX_HOME` 时使用对应目录。卸载也会保留旧宠物，便于恢复。离线安装、固定版本和恢复方法见[安装说明](docs/installation.md)。

## 参与改进

欢迎反馈不自然的动作、安装问题或翻译建议。提交 Issue 时请说明系统、Codex 版本、触发方式，并附上有问题的动作或方向。宠物包位于 `pets/eyjafjalla/`，开发与验收规则见[开发说明](docs/development.md)。

## 许可

脚本与文档采用 [MIT](LICENSE)。角色、美术和动画素材不属于 MIT 授权范围，详见[素材权利说明](ASSETS.md)。本项目为非官方同人作品，与《明日方舟》及 Codex 的开发、发行方无隶属或背书关系。

---

[English](README.en.md) · [日本語](README.ja.md)
