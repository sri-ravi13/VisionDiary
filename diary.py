"""
Vision Diary - Alternative Version with Replicate API
This version is more suitable for production deployment on Render.
It uses Replicate's API instead of Selenium for image generation.

To use this version:
1. Sign up at https://replicate.com
2. Get your API token from https://replicate.com/account/api-tokens
3. Add REPLICATE_API_TOKEN to your Render environment variables
4. Install: pip install replicate
"""

import os
import datetime
import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
import requests
import replicate

def generate_prompts(story):
    """Split story into individual prompts."""
    prompts = story.split('. ')
    detailed_prompts = []
    for prompt in prompts:
        if prompt.strip():
            detailed_prompt = f"{prompt.strip()}."
            detailed_prompts.append(detailed_prompt)
    return detailed_prompts[:8]  # Limit to 8 images to save time/cost

def generate_images_replicate(prompts, save_directory):
    """Generate images using Replicate API (much faster and more reliable)."""
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        raise ValueError("REPLICATE_API_TOKEN environment variable not set!")
    
    images = []
    
    for i, prompt in enumerate(prompts):
        try:
            st.info(f"Generating image {i+1}/{len(prompts)}...")
            
            # Use SDXL model via Replicate
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": f"Professional photo-realistic image: {prompt}",
                    "width": 1024,
                    "height": 1024,
                    "num_outputs": 1,
                }
            )
            
            # Download the generated image
            image_url = output[0]
            image_path = os.path.join(save_directory, f"generated_image_{i+1}.jpg")
            
            response = requests.get(image_url)
            with open(image_path, "wb") as f:
                f.write(response.content)
            
            images.append(image_path)
            print(f"Image {i+1} generated successfully!")
            
        except Exception as e:
            st.error(f"Error generating image {i+1}: {str(e)}")
            print(f"Error: {e}")
    
    return images

def generate_audio(story_text, audio_path):
    """Generate audio from text using gTTS."""
    tts = gTTS(story_text, lang='en')
    tts.save(audio_path)
    print(f"Audio generated successfully!")

def create_video(images, audio_path, video_path):
    """Create video from images and audio."""
    if not images:
        raise ValueError("No images were generated. Cannot create video.")
    
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    
    num_images = len(images)
    duration_per_image = audio_duration / num_images
    
    clip = ImageSequenceClip(images, durations=[duration_per_image] * num_images)
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile(video_path, codec="libx264", fps=24)
    print(f"Video created successfully!")

# Streamlit UI
st.set_page_config(page_title="Vision Diary", page_icon="📔", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📔 Vision Diary")
st.markdown("### Transform your daily stories into beautiful AI-generated videos!")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.write("---")
    st.write("✨ **How it works:**")
    st.write("1. Select a date for your diary entry")
    st.write("2. Write your story")
    st.write("3. AI generates images based on your story")
    st.write("4. Get a video with narration!")
    
    st.write("---")
    
    # Check if API token is configured
    if not os.getenv("REPLICATE_API_TOKEN"):
        st.warning("⚠️ REPLICATE_API_TOKEN not configured. Please add it to environment variables.")
        st.info("Get your API token from: https://replicate.com/account/api-tokens")
    
    if st.button("🚀 Start Creating", type="primary"):
        st.session_state.page = 'calendar'
        st.rerun()

elif st.session_state.page == 'calendar':
    st.write("---")
    st.subheader("📅 Select a Date")
    selected_date = st.date_input("Choose a date for your diary entry:", datetime.date.today())
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("Continue →", type="primary"):
            st.session_state.page = 'input'
            st.session_state.selected_date = selected_date
            st.rerun()

elif st.session_state.page == 'input':
    st.write("---")
    st.subheader(f"📝 Diary Entry for {st.session_state.selected_date}")
    
    diary_text = st.text_area(
        "Write your story:",
        height=250,
        placeholder="Today was an amazing day. I went to the park and saw beautiful flowers. The sun was shining brightly. I met my friends and we had a great time..."
    )
    
    st.info("💡 Tip: Write 3-8 sentences for best results. Each sentence will become an image in your video.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Calendar"):
            st.session_state.page = 'calendar'
            st.rerun()
    
    with col2:
        if st.button("🎬 Generate Video", type="primary"):
            if not diary_text.strip():
                st.error("❌ Please enter some text for your diary entry!")
            else:
                with st.spinner("🎨 Creating your video... This may take 2-3 minutes."):
                    try:
                        # Create save directory
                        save_directory = f"./diary_{st.session_state.selected_date}"
                        os.makedirs(save_directory, exist_ok=True)
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Step 1: Generate prompts
                        status_text.text("📝 Processing your story...")
                        prompts = generate_prompts(diary_text)
                        progress_bar.progress(20)
                        
                        # Step 2: Generate images
                        status_text.text(f"🎨 Generating {len(prompts)} images with AI...")
                        images = generate_images_replicate(prompts, save_directory)
                        progress_bar.progress(60)
                        
                        if not images:
                            st.error("❌ Failed to generate images. Please try again.")
                        else:
                            # Step 3: Create audio
                            status_text.text("🎵 Creating audio narration...")
                            audio_path = os.path.join(save_directory, f"story_audio.mp3")
                            generate_audio(diary_text, audio_path)
                            progress_bar.progress(80)
                            
                            # Step 4: Create video
                            status_text.text("🎬 Assembling your video...")
                            video_path = os.path.join(save_directory, f"story_video.mp4")
                            create_video(images, audio_path, video_path)
                            progress_bar.progress(100)
                            
                            status_text.text("✅ Video created successfully!")
                            
                            st.success("🎉 Your Vision Diary video is ready!")
                            st.video(video_path)
                            
                            # Download button
                            with open(video_path, "rb") as video_file:
                                st.download_button(
                                    label="📥 Download Video",
                                    data=video_file,
                                    file_name=f"vision_diary_{st.session_state.selected_date}.mp4",
                                    mime="video/mp4",
                                    type="primary"
                                )
                            
                            # Show generated images
                            with st.expander("🖼️ View Generated Images"):
                                cols = st.columns(3)
                                for idx, img_path in enumerate(images):
                                    with cols[idx % 3]:
                                        st.image(img_path, caption=f"Scene {idx+1}")
                                        
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.error("Please check your API token and try again.")

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("Vision Diary transforms your written stories into beautiful AI-generated videos.")
    
    st.header("🔧 Setup")
    st.write("This app requires a Replicate API token.")
    st.write("Get yours at: [replicate.com](https://replicate.com)")
    
    st.header("📊 Stats")
    if os.getenv("REPLICATE_API_TOKEN"):
        st.success("✅ API Token: Configured")
    else:
        st.error("❌ API Token: Not configured")