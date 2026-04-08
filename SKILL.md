---
name: youtube-transcribe
description: YouTube 视频自动转录工具，支持后台运行、进度更新、多语言识别
version: 2.1.0
author: Alex Bloomberg
tags: [youtube, transcribe, whisper, ai, subtitle, background, multi-language]
---

# YouTube Transcriber Skill

自动转录 YouTube 视频，生成带时间戳的文字稿和结构化总结。

## 核心功能

- ✅ **自动下载** - 使用 yt-dlp 下载音频
- ✅ **语音识别** - Whisper AI 高精度转录
- ✅ **多语言支持** - 自动检测或手动指定（zh/en/ja/ko 等）
- ✅ **后台运行** - 关闭终端不影响转录
- ✅ **进度更新** - 每 5 分钟自动更新进度
- ✅ **结果保存** - JSON + TXT 双格式输出
- ✅ **超时保护** - 支持 60 分钟超时设置

## 使用方法

### 方法 1：OpenClaw 中使用

```bash
# 基础用法
/youtube-transcribe <URL> [language]

# 例子
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" zh
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" en
```

### 方法 2：后台运行（推荐长视频）

```bash
# 启动后台转录
/tmp/start_transcribe.sh "URL" zh

# 查看进度
tail -f /tmp/transcribe_progress.log

# 查看结果
cat /tmp/transcribe_result.json
```

### 方法 3：直接 Python 调用

```bash
python3 /tmp/transcribe_background.py "URL" zh
```

## 参数说明

| 参数 | 说明 | 默认值 | 必填 |
|------|------|--------|------|
| URL | YouTube 视频链接 | - | ✅ |
| language | 语言代码 | auto | ❌ |

### 支持的语言代码

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| `auto` | 自动检测 | `ja` | 日文 |
| `zh` | 中文 | `ko` | 韩文 |
| `en` | 英文 | `es` | 西班牙文 |
| `fr` | 法文 | `de` | 德文 |

## 处理流程

```
┌─────────────────────────────────────────────────────────────┐
│                    用户发起请求                               │
│          /youtube-transcribe "URL" zh                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 1: 下载音频 (约 2 分钟)                                  │
│  - 使用 yt-dlp 下载最佳音频格式                              │
│  - 保存到临时目录                                            │
│  - 超时保护：600 秒                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 2: Whisper 转录 (视频时长的 0.6-1 倍)                     │
│  - 加载 Whisper tiny 模型 (100MB)                            │
│  - 语音识别 + 时间戳生成                                     │
│  - 每 5 分钟更新进度                                         │
│  - 超时保护：1800 秒                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 3: 生成总结 (约 1 分钟)                                  │
│  - 结构化 JSON 输出                                          │
│  - 保存 TXT 完整转录                                         │
│  - 清理临时文件                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    返回结果                                  │
│  - /tmp/transcribe_result.json (JSON 总结)                  │
│  - /tmp/transcript_*.txt (完整转录)                         │
│  - /tmp/transcribe_progress.log (进度日志)                  │
└─────────────────────────────────────────────────────────────┘
```

## 输出示例

### JSON 结果

```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "language": "zh",
  "duration_minutes": 29.2,
  "line_count": 356,
  "transcript": [
    {"start": 0.0, "end": 2.56, "text": "朋友们好..."},
    ...
  ]
}
```

### 进度日志

```
[2026-04-08 13:56:09] 📺 开始处理：https://youtube.com/watch?v=...
[2026-04-08 13:56:09] 🌐 语言：zh
[2026-04-08 13:56:09] [1/3] 开始下载音频...
[2026-04-08 13:57:47] ✅ 下载成功
[2026-04-08 13:57:47] [2/3] 开始转录...
[2026-04-08 14:02:47] 📊 进度：16.7% (300.0s / 1800.0s)
[2026-04-08 14:07:47] 📊 进度：33.3% (600.0s / 1800.0s)
[2026-04-08 14:12:47] 📊 进度：50.0% (900.0s / 1800.0s)
[2026-04-08 14:17:47] ✅ 转录完成！语言：zh
[2026-04-08 14:17:47] [3/3] 生成总结...
[2026-04-08 14:18:47] ✅ 完成！
```

## 性能参考

| 视频时长 | 下载时间 | 转录时间 | 总耗时 |
|---------|---------|---------|--------|
| 10 分钟 | ~1 分钟 | ~6-10 分钟 | ~10 分钟 |
| 30 分钟 | ~2 分钟 | ~18-30 分钟 | ~25 分钟 |
| 60 分钟 | ~3 分钟 | ~36-60 分钟 | ~45 分钟 |

## 依赖要求

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.8.0 | 运行环境 |
| yt-dlp | latest | YouTube 下载 |
| faster-whisper | >= 1.0.0 | 语音识别 |

## 文件说明

| 文件 | 路径 | 说明 |
|------|------|------|
| `transcribe.py` | `/tmp/Youtube-Transcriber-Skill/` | 主脚本 |
| `transcribe_background.py` | `/tmp/` | 后台运行脚本 |
| `start_transcribe.sh` | `/tmp/` | 启动脚本 |
| 进度日志 | `/tmp/transcribe_progress.log` | 实时进度 |
| 结果文件 | `/tmp/transcribe_result.json` | JSON 结果 |
| 完整转录 | `/tmp/transcript_*.txt` | TXT 转录 |

## 常见问题

### Q1: 下载失败（403 错误）

```bash
# 使用代理
python3 transcribe.py "URL" -p "http://proxy:port"
```

### Q2: 转录太慢

使用更小的模型（修改脚本中的 `WhisperModel('tiny')`）

### Q3: 长视频超时

使用后台运行模式：`/tmp/start_transcribe.sh "URL" zh`

### Q4: 找不到语言

确保安装了 faster-whisper：`pip3 install faster-whisper`

## 许可证

MIT License
