# 开发与验证

[返回首页](../README.md) · [English README](../README.en.md) · [日本語 README](../README.ja.md)

发布入口是 `pets/eyjafjalla/`。宠物 ID 和安装目录固定为 `eyjafjalla`，显示名可以本地化；重命名 ID 会使已安装用户得到另一个宠物。

## 文件约定

`pet.json` 使用 `spriteVersionNumber: 2`，通过同目录的 `spritesheet.webp` 加载图集。图集为 **1536 × 2288** 的透明 RGBA WebP，8 列 × 11 行，每格 192 × 208。坐标从 0 开始。

| 行 | 状态 | 有效帧 |
| --- | --- | --- |
| 0 | idle | 第 0–5 列；第 6 列为专用中性视线帧 |
| 1 | running-right | 8 |
| 2 | running-left | 8 |
| 3 | waving | 4 |
| 4 | jumping | 5 |
| 5 | failed | 8 |
| 6 | waiting | 6 |
| 7 | running | 6 |
| 8 | reviewing | 6 |
| 9 | look | 0°–157.5°，间隔 22.5° |
| 10 | look | 180°–337.5°，间隔 22.5° |

注视角度以屏幕坐标为准：0° 向上，90° 向右，180° 向下，270° 向左。未使用的单元格保持完全透明，不要重复填充。保持角色比例、站立基线、轮廓留白和透明边缘一致。

`assets/reference/eyjafjalla.png` 保存原始参考图；`docs/previews/` 保存展示动画。临时生成文件和本地 QA 记录放在被 Git 忽略的 `output/` 中。不要把个人路径、环境配置或会话记录放入发布文件。

`assets/reference/eyjafjalla-chibi.png` 是动画的统一造型参考。保持分组卷发、清楚的轮廓与少量平涂层次，避免每帧发丝、衣褶和高光各自变化。动作要由重心、手脚和头部共同完成，发梢与衣摆随后收住；不要只替换表情或平移整张站姿图。站立角色周围应留出运动空间，跳跃时保持头身尺度，通过屈膝和真实位移腾空。

## 运行验证

开发环境需要 Python 3.10+、Bash 和 Pillow。安装宠物本身不需要 Python。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/render_previews.py
bash -n install.sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

校验脚本检查元数据、SHA-256、图集尺寸、74 个有效单元格、透明空格与边缘裁切；跳跃入场和落地的站立轮廓与 idle 的宽高差不得超过 5%，脚底基线差不得超过 2 像素。透明像素的 RGB 必须为零，Pillow 导出时使用 `lossless=True, exact=True`。安装测试使用临时目录，覆盖首次安装、重复安装、更新备份、损坏文件、下载失败、符号链接、并发锁、卸载和替换失败回滚。GitHub Actions 在 macOS 与 Ubuntu 上运行这些检查。

这些检查不能代替视觉审查。修改动画后还需检查循环接缝、角色一致性、左右移动的双腿交替与前脚通过姿态、全部 16 个注视方向以及浅色、深色背景上的透明边缘，并同步更新预览图。

配色以 idle 为基准：头发保持柔和粉棕，肤色保持浅粉象牙色，靴子与服装暗部保持灰紫棕。比较同一材质的受光部位，不要用整帧平均颜色来校正侧身与正面。校验脚本逐格抽取发顶不透明中间色，要求相对 idle 的 CIELAB L* 亮度差不超过 2，HSV 饱和度差不超过 0.025；逐格检查可发现整行平均值掩盖的单帧色闪。仅比较饱和度无法发现悬停变暗，仍需目视确认肤色、服装和局部阴影。

`scripts/palette.py` 用已确认的 idle 色阶校准头发中间色与阴影，保留 alpha、眼睛、肤色和服装。材质识别针对本角色，不适用于任意宠物。校色前保留输入版本，每次从原始输入处理，避免反复叠加；校色后检查浅色、深色背景上的发丝边界及未修改材质。

```bash
python scripts/palette.py input.webp --reference approved.webp \
  --output calibrated.webp --report output/palette-report.json
```

左右移动应是轻柔的小步走。除完整换腿外，还要检查低位经过的脚、自然摆臂、头身轻微起伏和短步幅；动作技术上完整，不代表观感自然。需要镜像另一方向时，先确认没有文字、单侧道具或必须保留位置的非对称细节，并按帧镜像，保持帧顺序。

## 预览质量与播放限制

`scripts/render_previews.py` 从安装图直接导出无损 APNG，保留完整 RGBA，不做调色板量化、锐化、补帧或二次缩放。README 用 96 × 104 CSS 像素显示 192 × 208 的源图，适合 2 倍像素密度屏幕；不要将小图放大成模糊的展示图。

透明 GIF 只有全透明和不透明两种状态，无法准确保留插画的半透明边缘。改用 APNG 后，`tests/test_previews.py` 会逐帧核对像素、帧数和播放时间，防止预览与实际宠物脱节。

当前桌面实现固定 v2 的图集尺寸、状态帧数和时长。跑动前 7 帧各 120 ms，最后一帧 220 ms；跳跃前 4 帧各 140 ms，最后一帧 280 ms。不能通过在 `pet.json` 中增加帧数或把预览改成更高帧率来改变运行时表现。跑动的末帧应设计为能短暂停留的落脚姿势，跳跃末帧应稳定落地。

待机 6 帧的实际时长为 1680、660、660、840、840、1920 ms，整轮 6.6 秒。客户端统一将待机放慢 6 倍，宠物元数据不能单独覆盖眨眼时长。待机因此保持睁眼，以呼吸和发梢微动表现生命感；不要在这些长帧中安排半闭眼或闭眼。等待、工作和检查等状态可在各自 120–150 ms 的短帧中闭眼，避免把闭眼放在较长的末帧。预览必须保留客户端时序，不能单独加速来掩盖实际播放问题。

16 向注视由鼠标控制；README 中每方向 180 ms 的自动循环仅用于演示方向序列。

还要检查 **idle → 每个动作 → idle** 的切换，尤其是鼠标悬停时的跳跃。逐行循环正常，不代表跨状态没有大小跳变。对比头脸、躯干和服装尺寸，不要仅看总包围框：屈膝、转身和低头本来就会改变轮廓。跳跃应通过屈膝和位移表现，不能为了在单元格里腾出高度而缩小整个人物。

可执行 `python scripts/render_previews.py --transition-dir output/transitions`，导出待机、动作播放三轮、回到待机的完整序列，逐帧检查进出状态时的脸型、手臂与站姿。跳跃的五帧需要包含蓄力、腾空、落地缓冲和站稳；末帧的 280 ms 停留应留给自然站姿。等待、工作与检查状态的手腕应与前臂自然连接，手部不要与领结挤在一起，也不要依赖细碎的手指动作表达状态。

鼠标在跳跃中途移开时，桌面应用会立即切换回当前状态，不会等待落地帧。图集只能改善完整动作的进出姿态，无法为这种中断添加过渡帧；验证时需要区分正常播放结束与鼠标提前移开。

## 更新校验清单

修改宠物包后，在仓库根目录执行：

```bash
python - <<'PY'
import hashlib
from pathlib import Path
bundle = Path('pets/eyjafjalla')
names = ('pet.json', 'spritesheet.webp')
(bundle / 'checksums.sha256').write_text(''.join(
    f'{hashlib.sha256((bundle / name).read_bytes()).hexdigest()}  {name}\n'
    for name in names
))
PY
```

校验清单用于发现传输损坏和不一致，不是独立的来源签名。安装器仅处理两个固定文件名；更新前先校验暂存文件，通过后再备份并替换旧目录。

提交变更时请保持三份 README 的安装命令和功能描述一致，说明验证结果。图片不属于 MIT 授权范围；新增素材需核实权利并同步更新[素材说明](../ASSETS.md)。
