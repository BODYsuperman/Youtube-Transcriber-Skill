# YouTube Transcriber Skill

> 🎯 自动转录任何 YouTube 视频，生成带时间戳的文字稿和结构化总结

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ 功能特点

- ✅ **自动下载** - 自动从 YouTube 下载音频
- ✅ **语音识别** - 使用 Whisper AI 进行高精度转录
- ✅ **多语言支持** - 自动检测或手动指定语言（中文/英文/日文/韩文等）
- ✅ **时间戳** - 每行文字带精确时间戳
- ✅ **结构化总结** - 自动生成视频摘要和关键要点
- ✅ **本地运行** - 所有处理在本地完成，保护隐私

---

## 🚀 快速开始

### 方法 1：使用 NPX（推荐，无需安装）

```bash
# 一行命令即可使用
npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"

# 指定语言
npx youtube-transcribe "URL" zh      # 中文
npx youtube-transcribe "URL" en      # 英文
npx youtube-transcribe "URL" auto    # 自动检测
```

**优点：**
- ✅ 无需克隆仓库
- ✅ 无需安装依赖
- ✅ 随时随地使用
- ✅ 自动处理依赖

**要求：**
- Node.js >= 14.0.0
- Python >= 3.8.0

---

### 方法 2：克隆仓库（适合开发者）

### 1. 环境要求

| 要求 | 最低配置 | 推荐配置 |
|------|---------|---------|
| **系统** | Linux/Windows/Mac | Linux (NAS) |
| **Python** | 3.8+ | 3.10+ |
| **CPU** | 4 核心 | 8 核心+ |
| **内存** | 4GB | 8GB+ |
| **存储** | 10GB 可用 | 50GB+ |

### 2. 安装依赖（仅方法 2 需要）

```bash
# 安装 yt-dlp（YouTube 下载工具）
pip3 install --user --break-system-packages yt-dlp

# 安装 faster-whisper（语音识别）
pip3 install --user --break-system-packages faster-whisper

# 验证安装
python3 -m yt_dlp --version
python3 -c "from faster_whisper import WhisperModel; print('Whisper OK!')"
```

### 3. 克隆仓库（仅方法 2）

```bash
git clone https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git
cd Youtube-Transcriber-Skill
```

---

## 📖 使用方法

### NPX 方式（推荐）

```bash
# 自动检测语言
npx youtube-transcribe "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定语言
npx youtube-transcribe "URL" zh      # 中文
npx youtube-transcribe "URL" en      # 英文
npx youtube-transcribe "URL" ja      # 日文
npx youtube-transcribe "URL" ko      # 韩文
```

### Python 方式

```bash
# 自动检测语言
python3 transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定语言
python3 transcribe.py "URL" zh      # 中文
python3 transcribe.py "URL" en      # 英文
python3 transcribe.py "URL" ja      # 日文
python3 transcribe.py "URL" ko      # 韩文
```

### 输出示例

```
📺 URL: https://www.youtube.com/watch?v=jNQXAC9IVRw
🌐 Language: auto

[1/3] 下载音频...
✅ 下载成功

[2/3] 转录中...
✅ 转录完成！语言：en

[3/3] 生成总结...

============================================================
# 视频转录总结

**URL:** https://www.youtube.com/watch?v=jNQXAC9IVRw
**语言:** en
**行数:** 4

## 转录内容

[0.00s -> 4.00s]  Alright, so here we are, one of the elephants.
[4.00s -> 12.00s]  The cool thing about these guys is that they have really long trunks.
[12.00s -> 14.00s]  And that's cool.
[14.00s -> 19.00s]  And that's pretty much all there is to say.
============================================================
```

---

## ⚙️ 高级选项

### 使用不同模型

| 模型 | 速度 | 精度 | 内存 | 适用场景 |
|------|------|------|------|---------|
| `tiny` | ⚡⚡⚡ | ⭐⭐ | 100MB | 快速转录 |
| `base` | ⚡⚡ | ⭐⭐⭐ | 500MB | 平衡选择 |
| `small` | ⚡ | ⭐⭐⭐⭐ | 1GB | 高质量 |
| `medium` | 🐌 | ⭐⭐⭐⭐⭐ | 2GB | 专业需求 |

```bash
# 使用 base 模型（更高精度）
python3 transcribe.py "URL" -m base

# 使用 tiny 模型（更快速度）
python3 transcribe.py "URL" -m tiny
```

### 保存到文件

```bash
# 输出到文件
python3 transcribe.py "URL" -o output.txt

# 后台运行（长视频）
nohup python3 transcribe.py "URL" > transcribe.log 2>&1 &
```

### 使用代理

```bash
# 如果无法访问 YouTube
python3 transcribe.py "URL" -p "http://proxy:port"
```

---

## 📁 文件结构

```
Youtube-Transcriber-Skill/
├── README.md              # 使用说明
├── transcribe.py          # 主脚本
├── transcribe_local.py    # 备用脚本
├── SKILL.md              # OpenClaw 技能描述
├── requirements.txt       # Python 依赖
└── examples/             # 示例输出
    └── sample_output.txt
```

---

## 🔧 故障排除

### 问题 1：下载失败（403 错误）

```
ERROR: unable to download video data: HTTP Error 403: Forbidden
```

**解决方案：**

```bash
# 方案 1：使用代理
python3 transcribe.py "URL" -p "http://proxy:port"

# 方案 2：更新 yt-dlp
pip3 install --upgrade yt-dlp

# 方案 3：使用 cookies
python3 -m yt_dlp --cookies cookies.txt "URL"
```

### 问题 2：转录太慢

**解决方案：**

```bash
# 使用更小的模型
python3 transcribe.py "URL" -m tiny

# 或使用 GPU（如果有 NVIDIA 显卡）
# 修改 transcribe.py 中的模型加载：
# model = WhisperModel('base', device='cuda', compute_type='float16')
```

### 问题 3：内存不足

```
Killed
```

**解决方案：**

```bash
# 使用 tiny 模型（仅需 100MB 内存）
python3 transcribe.py "URL" -m tiny
```

### 问题 4：无法访问 YouTube

```bash
# 检查网络
ping youtube.com

# 使用代理
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 或使用 DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

---

## 📊 性能基准

**40 分钟视频转录时间：**

| 模型 | NAS (4 核) | 本地电脑 (8 核) |
|------|-----------|---------------|
| `tiny` | 24 分钟 | 10 分钟 |
| `base` | 45 分钟 | 20 分钟 |
| `small` | 90 分钟 | 40 分钟 |

---

## 🎯 实际案例

### 案例 1：40 分钟政治分析视频

```
输入：https://www.youtube.com/watch?v=Mm-Jeaf1M_g
视频时长：40 分钟
转录时间：24 分钟
输出行数：910 行
文件大小：54KB
语言：中文
```

### 案例 2：9.5 分钟投资分享视频

```
输入：https://www.youtube.com/watch?v=9uDH8z-HZKs
视频时长：9.5 分钟
转录时间：18 分钟
输出行数：219 行
文件大小：13KB
语言：中文
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube 下载工具
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Whisper 语音识别
- [OpenAI Whisper](https://github.com/openai/whisper) - 原始 Whisper 模型

---

## 📬 联系方式

- **作者：** Alex Bloomberg
- **项目：** [Youtube-Transcriber-Skill](https://github.com/BODYsuperman/Youtube-Transcriber-Skill)
- **问题反馈：** [GitHub Issues](https://github.com/BODYsuperman/Youtube-Transcriber-Skill/issues)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
