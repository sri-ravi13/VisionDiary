import os
import datetime
import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    service = Service(r"C:\Windows\chromedriver-win64\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://aicreate.com/text-to-image-generator/")

    for i, prompt in enumerate(prompts):
        image_generated = False
        while not image_generated:
            try:

                prompt_input = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "caption"))
                )
                prompt_input.clear()
                prompt_input.send_keys(prompt)


                enhance_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "enhance-prompt"))
                )
                enhance_button.click()


                photo_realistic_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "make-photo-realistic"))
                )
                photo_realistic_button.click()


                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element((By.ID, "loading-overlay"))
                )


                model_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "model_version"))
                )
                model_select.find_element(By.XPATH, "//option[@value='flux']").click()


                size_select = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "size"))
                )
                size_select.find_element(By.XPATH, "//option[@value='1024x1024']").click()


                generate_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Generate Images')]"))
                )
                driver.execute_script("arguments[0].click();", generate_button)


                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "download-image"))
                )


                image_element = driver.find_element(By.CSS_SELECTOR, "div.image-wrapper img")
                image_url = image_element.get_attribute("src")


                download_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "download-image"))
                )
                driver.execute_script("arguments[0].click();", download_button)


                image_path = os.path.join(save_directory, f"generated_image_{i+1}.jpg")
                image_data = requests.get(image_url, verify=False).content
                with open(image_path, "wb") as handler:
                    handler.write(image_data)

                images.append(image_path)
                image_generated = True
                print(f"Image {i+1} downloaded successfully! Saved at {image_path}")
            except Exception as e:
                print(f"Error generating image for prompt {i+1}: {e}. Retrying...")
                time.sleep(10)

    driver.quit()
    return images


def generate_audio(story_text, audio_path):
    tts = gTTS(story_text, lang='en')
    tts.save(audio_path)
    print(f"Audio generated successfully! Saved at {audio_path}")


def create_video(images, audio_path, video_path):
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration


    num_images = max(8, len(images))
    if len(images) < num_images:
        print(f"Warning: Less than {num_images} images found. Using {len(images)} images.")

    duration_per_image = audio_duration / num_images


    images += [images[-1]] * (num_images - len(images))

    clip = ImageSequenceClip(images, durations=[duration_per_image] * num_images)
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile(video_path, codec="libx264", fps=24)
    print(f"Video created successfully! Saved at {video_path}")


st.title("Vision Diary")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.header("Get Started With Vision Diary")
    st.write("Click the button below to start using the Vision Diary.")
    if st.button("Start"):
        st.session_state.page = 'calendar'

elif st.session_state.page == 'calendar':
    st.header("Select a Date")
    selected_date = st.date_input("Choose a date", datetime.date.today())
    if st.button("Submit"):
        st.session_state.page = 'input'
        st.session_state.selected_date = selected_date

elif st.session_state.page == 'input':
    st.header(f"Diary Entry for {st.session_state.selected_date}")
    input_type = st.radio("Choose input type", ('Text', 'Audio'))
    
    if input_type == 'Text':
        diary_text = st.text_area("Enter your day's story")
        if st.button("Generate Video"):
            save_directory = f"./{st.session_state.selected_date}"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            prompts = generate_prompts(diary_text)
            images = generate_images(prompts, save_directory)
            audio_path = os.path.join(save_directory, f"{st.session_state.selected_date}_story_audio.mp3")
            video_path = os.path.join(save_directory, f"{st.session_state.selected_date}_story_video.mp4")
            generate_audio(diary_text, audio_path)
            create_video(images, audio_path, video_path)
            st.success(f"Video created! Saved at {video_path}")
            st.video(video_path)
    
    elif input_type == 'Audio':
        audio_file = st.file_uploader("Upload your audio file", type=["mp3"])
        if st.button("Generate Video") and audio_file is not None:
            save_directory = f"./{st.session_state.selected_date}"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            audio_path = os.path.join(save_directory, f"{st.session_state.selected_date}_story_audio.mp3")
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
            prompts = [f"{prompt_text}."]
            images = generate_images(prompts, save_directory)
            video_path = os.path.join(save_directory, f"{st.session_state.selected_date}_story_video.mp4")
            create_video(images, audio_path, video_path)
            st.success(f"Video created! Saved at {video_path}")
            st.video(video_path)
