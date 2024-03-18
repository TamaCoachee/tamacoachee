# TEXT TO SPEECH FUNCTION

################################################################
# IMPORTING NECESSARY LIBRARIES AND PACKAGES
################################################################

from openai import OpenAI
import streamlit as st
import os
import base64
from datetime import datetime

from stt_function import user_audio_export

from drive_function import upload_file

################################################################
# DEFINING THE OPEN AI AUDIO MODEL CLIENT USING API
################################################################

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

################################################################
# TEXT TO SPEECH FUNCITON
################################################################

def tts(full_response, studentnumber):
    audio_response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    response_format="aac",
    input=full_response,
    )
    audio_content = audio_response.content
    
    # Decode audio to enable autoplay in browser without consent by user
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
    audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)
    audio_tag = None
    
    # Display play buttons for audio file
    # st.audio(audio_content)
    
    # EXPORT AI RESPONSE AUDIO TO GOOGLE DRIVE AFTER PLAYBACK AUDIO
    
    AI_audio_to_export = audio_content #this is the audio file to export to google drive
    timestamp = datetime.now()
    timestring = timestamp.strftime("%Y_%m_%d_%H%M%S")
    
    with open(f'{studentnumber}_{timestring}_ai_audio.aac', "wb") as audio_file:
        audio_file.write(AI_audio_to_export)
        upload_file(f'{studentnumber}_{timestring}_ai_audio.aac')
    
    # user_audio_export(studentnumber)