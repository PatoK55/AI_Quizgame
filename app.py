import openai
import os
import streamlit as st
#from config import OPENAI_API_KEY
os.environ['OPENAI_API_KEY']

api_key = os.getenv('OPENAI_API_KEY')

openai.api_key = api_key
client = openai.OpenAI()

# Function to get story completion
def get_story_completion(prompt, target_audience):
    system_msg = 'Du bist ein Assistent der gutgelaunte Geschicht schreibt die immer zwischen 50 und 100 Wörter hat.'
    user_msg = f'Schreib {target_audience}-geschichte zu folgendem Titel: {prompt}'

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )
    if response and response.choices:
        completion = response.choices[0].message.content.strip()
        # Ensure the story length is between 50 and 100 words
        words = completion.split()
        if len(words) < 50:
            return completion + " " + " ".join(words[:50 - len(words)])
        elif len(words) > 100:
            return " ".join(words[:100])
        else:
            return completion
    else:
        st.error("Empty response from OpenAI.")
        return None

# Function to generate image
def generate_image(prompt, target_audience):
    #client = openai.OpenAI()
    response = client.images.generate(
        model="dall-e-2",
        prompt=f'{target_audience}-bild zu folgender Geschichte: {prompt}',
        size="256x256",
        quality="standard",
        n=1,
    )
    if response and response.data and len(response.data) > 0:
        return response.data[0].url
    else:
        st.error("Error generating image from OpenAI.")
        return None

# Initialize session state
def initialize_session_state():
    session_state = st.session_state
    session_state.user_story = ""
    session_state.story_completion = ""
    session_state.image_url = ""
    session_state.story_target = "Kinder"

# Main function
def main():
    st.set_page_config(
        page_title="Fraunhofer Austria Story App",
        page_icon="icon.png",
    )

    # Custom CSS for the buttons
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
    }
    .centered {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session variables if they do not exist
    if 'user_story' not in st.session_state:
        initialize_session_state()

    # Title and description
    st.image("logo.png")
    st.title("Geschichtenerzähler")
    
    # Dropdown to select story target audience
    st.write("Zielpublikum für die Geschichte:")
    st.session_state.story_target = st.selectbox("Zielpublikum", ["Kinder", "Erwachsene"])

    # User input for the story
    st.write("Bitte geben Sie unten den Titel ihrer Geschichte ein:")
    user_story = st.text_area("Titel", height=50)

    if st.button('Geschichte und Bild erstellen'):
        if user_story.strip() != "":
            target_audience = st.session_state.story_target
            completion = get_story_completion(user_story, target_audience)
            if completion:
                st.session_state.story_completion = completion
                st.subheader("Geschichte:")
                st.write(completion)

                # Generate an image based on the completed story
                image_prompt = completion
                image_url = generate_image(image_prompt, target_audience)
                if image_url:
                    st.session_state.image_url = image_url
                    # Center the image using custom HTML
                    st.markdown(f'<div class="centered"><img src="{image_url}" alt="Generated Image"></div>', unsafe_allow_html=True)
        else:
            st.warning("Zuerst Titel eingeben.")

    if st.button('Reset'):
        initialize_session_state()
        st.experimental_rerun()

if __name__ == '__main__':
    main()