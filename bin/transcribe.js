#!/usr/bin/env node

/**
 * YouTube Transcriber CLI
 * 
 * Usage:
 *   npx youtube-transcribe <URL> [language]
 *   npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" zh
 * 
 * Requirements:
 *   - Node.js >= 14.0.0
 *   - Python >= 3.8.0
 *   - yt-dlp (Python package)
 *   - faster-whisper (Python package)
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get command line arguments
const args = process.argv.slice(2);

// Show help if no arguments
if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
  console.log(`
🎯 YouTube Transcriber - Automatically transcribe YouTube videos

Usage:
  npx youtube-transcribe <URL> [language]

Examples:
  npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
  npx youtube-transcribe "URL" zh        # Chinese
  npx youtube-transcribe "URL" en        # English
  npx youtube-transcribe "URL" auto      # Auto-detect

Options:
  -h, --help     Show this help message
  -v, --version  Show version

Requirements:
  - Node.js >= 14.0.0
  - Python >= 3.8.0
  - yt-dlp (pip3 install yt-dlp)
  - faster-whisper (pip3 install faster-whisper)

Install dependencies:
  pip3 install -r requirements.txt
`);
  process.exit(0);
}

// Show version
if (args.includes('-v') || args.includes('--version')) {
  const pkg = require('../package.json');
  console.log(`youtube-transcriber-skill v${pkg.version}`);
  process.exit(0);
}

// Get URL and language
const url = args.find(arg => arg.includes('youtube.com') || arg.includes('youtu.be'));
const language = args.find(arg => ['zh', 'en', 'ja', 'ko', 'auto'].includes(arg)) || 'auto';

if (!url) {
  console.error('❌ Error: Please provide a YouTube URL');
  console.error('Example: npx youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"');
  process.exit(1);
}

// Get script directory
const scriptDir = __dirname;
const pythonScript = path.join(scriptDir, '..', 'transcribe.py');

// Check if Python script exists
if (!fs.existsSync(pythonScript)) {
  console.error('❌ Error: transcribe.py not found');
  process.exit(1);
}

// Check Python installation
try {
  execSync('python3 --version', { stdio: 'ignore' });
} catch (error) {
  console.error('❌ Error: Python 3 is required but not installed');
  console.error('Please install Python 3.8 or higher: https://www.python.org/downloads/');
  process.exit(1);
}

// Run Python script
console.log('🎯 YouTube Transcriber v1.0.0\n');

try {
  const pythonArgs = language === 'auto' ? [pythonScript, url] : [pythonScript, url, language];
  execSync(`python3 ${pythonArgs.join(' ')}`, {
    stdio: 'inherit',
    env: process.env
  });
} catch (error) {
  console.error('\n❌ Error: Transcription failed');
  console.error('\nPossible solutions:');
  console.error('1. Install dependencies: pip3 install -r requirements.txt');
  console.error('2. Check your internet connection');
  console.error('3. Verify the YouTube URL is valid');
  console.error('4. If behind firewall, use proxy: python3 transcribe.py "URL" -p "http://proxy:port"');
  process.exit(1);
}
