# YouTube Transcriber

> 🎯 一键转录 YouTube 视频，自动生成带时间戳的文字稿

**v2.0 新功能：** 后台运行，每 5 分钟更新进度！

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 快速开始

### 方法 1：OpenClaw（推荐）

```bash
/openclaw install youtube-transcribe
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
```

### 方法 2：直接从 GitHub（NPX）

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "URL"
```

### 方法 3：Python（手动安装）

```bash
git clone https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git
cd Youtube-Transcriber-Skill
./install.sh
python3 transcribe.py "URL"
```

---

## 📖 使用方法

### 基础用法

```bash
# 自动检测语言
python3 transcribe.py "URL"

# 指定语言
python3 transcribe.py "URL" zh    # 中文
python3 transcribe.py "URL" en    # 英文
```

### 后台运行（长视频推荐）

```bash
# 启动后台转录
/tmp/start_transcribe.sh "URL" zh

# 查看进度
tail -f /tmp/transcribe_progress.log

# 查看结果
cat /tmp/transcribe_result.json
```

---

## 🌐 支持的语言

| 代码 | 语言 |
|------|------|
| `auto` | 自动检测 |
| `zh` | 中文 |
| `en` | 英文 |
| `ja` | 日文 |
| `ko` | 韩文 |
| `es` | 西班牙文 |
| `fr` | 法文 |

---

## 📝 输出示例

```
📺 URL: https://youtube.com/watch?v=VIDEO_ID
🌐 Language: zh

[1/3] 下载音频...
✅ 下载成功

[2/3] 转录中...
📊 进度：16.7% (60.0s / 360.0s)
📊 进度：33.3% (120.0s / 360.0s)
📊 进度：50.0% (180.0s / 360.0s)
✅ 转录完成！

[3/3] 生成总结...
============================================================
# 视频转录总结

**URL:** https://youtube.com/watch?v=VIDEO_ID
**语言:** zh
**时长:** 6.0 分钟
**行数:** 180

## 转录内容
[0.00s -> 3.00s] 大家好...
[3.00s -> 5.00s] 今天我们来...
============================================================
```

---

## 📦 系统要求

| 要求 | 最低版本 |
|------|---------|
| Python | >= 3.8.0 |
| Node.js | >= 14.0.0 (NPX 方式) |

---

## 🔧 常见问题

### Q1: 下载失败（403 错误）

```bash
# 使用代理
python3 transcribe.py "URL" -p "http://proxy:port"
```

### Q2: 转录太慢

使用更小的模型（修改 `transcribe.py` 中的 `WhisperModel('tiny')`）

### Q3: 长视频超时

使用后台运行模式：

```bash
/tmp/start_transcribe.sh "URL" zh
```

---

## 📁 文件结构

```
Youtube-Transcriber-Skill/
├── README.md           # 使用说明
├── SKILL.md            # OpenClaw 技能描述
├── transcribe.py       # Python 主脚本（支持后台）
├── start_transcribe.sh # 后台启动脚本
├── package.json        # npm 配置
└── requirements.txt    # Python 依赖
```

---

## 🙏 感谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)

---

**⭐ 有用请给个 Star！**
