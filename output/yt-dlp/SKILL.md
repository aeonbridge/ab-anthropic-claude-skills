---
name: yt-dlp
description: Comprehensive skill for yt-dlp - feature-rich command-line audio/video downloader supporting thousands of sites
version: 1.0.0
---

# yt-dlp Skill

Expert assistance for using yt-dlp, a feature-rich command-line audio/video downloader with support for thousands of websites. Fork of youtube-dl with enhanced features and active maintenance.

## When to Use This Skill

This skill should be used when:
- Downloading videos or audio from YouTube, Vimeo, or thousands of other sites
- Extracting audio from videos in various formats (MP3, M4A, OPUS, etc.)
- Downloading entire playlists or channels
- Selecting specific video quality or format combinations
- Embedding metadata, subtitles, or thumbnails
- Automating media downloads with scripts
- Recording live streams
- Converting video formats with FFmpeg integration
- Extracting video information without downloading
- Troubleshooting download issues or understanding yt-dlp options
- Setting up advanced configurations for batch processing

## Overview

**yt-dlp** is a powerful command-line tool that:
- **Supports thousands of sites**: YouTube, Vimeo, Twitter, Facebook, Instagram, TikTok, and many more
- **Actively maintained**: Regular updates with bug fixes and new features
- **Feature-rich**: Extensive options for format selection, metadata handling, and post-processing
- **Fast and efficient**: Multi-threaded downloads with resume capability
- **Extensible**: Plugin system for custom extractors and post-processors

### Key Improvements Over youtube-dl
- Better performance and stability
- More format options and quality selection
- Enhanced metadata handling
- Improved playlist and channel downloads
- Better error handling and retry logic
- Active development and frequent updates
- SponsorBlock integration for YouTube

## Installation

### Recommended Methods

#### Windows
```bash
# Download standalone executable
# Visit: https://github.com/yt-dlp/yt-dlp/releases/latest
# Download: yt-dlp.exe (64-bit)

# Or use winget
winget install yt-dlp

# Or use scoop
scoop install yt-dlp
```

#### macOS
```bash
# Using Homebrew
brew install yt-dlp

# Or download directly
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos -o /usr/local/bin/yt-dlp
chmod a+rx /usr/local/bin/yt-dlp
```

#### Linux
```bash
# Using pip (recommended)
python3 -m pip install -U yt-dlp

# Or download binary
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# Debian/Ubuntu (via apt)
sudo add-apt-repository ppa:tomtomtom/yt-dlp
sudo apt update
sudo apt install yt-dlp
```

#### Using pip (cross-platform)
```bash
# Install or upgrade
python3 -m pip install -U yt-dlp

# Or with pipx (isolated environment)
pipx install yt-dlp
```

### Essential Dependencies

#### FFmpeg (Strongly Recommended)
Required for merging video+audio formats and post-processing:

```bash
# Windows (scoop)
scoop install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

#### Optional Dependencies
```bash
# For better performance and features
pip install brotli certifi mutagen pycryptodomex websockets

# For browser cookie support
pip install secretstorage  # Linux
pip install pywin32        # Windows

# For HTTP/3 and impersonation
pip install curl-cffi
```

## Quick Start

### Basic Downloads

```bash
# Download a video
yt-dlp "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download from multiple URLs
yt-dlp URL1 URL2 URL3

# Download from a file containing URLs
yt-dlp -a urls.txt

# Download entire playlist
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Download channel
yt-dlp "https://www.youtube.com/@channelname"
```

### Audio-Only Downloads

```bash
# Extract audio as MP3
yt-dlp -x --audio-format mp3 URL

# Extract audio as best quality
yt-dlp -x --audio-quality 0 URL

# Extract audio with metadata
yt-dlp -x --audio-format mp3 --embed-metadata --embed-thumbnail URL

# Download music with best quality
yt-dlp -f 'bestaudio[ext=m4a]' --embed-thumbnail --add-metadata URL
```

## Format Selection

### Understanding Formats

```bash
# List all available formats
yt-dlp -F URL

# Download best quality (video+audio)
yt-dlp -f "best" URL

# Download best video and best audio separately, then merge
yt-dlp -f "bestvideo+bestaudio" URL

# Download specific format by ID
yt-dlp -f 22 URL

# Download best video up to 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" URL

# Download best MP4 format
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" URL
```

### Advanced Format Selection

```bash
# Best quality with size limit (under 100MB)
yt-dlp -f "best[filesize<100M]" URL

# Specific resolution
yt-dlp -f "bestvideo[height=720]+bestaudio" URL

# Prefer 60fps
yt-dlp -f "bestvideo[fps>30]+bestaudio" URL

# Download only video (no audio)
yt-dlp -f "bestvideo" URL

# Download only audio
yt-dlp -f "bestaudio" URL

# Prefer free codecs (VP9/Opus over H.264/AAC)
yt-dlp -f "bestvideo[vcodec^=vp]+bestaudio[acodec^=opus]" URL
```

## Common Use Cases

### 1. Download Entire Channel or Playlist

```bash
# Download all videos from a channel
yt-dlp -f "bestvideo[height<=1080]+bestaudio" \
       --output "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" \
       "https://www.youtube.com/@channelname"

# Download playlist with numbered files
yt-dlp --output "%(playlist_index)s-%(title)s.%(ext)s" PLAYLIST_URL

# Download only videos uploaded in last 7 days
yt-dlp --dateafter now-7days CHANNEL_URL

# Download specific date range
yt-dlp --dateafter 20230101 --datebefore 20231231 CHANNEL_URL
```

### 2. Download with Subtitles

```bash
# Download video with all subtitles
yt-dlp --write-subs --write-auto-subs URL

# Download with specific subtitle language
yt-dlp --write-subs --sub-lang en URL

# Embed subtitles in video file
yt-dlp --write-subs --embed-subs --sub-lang en URL

# Download all available subtitle languages
yt-dlp --write-subs --all-subs URL

# Convert subtitles to SRT format
yt-dlp --write-subs --convert-subs srt URL
```

### 3. Download with Metadata and Thumbnails

```bash
# Embed metadata and thumbnail
yt-dlp --embed-metadata --embed-thumbnail URL

# Download thumbnail as separate file
yt-dlp --write-thumbnail URL

# Convert thumbnail to JPG
yt-dlp --write-thumbnail --convert-thumbnails jpg URL

# Full metadata preservation
yt-dlp --embed-metadata --embed-thumbnail --embed-subs \
       --embed-chapters --write-description --write-info-json URL
```

### 4. Live Stream Recording

```bash
# Record live stream from the beginning
yt-dlp --live-from-start URL

# Record live stream from current time
yt-dlp URL

# Wait for stream to start
yt-dlp --wait-for-video 60 URL

# Monitor and download when live
yt-dlp --wait-for-video 3600 --live-from-start URL
```

### 5. Download Specific Playlist Items

```bash
# Download first 10 videos
yt-dlp --playlist-end 10 PLAYLIST_URL

# Download videos 5-15
yt-dlp --playlist-start 5 --playlist-end 15 PLAYLIST_URL

# Download specific video from playlist
yt-dlp --playlist-items 1,5,8,12 PLAYLIST_URL

# Download every 5th video
yt-dlp --playlist-items "::5" PLAYLIST_URL

# Skip first 20 videos
yt-dlp --playlist-start 21 PLAYLIST_URL
```

### 6. Archive and Download History

```bash
# Skip already downloaded videos
yt-dlp --download-archive archive.txt URL

# Continue interrupted downloads
yt-dlp --continue URL

# Don't overwrite files
yt-dlp --no-overwrites URL

# Force resume from beginning if interrupted
yt-dlp --no-continue URL
```

## Advanced Features

### Output Templates

```bash
# Custom filename pattern
yt-dlp -o "%(title)s.%(ext)s" URL

# Organize by uploader and date
yt-dlp -o "%(uploader)s/%(upload_date)s - %(title)s.%(ext)s" URL

# Include video ID and resolution
yt-dlp -o "%(id)s - %(title)s [%(resolution)s].%(ext)s" URL

# Organized folder structure
yt-dlp -o "Downloads/%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" URL

# Available template fields:
# %(title)s - Video title
# %(id)s - Video ID
# %(ext)s - File extension
# %(uploader)s - Channel/uploader name
# %(upload_date)s - Upload date (YYYYMMDD)
# %(duration)s - Video duration in seconds
# %(resolution)s - Video resolution (e.g., 1920x1080)
# %(playlist)s - Playlist name
# %(playlist_index)s - Position in playlist
# %(channel)s - Channel name
# %(channel_id)s - Channel ID
```

### Post-Processing

```bash
# Convert to MP4
yt-dlp --merge-output-format mp4 URL

# Re-encode video to H.264
yt-dlp --recode-video mp4 URL

# Extract audio and convert to MP3 with 320kbps
yt-dlp -x --audio-format mp3 --audio-quality 0 URL

# Remux to MKV without re-encoding
yt-dlp --remux-video mkv URL

# Embed thumbnail as cover art (audio files)
yt-dlp -x --audio-format mp3 --embed-thumbnail URL

# Add metadata and chapters
yt-dlp --embed-metadata --embed-chapters URL

# Split video by chapters
yt-dlp --split-chapters URL

# Execute command after download
yt-dlp --exec "echo Downloaded: {}" URL
```

### SponsorBlock Integration (YouTube)

```bash
# Skip sponsored segments
yt-dlp --sponsorblock-mark all URL

# Remove sponsored segments
yt-dlp --sponsorblock-remove all URL

# Mark and remove specific categories
yt-dlp --sponsorblock-mark sponsor,intro --sponsorblock-remove outro URL

# Available categories: sponsor, intro, outro, selfpromo, preview,
#                      filler, interaction, music_offtopic
```

### Browser Cookie Support

```bash
# Use cookies from browser
yt-dlp --cookies-from-browser firefox URL

# Use cookies from Chrome
yt-dlp --cookies-from-browser chrome URL

# Use cookies from file
yt-dlp --cookies cookies.txt URL

# Export cookies (for authentication)
# First: Use browser extension to export cookies.txt
yt-dlp --cookies cookies.txt URL
```

### Rate Limiting and Network Options

```bash
# Limit download speed (1MB/s)
yt-dlp --limit-rate 1M URL

# Use proxy
yt-dlp --proxy http://proxy.example.com:8080 URL

# Set custom user agent
yt-dlp --user-agent "Mozilla/5.0..." URL

# Add referer header
yt-dlp --referer "https://example.com" URL

# Set timeout
yt-dlp --socket-timeout 30 URL

# Retry on failure
yt-dlp --retries 10 URL

# Sleep between downloads
yt-dlp --sleep-interval 5 URL
```

### Geo-Restriction Bypass

```bash
# Use VPN or proxy
yt-dlp --proxy socks5://127.0.0.1:1080 URL

# Use Tor
yt-dlp --proxy socks5://127.0.0.1:9050 URL

# Fake IP for geo-restricted content
yt-dlp --geo-bypass URL

# Specify geo-bypass country
yt-dlp --geo-bypass-country US URL
```

## Configuration File

Create `~/.config/yt-dlp/config` (Linux/macOS) or `%APPDATA%/yt-dlp/config.txt` (Windows):

```
# Default format selection
-f bestvideo[height<=1080]+bestaudio/best[height<=1080]

# Output template
-o ~/Downloads/%(uploader)s/%(title)s.%(ext)s

# Always embed metadata
--embed-metadata
--embed-thumbnail
--embed-subs

# Download subtitles
--write-subs
--sub-lang en

# Archive to avoid re-downloading
--download-archive ~/.config/yt-dlp/archive.txt

# No overwrite
--no-overwrites

# Continue incomplete downloads
--continue

# Prefer free formats
--prefer-free-formats

# Add metadata
--add-metadata

# SponsorBlock
--sponsorblock-mark all

# Rate limit (optional)
# --limit-rate 5M

# Retries
--retries 10

# Sleep between downloads
--sleep-interval 3
```

## Information Extraction (No Download)

```bash
# Get video info as JSON
yt-dlp --dump-json URL

# Get only the title
yt-dlp --get-title URL

# Get direct video URL
yt-dlp --get-url URL

# Get filename without downloading
yt-dlp --get-filename URL

# Get thumbnail URL
yt-dlp --get-thumbnail URL

# Get video duration
yt-dlp --get-duration URL

# Get all available info
yt-dlp --dump-single-json URL

# Simulate download (show what would be done)
yt-dlp --simulate URL

# List formats without downloading
yt-dlp -F URL
```

## Batch Processing and Automation

### Bash Script Example

```bash
#!/bin/bash
# download_channel.sh

CHANNEL_URL="$1"
OUTPUT_DIR="$2"

yt-dlp \
    --download-archive archive.txt \
    --format "bestvideo[height<=1080]+bestaudio" \
    --output "${OUTPUT_DIR}/%(upload_date)s - %(title)s.%(ext)s" \
    --write-subs \
    --embed-subs \
    --embed-metadata \
    --embed-thumbnail \
    --no-overwrites \
    --continue \
    --retries 10 \
    --sleep-interval 5 \
    "$CHANNEL_URL"
```

### Python Integration

```python
import yt_dlp

# Basic download
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=VIDEO_ID'])

# Extract info only
with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info('URL', download=False)
    title = info.get('title', None)
    duration = info.get('duration', None)
    print(f"Title: {title}, Duration: {duration}s")

# Audio extraction
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

## Common Options Reference

### General Options

```bash
--help, -h              Show help message
--version               Print program version
--update                Update to latest version
--ignore-errors         Continue on download errors
--no-abort-on-error     Continue even if errors occur
--quiet, -q             Suppress output
--verbose, -v           Print debug information
--dump-json             Output info as JSON
--simulate, -s          Don't download, simulate
```

### Download Options

```bash
-f, --format FORMAT     Format selection
-o, --output TEMPLATE   Output filename template
--playlist-items ITEMS  Playlist items to download
--min-filesize SIZE     Minimum file size
--max-filesize SIZE     Maximum file size
--date DATE             Download only on this date
--datebefore DATE       Download before this date
--dateafter DATE        Download after this date
```

### Post-Processing

```bash
-x, --extract-audio           Extract audio only
--audio-format FORMAT         Audio format (mp3, m4a, opus, etc.)
--audio-quality QUALITY       Audio quality (0-9, 0=best)
--recode-video FORMAT         Re-encode video
--remux-video FORMAT          Remux to different container
--embed-subs                  Embed subtitles in video
--embed-thumbnail             Embed thumbnail
--embed-metadata              Add metadata to file
--embed-chapters              Add chapter markers
--split-chapters              Split by chapters
--sponsorblock-mark CATS      Mark SponsorBlock categories
--sponsorblock-remove CATS    Remove SponsorBlock segments
```

### Subtitle Options

```bash
--write-subs                Write subtitles
--write-auto-subs           Write auto-generated subtitles
--all-subs                  Download all subtitles
--sub-lang LANGS            Subtitle languages (comma-separated)
--sub-format FORMAT         Subtitle format (srt, vtt, etc.)
--convert-subs FORMAT       Convert subtitles to format
```

## Best Practices

### 1. **Use Download Archive**
Always use `--download-archive archive.txt` to avoid re-downloading videos:
```bash
yt-dlp --download-archive archive.txt CHANNEL_URL
```

### 2. **Set Reasonable Rate Limits**
Be respectful of bandwidth:
```bash
yt-dlp --limit-rate 5M --sleep-interval 3 URL
```

### 3. **Use Configuration Files**
Store commonly used options in config file instead of typing them each time.

### 4. **Handle Errors Gracefully**
Use retry options and error handling:
```bash
yt-dlp --retries 10 --ignore-errors --no-abort-on-error URL
```

### 5. **Organize Downloads**
Use meaningful output templates:
```bash
yt-dlp -o "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" URL
```

### 6. **Keep yt-dlp Updated**
Update regularly for bug fixes and new features:
```bash
yt-dlp -U
# or
pip install -U yt-dlp
```

## Troubleshooting

### Common Issues

#### "Unable to extract video data"
```bash
# Update yt-dlp
yt-dlp -U

# Clear cache
yt-dlp --rm-cache-dir

# Try different format
yt-dlp -f 'best' URL
```

#### "HTTP Error 403: Forbidden"
```bash
# Use cookies from browser
yt-dlp --cookies-from-browser firefox URL

# Or use cookies file
yt-dlp --cookies cookies.txt URL
```

#### "Requested format not available"
```bash
# List available formats first
yt-dlp -F URL

# Then select compatible format
yt-dlp -f "bestvideo+bestaudio" URL
```

#### Geo-restricted Content
```bash
# Use proxy or VPN
yt-dlp --proxy socks5://127.0.0.1:1080 URL

# Or bypass geo-restriction
yt-dlp --geo-bypass --geo-bypass-country US URL
```

#### Slow Downloads
```bash
# Use multiple connections
yt-dlp --concurrent-fragments 4 URL

# Check your rate limit setting
# Remove or increase --limit-rate if set
```

### Getting Help

```bash
# Show all options
yt-dlp --help

# Search for specific option
yt-dlp --help | grep subtitle

# Check version
yt-dlp --version

# Verbose output for debugging
yt-dlp --verbose URL
```

## Update and Maintenance

### Updating yt-dlp

```bash
# Self-update (if installed as binary)
yt-dlp -U

# Update via pip
pip install -U yt-dlp

# Update to specific channel
yt-dlp --update-to nightly  # or stable, or master

# Check current version
yt-dlp --version
```

### Release Channels

- **stable**: Well-tested releases (default)
- **nightly**: Daily builds, recommended for regular users
- **master**: Latest development after each commit

## Supported Sites

yt-dlp supports **thousands of sites**, including:

- **Video**: YouTube, Vimeo, Dailymotion, Twitch, TikTok
- **Social**: Facebook, Instagram, Twitter/X, Reddit
- **Streaming**: Twitch, Crunchyroll, Netflix (with cookies), Disney+
- **Education**: Coursera, Udemy, Khan Academy, edX
- **News**: BBC, CNN, NBC, ABC
- **And many more**: Full list at https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## Legal and Ethical Considerations

**Important Notes:**
- Respect copyright and terms of service of websites
- Only download content you have the right to download
- Some content may be protected by DRM or geo-restrictions
- Always check local laws regarding downloading copyrighted content
- Use yt-dlp responsibly and ethically

## Resources

- **GitHub**: https://github.com/yt-dlp/yt-dlp
- **Documentation**: https://github.com/yt-dlp/yt-dlp/blob/master/README.md
- **Supported Sites**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- **Issue Tracker**: https://github.com/yt-dlp/yt-dlp/issues
- **Wiki**: https://github.com/yt-dlp/yt-dlp/wiki

## License

yt-dlp is licensed under the Unlicense (public domain). Some bundled components may use different licenses.

---

**Note**: This skill provides comprehensive guidance for using yt-dlp. Always ensure your use complies with local laws and website terms of service.
