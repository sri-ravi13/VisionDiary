import os
import datetime
import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
warnings.simplefilter('ignore', InsecureRequestWarning)

def generate_prompts(story):
    prompts = story.split('. ')
    detailed_prompts = []
    for prompt in prompts:
        if prompt.strip():
            detailed_prompt = f"{prompt.strip()}."
            detailed_prompts.append(detailed_prompt)
    return detailed_prompts

def generate_images(prompts, save_directory):
    images = []
    
    # Setup Chrome options for headless mode (Render compatible)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Use webdriver-manager to automatically handle ChromeDriver
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    except:
        # Fallback for Render deployment
        driver = webdriver.Chrome(options=options)
    
    driver.get("https://aicreate.com/text-to-image-generator/")

    for i, prompt in enumerate(prompts):
        image_generated = False
        retry_count = 0
        max_retries = 3
        
        while not image_generated and retry_count < max_retries:
            try:
                # Wait for page to load
                prompt_input = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "caption"))
                )
                prompt_input.clear()
                prompt_input.send_keys(prompt)

                # Enhance prompt
                enhance_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "enhance-prompt"))
                )
                enhance_button.click()

                # Make photo realistic
                photo_realistic_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "make-photo-realistic"))
                )
                photo_realistic_button.click()

                # Wait for loading to finish
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element((By.ID, "loading-overlay"))
                )

                # Select model
                model_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "model_version"))
                )
                model_select.find_element(By.XPATH, "//option[@value='flux']").click()

                # Select size
                size_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "size"))
                )
                size_select.find_element(By.XPATH, "//option[@value='1024x1024']").click()

                # Generate images
                generate_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Generate Images')]"))
                )
                driver.execute_script("arguments[0].click();", generate_button)

                # Wait for image to be generated
                WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "download-image"))
                )

                # Get image URL
                image_element = driver.find_element(By.CSS_SELECTOR, "div.image-wrapper img")
                image_url = image_element.get_attribute("src")

                # Download image
                image_path = os.path.join(save_directory, f"generated_image_{i+1}.jpg")
                image_data = requests.get(image_url, verify=False).content
                with open(image_path, "wb") as handler:
                    handler.write(image_data)

                images.append(image_path)
                image_generated = True
                print(f"Image {i+1} downloaded successfully! Saved at {image_path}")
                
            except Exception as e:
                retry_count += 1
                print(f"Error generating image for prompt {i+1} (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    time.sleep(10)
                else:
                    print(f"Failed to generate image {i+1} after {max_retries} attempts. Skipping...")

    driver.quit()
    return images


def generate_audio(story_text, audio_path):
    tts = gTTS(story_text, lang='en')
    tts.save(audio_path)
    print(f"Audio generated successfully! Saved at {audio_path}")


def create_video(images, audio_path, video_path):
    if not images:
        raise ValueError("No images were generated. Cannot create video.")
    
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    # Use at least 8 images or the number of images we have
    num_images = max(8, len(images))
    duration_per_image = audio_duration / num_images

    # Duplicate last image if we don't have enough
    if len(images) < num_images:
        images += [images[-1]] * (num_images - len(images))

    clip = ImageSequenceClip(images, durations=[duration_per_image] * num_images)
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile(video_path, codec="libx264", fps=24)
    print(f"Video created successfully! Saved at {video_path}")


# Streamlit UI
st.set_page_config(page_title="Vision Diary", page_icon="📔", layout="centered")

st.title("📔 Vision Diary")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.header("Get Started With Vision Diary")
    st.write("Transform your daily stories into beautiful AI-generated videos!")
    st.write("Click the button below to start using the Vision Diary.")
    if st.button("Start", type="primary"):
        st.session_state.page = 'calendar'
        st.rerun()

elif st.session_state.page == 'calendar':
    st.header("Select a Date")
    selected_date = st.date_input("Choose a date", datetime.date.today())
    if st.button("Submit", type="primary"):
        st.session_state.page = 'input'
        st.session_state.selected_date = selected_date
        st.rerun()

elif st.session_state.page == 'input':
    st.header(f"📝 Diary Entry for {st.session_state.selected_date}")
    input_type = st.radio("Choose input type", ('Text', 'Audio'))
    
    if input_type == 'Text':
        diary_text = st.text_area("Enter your day's story", height=200, 
                                  placeholder="Write about your day...")
        
        if st.button("Generate Video", type="primary"):
            if not diary_text.strip():
                st.error("Please enter some text for your diary entry!")
            else:
                with st.spinner("Generating your video... This may take a few minutes."):
                    try:
                        save_directory = f"./{st.session_state.selected_date}"
                        if not os.path.exists(save_directory):
                            os.makedirs(save_directory)
                        
                        st.info("Step 1/4: Processing your story...")
                        prompts = generate_prompts(diary_text)
                        
                        st.info(f"Step 2/4: Generating {len(prompts)} images...")
                        images = generate_images(prompts, save_directory)
                        
                        if not images:
                            st.error("Failed to generate images. Please try again.")
                        else:
                            st.info("Step 3/4: Creating audio narration...")
                            audio_path = os.path.join(save_directory, f"{st.session_state.selected_date}_story_audio.mp3")
                            generate_audio(diary_text, audio_path)
                            
                            st.info("Step 4/4: Creating your video...")
                            video_path = os.path.join(save_directory, f"{st.session_state.selected_date}_story_video.mp4")
                            create_video(images, audio_path, video_path)
                            
                            st.success(f"✅ Video created successfully!")
                            st.video(video_path)
                            
                            # Provide download button
                            with open(video_path, "rb") as video_file:
                                st.download_button(
                                    label="Download Video",
                                    data=video_file,
                                    file_name=f"vision_diary_{st.session_state.selected_date}.mp4",
                                    mime="video/mp4"
                                )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        st.error("Please try again or contact support if the issue persists.")
    
    elif input_type == 'Audio':
        st.info("Audio upload feature - Coming soon!")
        st.write("Currently, only text input is supported for deployment.")

    if st.button("← Back to Calendar"):
        st.session_state.page = 'calendar'
        st.rerun()