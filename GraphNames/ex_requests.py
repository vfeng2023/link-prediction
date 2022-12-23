# from cgitb import html
import requests
from bs4 import BeautifulSoup
import typing

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

# print(page.text)
soup = BeautifulSoup(page.content,"html.parser")
results = soup.find(id="ResultsContainer")
# print(results.prettify())
job_el = results.find_all("h2",string=lambda text: "python" in text.lower())#"Python")# )
py_jobs = [r.parent.parent.parent for r in job_el]
print(len(job_el))
# print(job_el)
for job_element in py_jobs:
    # print(job,end="\n\n")
    # print(job_element.prettify())
    title_element = job_element.find("h2", class_="title")
    # print(title_element)
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
    links = job_element.find_all("a")
    for link in links:
        link_url = link['href']
        # print(link_url)
        if "fake-jobs" in link_url.lower():
            print("Apply here: ",link_url)