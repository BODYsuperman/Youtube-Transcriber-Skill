#!/usr/bin/env python3
"""
YouTube Transcriber - 支持后台运行
- 自动下载 YouTube 音频
- Whisper AI 语音识别
- 每 5 分钟更新进度
- 完成后生成总结
"""
import sys, os, subprocess, tempfile, time, json
from pathlib import Path

LOG_FILE = '/tmp/transcribe_progress.log'
RESULT_FILE = '/tmp/transcribe_result.json'

def log(message):
    """写入日志"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')
    print(message, flush=True)

def save_result(data):
    """保存结果"""
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def download_audio(video_url, output_path):
    """下载音频"""
    log('[1/3] 开始下载音频...')
    cmd = [
        'python3', '-m', 'yt_dlp',
        '-f', 'bestaudio',
        '-o', output_path,
        '--no-playlist',
        '--socket-timeout', '60',
        video_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        log(f'❌ 下载失败：{result.stderr[:200]}')
        return False
    log('✅ 下载成功')
    return True

def transcribe_audio(audio_path, language='auto'):
    """转录音频"""
    log('[2/3] 开始转录...')
    
    from faster_whisper import WhisperModel
    model = WhisperModel('tiny', device='cpu', compute_type='int8')
    
    segments, info = model.transcribe(audio_path, language=language if language != 'auto' else None)
    
    transcript = []
    total_duration = info.duration
    
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
            progress = (seg.start / total_duration * 100) if total_duration > 0 else 0
            log(f'📊 进度：{progress:.1f}% ({seg.start:.1f}s / {total_duration:.1f}s)')
            last_update = elapsed
    
    log(f'✅ 转录完成！语言：{info.language}')
    
    return {
        'language': info.language,
        'duration': info.duration,
        'transcript': transcript
    }

def generate_summary(result, video_url):
    """生成总结"""
    log('[3/3] 生成总结...')
    
    lines = len(result['transcript'])
    duration = result['duration']
    
    summary = {
        'url': video_url,
        'language': result['language'],
        'duration_minutes': duration / 60,
        'line_count': lines,
        'transcript': result['transcript'][:50],
        'full_line_count': lines
    }
    
    return summary

def transcribe(video_url, language='auto', background=False):
    """主函数"""
    # 清空日志
    open(LOG_FILE, 'w').close()
    
    log(f'📺 开始处理：{video_url}')
    log(f'🌐 语言：{language}')
    
    video_id = video_url.split('v=')[-1].split('&')[0] if 'v=' in video_url else video_url.split('/')[-1].split('?')[0]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, f'{video_id}.webm')
        
        # 1. 下载
        if not download_audio(video_url, audio_path):
            save_result({'error': 'Download failed'})
            return {'error': 'Download failed'}
        
        # 2. 转录
        try:
            result = transcribe_audio(audio_path, language)
        except Exception as e:
            log(f'❌ 转录失败：{e}')
            save_result({'error': str(e)})
            return {'error': str(e)}
        
        # 3. 总结
        summary = generate_summary(result, video_url)
        
        # 4. 保存结果
        save_result(summary)
        
        # 5. 输出
        log('\n' + '='*60)
        log('📝 视频转录总结')
        log('='*60)
        log(f'URL: {video_url}')
        log(f'语言：{summary["language"]}')
        log(f'时长：{summary["duration_minutes"]:.1f} 分钟')
        log(f'行数：{summary["line_count"]}')
        log('')
        log('转录内容（前 10 行）：')
        for item in summary['transcript'][:10]:
            log(f'  [{item["start"]:.2f}s -> {item["end"]:.2f}s] {item["text"]}')
        if summary['line_count'] > 10:
            log(f'  ... 还有 {summary["line_count"]-10} 行 ...')
        log('='*60)
        log(f'✅ 完成！结果已保存到：{RESULT_FILE}')
        
        # 保存完整转录
        transcript_file = f'/tmp/transcript_{video_id}.txt'
        with open(transcript_file, 'w', encoding='utf-8') as f:
            for item in result['transcript']:
                f.write(f'[{item["start"]:.2f}s -> {item["end"]:.2f}s] {item["text"]}\n')
        log(f'📄 完整转录：{transcript_file}')
        
        return summary

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 transcribe.py <URL> [language]')
        print('')
        print('Examples:')
        print('  python3 transcribe.py "https://youtube.com/watch?v=VIDEO_ID"')
        print('  python3 transcribe.py "URL" zh')
        print('  python3 transcribe.py "URL" en')
        sys.exit(1)
    
    url = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'auto'
    
    transcribe(url, lang)
