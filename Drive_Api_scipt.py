from __future__ import print_function

import io
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def getCreds():
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    
    CLIENT_SECRET_FILE = 'client_secret_credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE,SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json','w') as token:
            token.write(creds.to_json())
    return creds

# def displayProgress():
#     while True:
#         time.sleep(1)
#         global file
#         size = file.getbuffer().nbytes
#         print(file.getbuffer().nbytes, end='\r')
#         if size >200000:
#             break

def download_file(fileName,real_file_id):
    try:
        # create gmail api client
        service = build('drive','v3',credentials=getCreds())

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        # t1 = threading.Thread(target=displayProgress)
        # t1.start()
        print('Now downloading :', fileName)
        print('Wait for download to complete')
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print("Downloaded %d%%. " % int(status.progress() * 100), end='\r')
        # t1.join()

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None
    
    return file.getvalue()

def overWriteToDownload(path, start, end):
    with open(path,'r') as downloadTextOverWrite:
        listOfFileNames = downloadTextOverWrite.readlines()
    with open('D:\\Engg\\Project_drive_auto_download\\FileID\'s.txt','w') as downloadText:
        downloadText.writelines(listOfFileNames[start-1:end])

if __name__ == '__main__':

    with open('D:\\Engg\\Project_drive_auto_download\\input.txt','r') as inputFile:
        inputList = inputFile.readlines()
    
    downloadPath = inputList[0][:-1]
    pathToId = inputList[1][:-1]
    # downloadPath = input('Enter the Download location : ')
    if downloadPath[0] == '\"' and downloadPath[-1] == '\"':
        downloadPath = downloadPath[1:-1]
    print()
    # pathToId = input('Enter the path to File ID\'s : ')
    if pathToId[0] == '\"' and pathToId[-1] == '\"':
        pathToId = pathToId[1:-1]
    print()
    startFile = int(input('Enter the Starting file number to download : '))
    endFile = int(input('Enter the ending file number to download : '))

    overWriteToDownload(pathToId, startFile, endFile)

    with open('D:\\Engg\\Project_drive_auto_download\\FileID\'s.txt','r') as downloadText:
        listOfFileNames = downloadText.readlines()
        fileNames = []
        fileIDs = []
        for i in range(len(listOfFileNames)):
            a = listOfFileNames[i].split(" => ")
            fileNames.append(a[0])
            fileIDs.append(a[1][:-1])
        # print(fileNames)
        # print(downloadLinks)

    for name, id in zip(fileNames, fileIDs):
        print('------------------------------------------')
        data = download_file(fileName=name, real_file_id=id)
        with open(os.path.join(downloadPath,name),'wb') as mkv:
            mkv.write(data)
        mkv.close()
        print('\nDownload Complete.\n')
    
    