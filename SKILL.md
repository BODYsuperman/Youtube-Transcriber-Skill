---
name: youtube-transcribe-v2
description: YouTube 视频自动转录 + AI 总结（HTTP API 版）。Usage: 直接发 YouTube 链接
user-invocable: true
---

# YouTube 转录总结 Skill V2

## 工作流程

1. 接收 YouTube 链接
2. HTTP POST → Mac API 创建任务
3. 轮询等待任务完成
4. 读取转录文件
5. AI 分段总结
6. 返回 Markdown 总结

## 配置

- Mac API: http://192.168.1.193:8000
- 超时：2700 秒 (45 分钟)
- 轮询间隔：30 秒
