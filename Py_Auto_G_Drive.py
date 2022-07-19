import requests
import os
from progress.bar import ChargingBar
import time

def dowloadFile(path, url, name):
    print('---------------------------------------')
    print("Now downloading: ",name)
    r = requests.get(url, stream=True)
    # count = 0
    # if int(r.headers.get('content-length')) <= 0:
    #     while int(r.headers.get('content-length')) <= 0 or count <=30:
    #         time.sleep(1)
    #         count += 1
    #         r = requests.get(url, stream=True)
    # print(r.headers)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        expected_len_in_MB = round(total_length/(1024*1024), 2)
        print('Size: ',expected_len_in_MB, ' MB')
        for chunk in ChargingBar('Downloading', max=(total_length/1024),  bar_prefix = ' |', bar_suffix = '| ', empty_fill = ' ',suffix=' %(percent)d%%  [%(index)d/%(max)d]  [%(eta_td)s]', color = 'green').iter(r.iter_content(1024)):
            if chunk:
                f.write(chunk)
                f.flush()

def overWriteToDownload(path, start, end):
    with open(path,'r') as downloadTextOverWrite:
        listOfFileNames = downloadTextOverWrite.readlines()
    with open('D:\\Engg\\Project_drive_auto_download\\Download.txt','w') as downloadText:
        downloadText.writelines(listOfFileNames[start-1:end])
        # print(listOfFileNames[start-1:end])

with open('D:\\Engg\\Project_drive_auto_download\\input.txt','r') as inputFile:
    inputList = inputFile.readlines()
    
downloadPath = inputList[0][:-1]
pathToLinks = inputList[1][:-1]
# downloadPath = input('Enter the Download location : ')
if downloadPath[0] == '\"' and downloadPath[-1] == '\"':
    downloadPath = downloadPath[1:-1]
print()
# pathToLinks = input('Enter the path to download links file : ')
if pathToLinks[0] == '\"' and pathToLinks[-1] == '\"':
    pathToLinks = pathToLinks[1:-1]
print()
startFile = int(input('Enter the Starting file number to download : '))
endFile = int(input('Enter the ending file number to download : '))

overWriteToDownload(path=pathToLinks, start = startFile, end = endFile)

with open('D:\\Engg\\Project_drive_auto_download\\Download.txt','r') as downloadText:
    listOfFileNames = downloadText.readlines()
    fileNames = []
    downloadLinks = []
    for i in range(len(listOfFileNames)):
        a = listOfFileNames[i].split(" => ")
        fileNames.append(a[0])
        downloadLinks.append(a[1][:-1])
    # print(fileNames)
    # print(downloadLinks)

for name, link in zip(fileNames, downloadLinks):
    dowloadFile(os.path.join(downloadPath,name), link, name=name)
