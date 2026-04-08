---
name: youtube-transcribe
description: 自动转录 YouTube 视频，每 5 分钟更新进度，完成后生成带时间戳的文字稿和总结
version: 2.0.0
author: Alex Bloomberg
tags: [youtube, transcribe, whisper, ai, subtitle, background]
---

# YouTube Transcriber Skill

自动转录 YouTube 视频，生成带时间戳的文字稿和结构化总结。

**v2.0 新功能：**
- ✅ 后台运行，关闭终端不影响
- ✅ 每 5 分钟自动更新进度
- ✅ 完成后自动保存结果

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

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| URL | YouTube 视频链接 | 必填 |
| language | 语言代码 (zh/en/ja/ko/auto) | auto |

## 语言代码

| 代码 | 语言 |
|------|------|
| `auto` | 自动检测 |
| `zh` | 中文 |
| `en` | 英文 |
| `ja` | 日文 |
| `ko` | 韩文 |

## 例子

### 基础用法

```bash
# 自动检测语言
/youtube-transcribe "https://youtube.com/watch?v=jNQXAC9IVRw"

# 指定中文
/youtube-transcribe "https://youtube.com/watch?v=9uDH8z-HZKs" zh

# 指定英文
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" en
```

### 后台运行（长视频推荐）

```bash
# 启动后台转录
/tmp/start_transcribe.sh "https://youtube.com/watch?v=LONG_VIDEO" zh

# 另开终端监控进度
tail -f /tmp/transcribe_progress.log

# 等待完成后查看结果
cat /tmp/transcribe_result.json
```

## 输出示例

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
...
============================================================
```

## 后台运行功能

### 启动脚本

```bash
# 位置：/tmp/start_transcribe.sh
# 用法：./start_transcribe.sh "URL" [language]
```

### 进度更新

- 每 5 分钟自动更新进度
- 日志文件：`/tmp/transcribe_progress.log`
- 结果文件：`/tmp/transcribe_result.json`

### 监控命令

```bash
# 实时查看进度
tail -f /tmp/transcribe_progress.log

# 查看最新 20 行
tail -n 20 /tmp/transcribe_progress.log

# 查看结果
cat /tmp/transcribe_result.json | python3 -m json.tool
```

## 性能参考

| 视频时长 | 转录时间 | 进度更新次数 |
|---------|---------|-------------|
| 10 分钟 | ~10 分钟 | 2 次 |
| 30 分钟 | ~30 分钟 | 6 次 |
| 60 分钟 | ~60 分钟 | 12 次 |

## 依赖

- Python >= 3.8.0
- yt-dlp
- faster-whisper

## 文件说明

| 文件 | 说明 |
|------|------|
| `transcribe.py` | 主脚本（支持后台） |
| `start_transcribe.sh` | 后台启动脚本 |
| `/tmp/transcribe_progress.log` | 进度日志 |
| `/tmp/transcribe_result.json` | 结果文件 |
| `/tmp/transcript_*.txt` | 完整转录 |

## 许可证

MIT License
