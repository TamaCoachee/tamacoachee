# EXPORT TO GOOGLE DRIVE FUNCTION

###########################################################
# IMPORTING NECESSARY LIBRARIES AND PACKAGES
###########################################################

from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import streamlit as st

from datetime import datetime

###########################################################
# DEFINING VARIABLES
###########################################################

SCOPES = ['https://www.googleapis.com/auth/drive']
#SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = st.secrets['PARENT_FOLDER_ID']
SERVICE_ACCOUNT_INFO = st.secrets['SERVICE_ACCOUNT_FILE']

###########################################################
# NECESSARY FUNCTIONS
###########################################################

# Authentication with Google

def authenticate():
    creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    return creds

# Upload to drive function

def upload_file(filename):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : filename,
        'parents' : [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=filename
    ).execute()

# Conversion from data to csv file with specific name and timestamp

def csv_conv(conversation_file, studentnumber):
  filename = studentnumber
  timestamp = datetime.now()
  timestring = timestamp.strftime("%Y_%m_%d_%H%M%S")
  
  csv_file = conversation_file.to_csv(f'{filename}_{timestring}_conv_file.csv', index=False)
  
  #Let user download conversation file?
  open(f'{filename}_{timestring}_conv_file.csv')
  
  #call upload_file function:
  upload_file(f'{filename}_{timestring}_conv_file.csv')
  #upload_file('Tamacoachee_conv_.csv')
  
def csv_fb(feedback_file, studentnumber):
  filename = studentnumber
  timestamp = datetime.now()
  timestring = timestamp.strftime("%Y_%m_%d_%H%M%S")
  
  csv_file = feedback_file.to_csv(f'{filename}_{timestring}_fb_file.csv', index=False)
  
  #Let user download conversation file?
  open(f'{filename}_{timestring}_fb_file.csv')
  
  #call upload_file function:
  upload_file(f'{filename}_{timestring}_fb_file.csv')
