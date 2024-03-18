# TamaCoachee - AI chatbot

Custom AI Chatbot, developed for S. Nouwen [TU/e: Promovendus ‘Real feelings for virtual humans’ - Human Technology Interaction] <br/>

## Features & Specs
- Context aware **AI Chatbot using OpenAI GPT-4**
- To be used in an educational environment to train **conversational techniques**
- **Text and speech** input
- Both **text and audio output**<br>
- Memory to have a smooth conversation where the AI **remembers past messages**<br>
- Generate feedback on the way the user has **interacted with the AI**<br>
- Download and export the final conversation **as a generated text file to Google Drive**<br>
- Automatic export of recorded and generated audio files per input/output **to Google Drive**<br>

TamaCoachee uses OpenAI's GPT-4 model, their audio model for TTS (Text to Speech) and Whisper for STT (Speech to Text).

Streamlit, as a free and open-source framework, is used to build this chatbot with interface, and to be able to rapidly deploy it through streamlit cloud for online usage.

## Setup & How to Use
**1.** Clone the repository: git clone https://github.com/dwltr/tamacoachee.git

**2.** Navigate to the project directory
```python
cd repository-name
```
**3.** Install the dependencies:
```python 
pip install -r requirements.txt
```
**4.** Run the Streamlit application (locally)
```
streamlit run main.py
```

## REMARKS
**1.** Key features are defined in seperate py files to make it more readable

**2.** Important sections in each file are accompanied with comments if needed

**3.** Code is written with some use of langchain to make the chatbot future proof for new functionalities if needed in the future

**4.** Code is written in a way that it's easy, with some basic knowledge of python, to change the connection to other AI model's

**5.** Within the seperate instruction.py file it's possible to build a different use case and provide the AI model with instructions to play a different role

## Links
The following models, frameworks and/or tools are used

**1.** Streamlit https://streamlit.io/

**2.** Langchain https://www.langchain.com/

**3.** OpenAI (model, stt and tts) https://openai.com/blog/gpt-4-api-general-availability

**4.** Google's Drive API and authentication https://developers.google.com/drive/api/guides/about-sdk