# Vision Diary 📖✨

Transform your daily journal entries into captivating visual stories! Vision Diary is an innovative Streamlit-based application that automatically generates AI-powered images from your diary text and creates stunning video narratives with voiceovers.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Dependencies](#dependencies)
- [Setup Guide](#setup-guide)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
## 🌟 Overview

Vision Diary brings your written memories to life by combining cutting-edge AI image generation with text-to-speech technology. Simply write about your day, and watch as your words transform into a beautiful video montage complete with narration.

**Perfect for:**
- Personal journaling and reflection
- Creating visual memories of special moments
- Storytelling and creative writing
- Social media content creation
- Memory preservation for loved ones

## ✨ Features

### 🎨 AI-Powered Image Generation
- Automatically converts diary entries into visual prompts
- Uses advanced AI image generation (flux model via aicreate.com)
- Photo-realistic image enhancement
- High-resolution 1024x1024 images

### 🎙️ Text-to-Speech Narration
- Converts your written story into natural-sounding audio
- Uses Google Text-to-Speech (gTTS) engine
- Clear, expressive narration

### 🎬 Automated Video Creation
- Seamlessly combines images and audio
- Smooth transitions between scenes
- Professional-quality output (1080p, 24 fps)
- MP4 format for universal compatibility

### 📅 Calendar-Based Organization
- Date-specific diary entries
- Organized file structure by date
- Easy retrieval of past memories

### 💡 Dual Input Modes
- **Text Mode**: Type your story directly
- **Audio Mode**: Upload pre-recorded audio files

### 🖥️ User-Friendly Interface
- Clean, intuitive Streamlit interface
- Step-by-step guided workflow
- Real-time progress updates

## 🔧 How It Works

1. **Select a Date**: Choose the date for your diary entry
2. **Input Your Story**: Write your story or upload an audio file
3. **AI Processing**: 
   - Text is split into meaningful prompts
   - Each prompt is enhanced for better image generation
   - AI generates photo-realistic images for each scene
4. **Audio Generation**: Text-to-speech converts your story to narration
5. **Video Creation**: Images and audio are synchronized into a video
6. **Download & Share**: Your visual diary is ready!

## 🚀 Installation

### Prerequisites

Before installing Vision Diary, ensure you have:

- **Python 3.8+** installed
- **Google Chrome Browser** (for Selenium automation)
- **ChromeDriver** matching your Chrome version
- **FFmpeg** (for video processing)
- Stable internet connection (for AI image generation)

### System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 1GB free space minimum
- **Internet**: Required for AI image generation

## 📦 Dependencies

### Core Libraries

```txt
streamlit>=1.28.0
gtts>=2.4.0
moviepy>=1.0.3
selenium>=4.15.0
requests>=2.31.0
Pillow>=10.0.0
```

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/vision-diary.git
cd vision-diary
```

2. **Create a Virtual Environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

4. **Install FFmpeg**

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

5. **Download ChromeDriver**

- Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
- Download version matching your Chrome browser
- Extract and note the path (used in configuration)

## 🛠️ Setup Guide

### 1. Configure ChromeDriver Path

Edit `diary.py` and update the ChromeDriver path:

```python
# Line 33 in diary.py
service = Service(r"C:\Windows\chromedriver-win64\chromedriver.exe")

# Change to your ChromeDriver location
# Windows example: r"C:\path\to\chromedriver.exe"
# macOS/Linux example: "/usr/local/bin/chromedriver"
```

### 2. Test Installation

```bash
# Test if all dependencies are installed
python -c "import streamlit, gtts, moviepy, selenium; print('All dependencies installed!')"
```

### 3. Verify FFmpeg

```bash
ffmpeg -version
```

If FFmpeg is not recognized, add it to your system PATH.

## 💻 Usage

### Starting the Application

```bash
streamlit run diary.py
```

The application will open in your default web browser at `http://localhost:8501`

### Creating Your First Video Diary

#### Text Input Method

1. **Click "Start"** on the home page
2. **Select a Date** from the calendar
3. **Choose "Text"** as input type
4. **Enter Your Story** in the text area:
   ```
   Example:
   "Today was an amazing day at the beach. The sun was shining bright and the waves were perfect for surfing. I made sandcastles with my family and watched the sunset over the ocean. It was a perfect day filled with laughter and joy."
   ```
5. **Click "Generate Video"**
6. **Wait** for processing (2-5 minutes depending on story length)
7. **Watch** your video in the browser
8. **Download** from the generated folder

#### Audio Input Method

1. **Click "Start"** on the home page
2. **Select a Date** from the calendar
3. **Choose "Audio"** as input type
4. **Upload** your pre-recorded MP3 file
5. **Click "Generate Video"**
6. **Wait** for processing
7. **View and download** your video

### Output Location

Videos are saved in date-specific folders:

```
vision-diary/
├── diary.py
├── 2024-01-15/
│   ├── generated_image_1.jpg
│   ├── generated_image_2.jpg
│   ├── generated_image_3.jpg
│   ├── 2024-01-15_story_audio.mp3
│   └── 2024-01-15_story_video.mp4
├── 2024-01-16/
│   └── ...
```

## 📁 Project Structure

```
vision-diary/
│
├── diary.py                    # Main application file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── venv/                       # Virtual environment (not tracked)
│
├── [DATE]/                     # Auto-generated folders per date
│   ├── generated_image_*.jpg   # AI-generated images
│   ├── [DATE]_story_audio.mp3  # Generated audio
│   └── [DATE]_story_video.mp4  # Final video output
│
└── .gitignore                  # Git ignore file
```

## 🔍 Technical Details

### Image Generation Pipeline

1. **Prompt Splitting**: Story is divided by sentences
2. **Prompt Enhancement**: Each prompt is enhanced for better visual results
3. **Photo-Realistic Conversion**: Prompts are converted to photo-realistic style
4. **AI Generation**: flux model generates 1024x1024 images
5. **Download & Storage**: Images are saved locally

### Audio Generation

- **Engine**: Google Text-to-Speech (gTTS)
- **Language**: English (configurable)
- **Format**: MP3
- **Quality**: Standard voice quality

### Video Creation

- **Codec**: H.264 (libx264)
- **Frame Rate**: 24 fps
- **Resolution**: Based on input images (1024x1024)
- **Duration**: Auto-calculated based on audio length
- **Minimum Images**: 8 images (padded if necessary)

### Web Automation

```python
# Selenium WebDriver automates:
# 1. Navigation to AI generator
# 2. Prompt entry
# 3. Enhancement activation
# 4. Model selection (flux)
# 5. Size selection (1024x1024)
# 6. Image generation trigger
# 7. Download automation
```

## ⚙️ Configuration

### Customizing Image Count

Edit the `create_video` function in `diary.py`:

```python
# Line 132
num_images = max(8, len(images))  # Change 8 to desired minimum
```

### Changing Voice/Language

Edit the `generate_audio` function:

```python
# Line 124
tts = gTTS(story_text, lang='en')  # Change 'en' to other language codes
# Examples: 'es' (Spanish), 'fr' (French), 'de' (German)
```

### Video Quality Settings

Edit the `create_video` function:

```python
# Line 136
final_clip.write_videofile(video_path, codec="libx264", fps=24)
# Change fps to 30 or 60 for smoother video
# Add bitrate parameter: bitrate="5000k"
```

### Timeout Settings

Adjust Selenium wait times if you have slow internet:

```python
# Increase wait times in generate_images function
WebDriverWait(driver, 30)  # Change 30 to 60 for slower connections
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. ChromeDriver Error
```
Error: ChromeDriver not found
```
**Solution:**
- Verify ChromeDriver path in `diary.py`
- Ensure ChromeDriver version matches Chrome browser
- Check file permissions (executable on Unix systems)

#### 2. Image Generation Timeout
```
Error: Timeout waiting for element
```
**Solution:**
- Check internet connection
- Increase timeout values in code
- Verify aicreate.com is accessible
- Try again during off-peak hours

#### 3. FFmpeg Not Found
```
Error: FFmpeg not found
```
**Solution:**
- Install FFmpeg using instructions above
- Add FFmpeg to system PATH
- Restart terminal/command prompt

#### 4. Audio Generation Error
```
Error: gTTS request failed
```
**Solution:**
- Check internet connection
- Verify gTTS is installed: `pip install --upgrade gtts`
- Try shorter text if quota exceeded

#### 5. Video Creation Failed
```
Error: MoviePy error
```
**Solution:**
- Ensure at least 1 image was generated
- Check FFmpeg is properly installed
- Verify sufficient disk space
- Check audio file is valid

#### 6. Streamlit Won't Start
```
Error: Port already in use
```
**Solution:**
```bash
# Use different port
streamlit run diary.py --server.port 8502
```

### Debug Mode

Enable verbose logging:

```python
# Add at top of diary.py
import logging
logging.basicConfig(level=logging.DEBUG)
```
**Happy Diary Writing! 📖✨🎬**