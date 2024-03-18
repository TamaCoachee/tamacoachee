# SPEECH TO TEXT FUNCTION

################################################################
# IMPORTING NECESSARY LIBRARIES AND PACKAGES
################################################################

from streamlit_mic_recorder import mic_recorder
import streamlit as st
import io
from openai import OpenAI
from datetime import datetime
from drive_function import upload_file # to export audiofile to google drive

import os

################################################################
# RECORDING AUDIO FROM USER AND RETURN TRANSCRIPT USING WHISPER
################################################################

def WhisperSTT(openai_api_key=None,start_prompt="Start recording",stop_prompt="Stop recording",just_once=True,use_container_width=True,language=None,callback=None,args=(),kwargs={},key=None):
    if not 'openai_client' in st.session_state:
        st.session_state.openai_client=OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    if not '_last_speech_to_text_transcript_id' in st.session_state:
        st.session_state._last_speech_to_text_transcript_id=0
    if not '_last_speech_to_text_transcript' in st.session_state:
        st.session_state._last_speech_to_text_transcript=None
    if key and not key+'_output' in st.session_state:
        st.session_state[key+'_output']=None

    if "user_audio_files" not in st.session_state:
        st.session_state["user_audio_files"] = []

    audio = mic_recorder(start_prompt=start_prompt,stop_prompt=stop_prompt,just_once=just_once,use_container_width=use_container_width,key=key)
    new_output=False
    if audio is None:
        output=None
    else:
        id=audio['id']
        new_output=(id>st.session_state._last_speech_to_text_transcript_id)
        if new_output:
            output=None
            st.session_state._last_speech_to_text_transcript_id=id
            
            audiofile = audio['bytes']
            st.session_state.user_audio_files.append(audiofile)
            
            audio_BIO = io.BytesIO(audio['bytes'])
            audio_BIO.name='audio.mp3'
            success=False
            err=0
            ##############################
            # audio_to_export = audio['bytes'] #this is the audio file to export to google drive
            
            # with open("audio.mp3", "wb") as audio_file:
            #     audio_file.write(audio_to_export)
            #     upload_file("audio.mp3")
            ##############################
            while not success and err<3: #Retry up to 3 times in case of OpenAI server error.
                try:
                    transcript = st.session_state.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_BIO,
                        language=language
                    )
                except Exception as e:
                    print(str(e)) # log the exception in the terminal
                    err+=1
                else:
                    success=True
                    output=transcript.text
                    st.session_state._last_speech_to_text_transcript=output
        elif not just_once:
            output=st.session_state._last_speech_to_text_transcript
        else:
            output=None

    if key:
        st.session_state[key+'_output']=output
    if new_output and callback:
        callback(*args,**kwargs)
    return output

################################################################
# EXPORTING USER AUDIO (SPEECH) TO GOOGLE DRIVE
################################################################

def user_audio_export(studentnumber):
    if not st.session_state.user_audio_files:
        pass
    else:
        audio_to_export = list(st.session_state.user_audio_files)[-1] #this is the audio file to export to google drive
    
        timestamp = datetime.now()
        timestring = timestamp.strftime("%Y_%m_%d_%H%M%S")        
        with open(f'{studentnumber}_{timestring}_user_audio.wav', "wb") as audio_file:
            audio_file.write(audio_to_export)
            upload_file(f'{studentnumber}_{timestring}_user_audio.wav')
        st.session_state["user_audio_files"] = [] # with this the most recent user audio file gets cleaned up after being exported to google drive