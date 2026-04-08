# NPX 使用指南

## 🎯 什么是 NPX？

**NPX** 是 Node.js 的包执行工具，允许你无需安装即可运行 npm 包。

**优势：**
- ✅ 无需克隆仓库
- ✅ 无需安装依赖
- ✅ 一行命令即可使用
- ✅ 自动处理所有依赖

---

## 🚀 快速开始

### 基础用法

```bash
# 自动检测语言
npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"

# 指定语言
npx youtube-transcribe "URL" zh      # 中文
npx youtube-transcribe "URL" en      # 英文
npx youtube-transcribe "URL" ja      # 日文
npx youtube-transcribe "URL" ko      # 韩文
```

### 实际例子

```bash
# 转录英文视频
npx youtube-transcribe "https://youtube.com/watch?v=jNQXAC9IVRw"

# 转录中文视频
npx youtube-transcribe "https://youtube.com/watch?v=9uDH8z-HZKs" zh

# 自动检测语言
npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" auto
```

---

## 📦 系统要求

| 要求 | 最低版本 | 检查命令 |
|------|---------|---------|
| **Node.js** | >= 14.0.0 | `node --version` |
| **Python** | >= 3.8.0 | `python3 --version` |
| **npm** | >= 6.0.0 | `npm --version` |

### 安装 Node.js

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**macOS:**
```bash
brew install node
```

**Windows:**
- 下载安装：https://nodejs.org/

### 安装 Python

**Ubuntu/Debian:**
```bash
sudo apt-get install -y python3 python3-pip
```

**macOS:**
```bash
brew install python
```

**Windows:**
- 下载安装：https://www.python.org/downloads/

---

## 🔧 常见问题

### Q1: `npx: command not found`

**解决方案：** 安装 Node.js

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node
```

### Q2: `python3: command not found`

**解决方案：** 安装 Python 3

```bash
# Ubuntu/Debian
sudo apt-get install -y python3 python3-pip

# macOS
brew install python
```

### Q3: 下载失败（403 错误）

**解决方案：** 使用代理

```bash
# 临时使用代理
npx youtube-transcribe "URL" -p "http://proxy:port"

# 或设置环境变量
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
npx youtube-transcribe "URL"
```

### Q4: 转录太慢

**解决方案：**
1. 使用更小的模型（需要修改代码）
2. 使用更好的 CPU/GPU
3. 检查网络连接

### Q5: 内存不足

**解决方案：**
- 关闭其他程序释放内存
- 使用更小的模型（tiny）
- 增加系统内存

---

## 📊 性能对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| **NPX** | 无需安装，随时随地用 | 首次运行需下载 |
| **Python** | 完全控制，可定制 | 需安装依赖 |

---

## 🎯 最佳实践

### 1. 使用引号包裹 URL

```bash
# ✅ 正确
npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"

# ❌ 错误（可能被 shell 解析）
npx youtube-transcribe https://youtube.com/watch?v=VIDEO_ID
```

### 2. 后台运行长视频

```bash
# 后台运行
nohup npx youtube-transcribe "URL" > output.log 2>&1 &

# 查看进度
tail -f output.log
```

### 3. 批量处理

```bash
# 创建脚本
cat > batch.sh << 'EOF'
#!/bin/bash
for url in "$@"; do
    echo "Processing: $url"
    npx youtube-transcribe "$url"
done
EOF

chmod +x batch.sh

# 使用
./batch.sh "URL1" "URL2" "URL3"
```

---

## 📝 输出示例

```
🎯 YouTube Transcriber v1.0.0

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
...
============================================================
```

---

## 🙏 反馈与支持

遇到问题？欢迎反馈：
- **GitHub Issues:** https://github.com/BODYsuperman/Youtube-Transcriber-Skill/issues
- **讨论区:** https://github.com/BODYsuperman/Youtube-Transcriber-Skill/discussions

---

**享受便捷的视频转录！** 🎉
