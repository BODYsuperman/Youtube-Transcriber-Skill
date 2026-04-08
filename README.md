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

某些 YouTube 视频需要 cookies 才能下载。

**解决方案 1：使用 cookies**

1. 安装 Chrome 扩展：[Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

2. 访问 YouTube 并登录账号

3. 点击扩展图标 → Export cookies.txt

4. 保存 cookies.txt 到 `~/cookies.txt`

5. 使用 cookies 下载：
   ```bash
   python3 -m yt_dlp --cookies ~/cookies.txt "URL"
   ```

**解决方案 2：使用代理**

```bash
# HTTP 代理
python3 transcribe.py "URL" -p "http://proxy:port"

# SOCKS 代理
python3 transcribe.py "URL" -p "socks5://proxy:port"
```

### Q2: 转录太慢

**使用更小的模型：**

```python
# 修改 transcribe.py
model = WhisperModel('tiny')  # 最快（100MB）
# model = WhisperModel('base')  # 平衡（500MB）
```

**使用 GPU 加速（需要 NVIDIA）：**

```python
model = WhisperModel('tiny', device='cuda', compute_type='float16')
```

### Q3: 长视频超时

**使用后台运行模式：**

```bash
/tmp/start_transcribe.sh "URL" zh

# 监控进度
tail -f /tmp/transcribe_progress.log
```

**增加超时设置：**

```json
{
  "agents": {
    "defaults": {
      "timeoutSeconds": 3600
    }
  },
  "tools": {
    "timeout": 1800
  }
}
```

### Q4: 内存不足

**使用 tiny 模型（仅需 100MB）：**

```python
model = WhisperModel('tiny', device='cpu', compute_type='int8')
```

### Q5: 找不到结果文件

**检查临时文件：**

```bash
ls -lh /tmp/transcribe_*.json
ls -lh /tmp/transcript_*.txt
cat /tmp/transcribe_progress.log
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
