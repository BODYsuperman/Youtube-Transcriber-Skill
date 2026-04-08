# YouTube Transcriber Skill 架构文档

## 📊 完整系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         用户交互层                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │  OpenClaw   │  │ 命令行调用   │  │  后台脚本    │                     │
│  │  /youtube-  │  │  python3    │  │  start_     │                     │
│  │  transcribe │  │  transcribe │  │  transcribe │                     │
│  │             │  │  .py        │  │  .sh        │                     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                     │
└─────────┼────────────────┼────────────────┼────────────────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      核心处理层 (transcribe_background.py)              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. log() - 日志记录函数                                         │   │
│  │     - 写入 /tmp/transcribe_progress.log                         │   │
│  │     - 每 5 分钟更新进度                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  2. save_result() - 结果保存函数                                 │   │
│  │     - 写入 /tmp/transcribe_result.json                          │   │
│  │     - JSON 格式结构化数据                                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  3. download_audio() - 下载函数                                  │   │
│  │     - 调用 yt-dlp                                               │   │
│  │     - 下载最佳音频格式                                          │   │
│  │     - 保存到临时目录                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  4. transcribe_audio() - 转录函数                                │   │
│  │     - 加载 Whisper tiny 模型                                      │   │
│  │     - 语音识别 + 时间戳生成                                      │   │
│  │     - 每 5 分钟更新进度                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  5. generate_summary() - 总结函数                                │   │
│  │     - 生成结构化 JSON                                           │   │
│  │     - 包含前 50 行转录                                            │   │
│  │     - 元数据（时长、行数、语言）                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         外部依赖层                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │   YouTube   │  │   yt-dlp    │  │  Whisper    │                     │
│  │   视频源    │  │  下载工具   │  │  AI 模型     │                     │
│  └─────────────┘  └─────────────┘  └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 数据处理流程

```
┌─────────────────────────────────────────────────────────────┐
│  输入：YouTube URL + 语言代码                                 │
│  示例：https://youtube.com/watch?v=VIDEO_ID, zh             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 1: 初始化 (0.1 秒)                                       │
│  - 清空日志文件                                              │
│  - 记录开始时间                                              │
│  - 提取视频 ID                                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 2: 下载音频 (1-3 分钟)                                   │
│  - 创建临时目录                                              │
│  - 调用 yt-dlp 下载                                          │
│  - 格式：bestaudio                                           │
│  - 超时：600 秒                                              │
│  - 输出：/tmp/xxx.webm                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 3: Whisper 转录 (视频时长的 0.6-1 倍)                      │
│  - 加载 tiny 模型 (100MB)                                    │
│  - 语音识别                                                  │
│  - 生成时间戳                                                │
│  - 每 300 秒更新进度                                          │
│  - 超时：1800 秒                                             │
│  - 输出：transcript[] 数组                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 4: 生成总结 (0.5-1 分钟)                                 │
│  - 计算元数据（时长、行数）                                   │
│  - 截取前 50 行                                               │
│  - 保存 JSON 结果                                             │
│  - 保存 TXT 完整转录                                          │
│  - 清理临时文件                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  输出：三个文件                                              │
│  - /tmp/transcribe_result.json (JSON 总结)                  │
│  - /tmp/transcript_*.txt (完整转录)                         │
│  - /tmp/transcribe_progress.log (进度日志)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 文件结构

```
Youtube-Transcriber-Skill/
├── SKILL.md                    # OpenClaw 技能描述
├── README.md                   # 使用说明
├── ARCHITECTURE.md             # 架构文档（本文件）
├── transcribe.py               # 主脚本（支持后台）
├── start_transcribe.sh         # 启动脚本
└── package.json                # npm 配置

临时文件（运行时生成）：
├── /tmp/transcribe_progress.log    # 进度日志
├── /tmp/transcribe_result.json     # JSON 结果
└── /tmp/transcript_*.txt           # 完整转录
```

---

## 🔧 核心代码模块

### 1. 日志记录模块

```python
LOG_FILE = '/tmp/transcribe_progress.log'

def log(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')
    print(message, flush=True)
```

**功能：**
- 写入日志文件
- 同时打印到控制台
- 带时间戳

---

### 2. 下载模块

```python
def download_audio(video_url, output_path):
    cmd = [
        'python3', '-m', 'yt_dlp',
        '-f', 'bestaudio',
        '-o', output_path,
        '--no-playlist',
        '--socket-timeout', '60',
        video_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return result.returncode == 0
```

**功能：**
- 调用 yt-dlp
- 下载最佳音频
- 超时保护 600 秒

---

### 3. 转录模块

```python
def transcribe_audio(audio_path, language='auto'):
    from faster_whisper import WhisperModel
    model = WhisperModel('tiny', device='cpu', compute_type='int8')
    
    segments, info = model.transcribe(audio_path, 
                                       language=language if language != 'auto' else None)
    
    transcript = []
    start_time = time.time()
    last_update = 0
    
    for seg in segments:
        transcript.append({
            'start': seg.start,
            'end': seg.end,
            'text': seg.text
        })
        
        # 每 5 分钟更新进度
        elapsed = int(time.time() - start_time)
        if elapsed > 0 and elapsed % 300 == 0 and elapsed != last_update:
            progress = (seg.start / total_duration * 100)
            log(f'📊 进度：{progress:.1f}%')
            last_update = elapsed
    
    return {'language': info.language, 'duration': info.duration, 'transcript': transcript}
```

**功能：**
- 加载 Whisper 模型
- 语音识别
- 进度更新
- 返回结构化数据

---

### 4. 结果保存模块

```python
RESULT_FILE = '/tmp/transcribe_result.json'

def save_result(data):
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**功能：**
- JSON 格式保存
- UTF-8 编码
- 美化格式

---

## 📊 数据流图

```
YouTube URL
    │
    ▼
┌─────────────────┐
│  yt-dlp 下载     │
│  audio.webm    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Whisper 转录    │
│  transcript[]  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成总结        │
│  result.json   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  保存文件        │
│  - result.json │
│  - transcript  │
│  - progress    │
└─────────────────┘
```

---

## ⏱️ 性能指标

| 指标 | 值 | 说明 |
|------|-----|------|
| 模型大小 | 100MB | Whisper tiny |
| 内存占用 | 300-500MB | 转录过程中 |
| 转录速度 | 0.6-1x 实时 | 取决于 CPU |
| 下载速度 | 取决于网络 | 通常 1-3 分钟 |
| 进度更新 | 每 300 秒 | 5 分钟一次 |

---

## 🔐 超时保护

| 阶段 | 超时 | 处理 |
|------|------|------|
| 下载 | 600 秒 | subprocess timeout |
| 转录 | 1800 秒 | OpenClaw timeout |
| 总计 | 3600 秒 | Agent timeout |

---

## 🎯 扩展性

### 支持的视频时长

| 时长 | 支持 | 建议 |
|------|------|------|
| <10 分钟 | ✅ | 直接运行 |
| 10-30 分钟 | ✅ | 直接运行 |
| 30-60 分钟 | ✅ | 后台运行 |
| >60 分钟 | ✅ | 后台运行 + 分段 |

---

## 📝 配置要求

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

---

**文档版本：** v2.1.0  
**最后更新：** 2026-04-08
