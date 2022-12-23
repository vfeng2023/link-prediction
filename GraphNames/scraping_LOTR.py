import requests
from bs4 import BeautifulSoup
import sys
# myURL = "https://tolkiengateway.net/wiki/Category:Characters_in_The_Hobbit"
# page = requests.get(myURL)
# print(page.text)

def getPage(page,file_=sys.stdout):
    soup = BeautifulSoup(page.content,"html.parser")
    # print(soup)
    cl = soup.find("tr",valign="top")
    # if cl is None:
    #     cl = soup.find(id="")
    character_links = cl.find_all('a')
    print(len(character_links))
    for c in character_links:
        # print(c.prettify())
        link = c['href']
        # keep link if the first and last characters match and there isn't a semicolon 
        print(link,file=file_)
        # print()
# getPage(page)

# myURLlist = [
#     "https://tolkiengateway.net/wiki/Category:Characters_in_The_Hobbit",
#     "https://tolkiengateway.net/wiki/Category:Characters_in_The_Lord_of_the_Rings",
#     "https://tolkiengateway.net/w/index.php?title=Category:Characters_in_The_Silmarillion",
#     "https://tolkiengateway.net/w/index.php?title=Category:Characters_in_The_Silmarillion&pagefrom=Tulkas#mw-pages",

# ]
# for myURL in myURLlist:
#     start = myURL.rfind(":")
#     fname = myURL[start+1:]
#     with open(fname+".txt","w") as f:
#         page = requests.get(myURL)
#         getPage(page,file_=f)
#         f.close()
#     print("Done with: ",fname)

########## NOW: GETTING LOCATION NAMES #######################
myURL = "https://tolkiengateway.net/wiki/Index:Locations"
start = myURL.rfind(":")
fname = myURL[start+1:]
with open(fname+".txt","w") as f:
    page = requests.get(myURL)
    getPage(page,file_=f)
    f.close()
print("Done with: ",fname)