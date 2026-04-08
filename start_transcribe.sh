#!/bin/bash
# YouTube 后台转录启动脚本
# 用法：./start_transcribe.sh "URL" [language]

if [ -z "$1" ]; then
    echo "用法：$0 <YouTube_URL> [language]"
    echo "例子：$0 'https://youtube.com/watch?v=VIDEO_ID' zh"
    exit 1
fi

URL="$1"
LANG="${2:-auto}"

echo "🚀 启动后台转录..."
echo "📺 视频：$URL"
echo "🌐 语言：$LANG"
echo ""

# 启动后台进程
nohup python3 /tmp/transcribe_background.py "$URL" "$LANG" > /tmp/transcribe_nohup.log 2>&1 &
PID=$!

echo "✅ 后台进程已启动"
echo "📊 进程 ID: $PID"
echo "📄 进度日志：/tmp/transcribe_progress.log"
echo "📝 结果文件：/tmp/transcribe_result.json"
echo ""
echo "查看进度：tail -f /tmp/transcribe_progress.log"
echo "查看结果：cat /tmp/transcribe_result.json"
echo ""

# 监控脚本
cat > /tmp/watch_transcribe.sh << 'EOF'
#!/bin/bash
echo "📊 转录进度监控（按 Ctrl+C 停止）"
echo ""
while true; do
    if [ -f /tmp/transcribe_progress.log ]; then
        tail -n 20 /tmp/transcribe_progress.log
    else
        echo "⏳ 等待转录开始..."
    fi
    sleep 30
done
EOF

chmod +x /tmp/watch_transcribe.sh

echo "💡 提示："
echo "  - 后台运行中，关闭终端不影响"
echo "  - 每 5 分钟自动更新进度"
echo "  - 完成后查看 /tmp/transcribe_result.json"
