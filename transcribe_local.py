#!/usr/bin/env python3
"""
YouTube 转录总结 - NAS 本地版（不依赖 Mac）
直接在 NAS 上下载和转录
"""
import sys, os, subprocess, json, tempfile
from pathlib import Path

def download_audio(video_url, output_path):
    """使用 yt-dlp 下载音频"""
    cmd = [
        'python3', '-m', 'yt_dlp',
        '-f', 'bestaudio[ext=webm]/bestaudio',
        '-o', output_path,
        '--no-playlist',
        '--socket-timeout', '30',
        video_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0, result.stderr

def transcribe_audio(audio_path, language='auto'):
    """使用 Whisper 转录"""
    from faster_whisper import WhisperModel
    
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    # 自动检测语言
    if language == 'auto':
        segments, info = model.transcribe(audio_path)
    else:
        segments, info = model.transcribe(audio_path, language=language)
    
    transcript = []
    for seg in segments:
        transcript.append({
            'start': seg.start,
            'end': seg.end,
            'text': seg.text
        })
    
    return {
        'language': info.language,
        'transcript': transcript
    }

def format_transcript(transcript_data):
    """格式化为带时间戳的文本"""
    lines = []
    for item in transcript_data['transcript']:
        lines.append(f"[{item['start']:.2f}s -> {item['end']:.2f}s] {item['text']}")
    return '\n'.join(lines)

def summarize(transcript_text, video_url):
    """生成简单总结"""
    lines = transcript_text.split('\n')
    return f"""# 视频转录总结

**URL:** {video_url}
**语言:** 自动检测
**时长:** {len(lines)} 行

## 内容预览
{transcript_text[:500]}...

## 完整转录
{transcript_text}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_local.py <YouTube_URL> [language]")
        sys.exit(1)
    
    video_url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'auto'
    
    print(f"📺 URL: {video_url}")
    print(f"🌐 Language: {language}")
    
    # 提取 video_id
    video_id = video_url.split('v=')[-1].split('&')[0] if 'v=' in video_url else video_url.split('/')[-1].split('?')[0]
    
    # 创建临时文件
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, f"{video_id}.webm")
        
        # 1. 下载
        print("\n[1/3] 下载音频...")
        success, error = download_audio(video_url, audio_path)
        if not success:
            print(f"❌ 下载失败：{error[:200]}")
            sys.exit(1)
        print(f"✅ 下载成功：{audio_path}")
        
        # 2. 转录
        print("\n[2/3] 转录中...")
        try:
            transcript_data = transcribe_audio(audio_path, language)
            print(f"✅ 转录完成！语言：{transcript_data['language']}")
        except Exception as e:
            print(f"❌ 转录失败：{e}")
            sys.exit(1)
        
        # 3. 格式化
        print("\n[3/3] 生成总结...")
        transcript_text = format_transcript(transcript_data)
        summary = summarize(transcript_text, video_url)
        
        # 输出
        print("\n" + "="*60)
        print(summary)
        print("="*60)

if __name__ == "__main__":
    main()
