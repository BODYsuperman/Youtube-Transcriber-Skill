# YouTube Transcriber

> 🎯 一键转录 YouTube 视频，自动生成带时间戳的文字稿

---

## 🚀 快速开始

### 方法 1：NPX（最简单）

```bash
npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
```

### 方法 2：Python

```bash
git clone https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git
cd Youtube-Transcriber-Skill
pip3 install -r requirements.txt
python3 transcribe.py "URL"
```

---

## 📖 使用方法

### NPX 方式

```bash
# 自动检测语言
npx youtube-transcribe "URL"

# 指定语言
npx youtube-transcribe "URL" zh    # 中文
npx youtube-transcribe "URL" en    # 英文
```

### Python 方式

```bash
python3 transcribe.py "URL"
python3 transcribe.py "URL" zh
```

---

## 📦 系统要求

| 要求 | 最低版本 |
|------|---------|
| Node.js | >= 14.0.0 |
| Python | >= 3.8.0 |

---

## 📝 输出示例

```
📺 URL: https://youtube.com/watch?v=VIDEO_ID
🌐 Language: zh

[1/3] 下载音频...
✅ 下载成功

[2/3] 转录中...
✅ 转录完成！

[3/3] 生成总结...
============================================================
# 视频转录总结

**URL:** https://youtube.com/watch?v=VIDEO_ID
**语言:** zh

## 转录内容
[0.00s -> 3.00s] 大家好...
[3.00s -> 5.00s] 今天我们来...
============================================================
```

---

## 🔧 常见问题

### 下载失败

```bash
# 使用代理
npx youtube-transcribe "URL" -p "http://proxy:port"
```

### 转录太慢

使用更小的模型（修改 `transcribe.py` 中的 `WhisperModel('tiny')`）

---

## 📁 文件结构

```
Youtube-Transcriber-Skill/
├── README.md           # 使用说明
├── package.json        # npm 配置
├── requirements.txt    # Python 依赖
├── transcribe.py       # Python 脚本
└── bin/
    └── transcribe.js   # NPX 入口
```

---

## 🙏 感谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)

---

**⭐ 有用请给个 Star！**
