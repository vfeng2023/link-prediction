"""
Scrapes each of the pages for character names
"""
import requests
from bs4 import BeautifulSoup
import re
import pickle
import sys
# myurl = "https://tolkiengateway.net/wiki/Aegnor"
# ids of characters is /wiki/--- link for now

URLStem = "https://tolkiengateway.net" # URL Stem
characterNames = pickle.load(open('allowed_names.pkl','rb')) #set of valid links
def getLinks(url,file_=sys.stdout):
    page = requests.get(url) # get page
    soup = BeautifulSoup(page.content,"html.parser")
    # ge the title 
    title = soup.find('h1',id="firstHeading").get_text().strip()
    print(title,end=",",file=file_)
    subsec = soup.find('div',id="bodyContent")
    # print(subsec.get_text())
    # find all of the URLS
    links = subsec.find_all('a')
    stem = re.compile(r'/wiki/.+')
    for l in links:
        if l.has_attr('href'):
            mystem=re.search(stem,l['href'])
            if mystem is not None:
                ml = mystem[0]
                if ml in characterNames:
                    print(ml,file=file_,end=",")
    print(file=file_)
print("Total characters: ",len(characterNames))
with open('graphValues.txt',"w") as myFile:
    count = 0
    for c in characterNames: 
        myurl = URLStem + c
        
        print(c,end=",",file=myFile)
        getLinks(myurl,file_=myFile)# myFile)
        count += 1
        if count%100==0:
            print(count, " completed")
        print(c, " done!")

    myFile.close()
    # format: my Id, title, IDs of connected characters