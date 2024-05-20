
# Tamacoachee Chatbot v1.0

###########################################################
# IMPORTING NECESSARY LIBRARIES AND PACKAGES
###########################################################

import os
import pandas as pd
import streamlit as st
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.prompts import ChatPromptTemplate

import instructions

from stt_function import WhisperSTT, user_audio_export
from tts_function import tts


from drive_function import csv_conv, csv_fb

###########################################################
# API KEYS
###########################################################

apikey = st.secrets['OPENAI_API_KEY']

###########################################################
# CREATING PARSING INSTRUCTIONS FOR THE AI FEEDBACK OUTPUT
###########################################################

from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

posfb_schema = ResponseSchema(name="posfb",
                                    description="This is the positive feedback")
negfb_schema = ResponseSchema(name="negfb",
                                description="This is the negative feedback")
response_schemas = [posfb_schema, negfb_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()

###########################################################
# CREATING PROMPT TEMPLATES FOR AI INSTRUCTIONS
###########################################################

# The prompt instruction for the system is derived from a seperate file to keep this code clean.
# The instruction includes reference to the format instructions to get json output for parsing.

sys_prompt = PromptTemplate(
    input_variables=["original_sentence", "desired_language"],
    template = instructions.instruction_text3
)

system_message_prompt = SystemMessagePromptTemplate(prompt=sys_prompt)


# Creating the human prompt template
student_prompt = PromptTemplate(
    input_variables=["input"],
    template="{input}"
)
student_message_prompt = HumanMessagePromptTemplate(prompt=student_prompt)


# Putting the prompt templates together for the entire chat prompt. 
# This includes the instruction for the AI to stay in the specific role.

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, student_message_prompt])

###########################################################
# DEFINING THE LLM MODEL(s)
###########################################################

# Defining the OpenAI model as client (this one is used to stream conversational output)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

system_prompt = instructions.instruction_text2

# Define the OpenAI language model to give feedback on the conversation
llm=ChatOpenAI(model_name='gpt-4', openai_api_key = apikey,
             temperature=0.5,
             )

# Create the LLM chain to put the feedback model and chat prompt together
chain = LLMChain(llm=llm, prompt=chat_prompt)

###########################################################
# CHATBOT INTERFACE
###########################################################

# Display the chat history
def create_chat_area(chat_history):
    for chat in chat_history:
        if chat['role'] == 'system': continue
        role = chat['role']
        with st.chat_message(role):
            st.write(chat['content'])

############ Chat-GPT solution #############
# Initialize session state for button
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

def record_audio():
    st.session_state['button_clicked'] = True
    audio_data = st.audio_input("Record your message")
    if audio_data:
        # Process the audio data
        st.write("...")
############ Chat-GPT solution #############

# Main function to run the Streamlit app
def main():
    # Streamlit settings
    
    st.set_page_config(page_title="Tamacoachee", layout="centered", initial_sidebar_state="expanded")
    st.header("Chat met Tamacoachee v1.0")

    # Introduction text
    col1, mid, col2 = st.columns([320,1,180])
    with col2:
        st.image('tamacoachee_small_circle.png', use_column_width='äuto', width=180)
    with col1:
        st.write(
    """
    👋 20/5/'24 Welkom bij Tamacoachee. Je neemt in dit gesprek de rol aan van een coach.
    Anna komt bij je langs om de problemen te bespreken die zij ervaart gedurende haar studie. Probeer te achterhalen waar ze tegenaan loopt, en help haar verder opweg.
    Je kan je antwoorden inspreken met de knop "Start recording" of typen.
    Je kan het gesprek afronden met de knop "Genereer feedback"
    Het kan soms even duren voordat je antwoord er is. Bovenin zie je een indicatie dat het systeem nog bezig is.
    """
    )
        st.markdown(''':red[Vul links je studentnummer in om het gesprek te kunnen starten!]''')
    
    st.divider()  
    
    
                
    # Session state initialization to store chat history, messages and streaming
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{"role": "system", "content": system_prompt}]
    if 'streaming' not in st.session_state:
        st.session_state.streaming = False
    if 'feedback_history' not in st.session_state:
        st.session_state.feedback_history = []
        
    # API key setup if not present
    apikey = os.environ.get("OPENAI_API_KEY")
    if apikey is None:
        with st.sidebar:
            st.subheader("Instellingen")
            apikey = st.text_input("Vul hier je OpenAI API key in:", type="password")
    elif apikey:
        run_chat_interface()
    else:
        st.error("Vul hier je API key in om de chat te starten")

# Run the chat interface within Streamlit
def run_chat_interface():
    
    # Conversation control buttons in sidebar
    with st.sidebar:
        studentnumber = st.text_input(
            "Voer je studentnummer in 👇",
            placeholder='123456',
        )    
        st.markdown('---')
                
        # drive_button = st.button("Download gesprek")
        feedback_button = st.button("Genereer feedback") 
    
    global filename_complete
    global filename_complete_fb
    filename_complete = f'{studentnumber}_conv_file'
    filename_complete_fb = f'{studentnumber}_fb_file'
    
    # Export conversation to Google Drive via specific download button
    
    # if drive_button:
    #     conversation_file = pd.DataFrame(st.session_state.chat_history[1:])
    #     csv_conv(conversation_file, filename_complete)
    # else:
    #     pass
    
    # create_chat_area(st.session_state.chat_history)
    create_chat_area(st.session_state.chat_history)
    
    # Display User text input field
    if studentnumber:    
        user_input = st.chat_input("Stel hier je vraag")
    else:
        pass
    
    
    # Display User speech record button
    if studentnumber:

        ############ Chat-GPT solution #############
       # text=WhisperSTT(openai_api_key=apikey, language='nl')
        if not st.session_state['button_clicked']:
            if st.button('Record Audio'):
                record_audio()
        else:
           # st.write("Audio has been recorded.")
            if st.button('Record Again'):
                st.session_state['button_clicked'] = False

        ############ Chat-GPT solution #############
    else:
        pass
    
        
    # Generate feedback on conversation
    if feedback_button:
        fb_content = st.session_state.chat_history # this gives feedback on the entire chat history
        feedback = chain.run(input=fb_content, format_instructions=format_instructions)
        parsed_feedback = output_parser.parse(feedback)
        with st.sidebar:
            container = st.container()
            container.write("Top: " + parsed_feedback["posfb"] + "\n\nTip: " + parsed_feedback["negfb"])
        
        st.session_state.feedback_history.append({"posfb": parsed_feedback["posfb"], "negfb": parsed_feedback["negfb"]})
            
        conversation_file = pd.DataFrame(st.session_state.chat_history[1:])
        csv_conv(conversation_file, studentnumber)
        
        feedback_file = pd.DataFrame(st.session_state.feedback_history)
        csv_fb(feedback_file, studentnumber)
        
        
    else:
        pass
                    


    # Handle user text input and generate AI response
    if studentnumber:
        if user_input:
            process_user_input(user_input, studentnumber)
    else:
        pass
        
    # Handle user speech input and generate AI response
    if studentnumber:
         ############ Chat-GPT solution #############
        text=WhisperSTT(openai_api_key=apikey, language='nl')
         ############ Chat-GPT solution #############
        if text:
            process_user_speech(text, studentnumber)
    else:
        pass

###########################################################
# Generate AI response functions
###########################################################


def process_user_speech(text, studentnumber):
    if text:
        user_audio_export(studentnumber)
        st.session_state.chat_history.append({"role": "user", "content": text})
        with st.chat_message("user"):
            st.markdown(text)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
        #st.rerun() 

        # Auto generate audio from response with the use of external function py file:
        full_response = list(st.session_state.chat_history)[-1]["content"]
        tts(full_response, studentnumber)    
           
    else:
        pass

        
def process_user_input(user_input, studentnumber):
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
        #st.rerun()
        
        # Auto generate audio from response with the use of external function py file:
    
        full_response = list(st.session_state.chat_history)[-1]["content"]
        tts(full_response, studentnumber)
        
    else:
        pass
        
        
if __name__ == '__main__':
    main()
