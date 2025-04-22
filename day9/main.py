# BLUEPRINT | DONT EDIT

import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://berlinstartupjobs.com/engineering/", verify=False,
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

skills = ["python", "typescript", "javascript", "rust"]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:


urls = []
urls.append("https://berlinstartupjobs.com/engineering/")

def get_page_number(soup):
    page_number = soup.find_all("a", class_="page-numbers")
    return len(page_number)

def pagination():
    page_number = get_page_number(soup)
    if page_number > 1:
        for i in range(2, page_number + 1):
            urls.append(f"https://berlinstartupjobs.com/engineering/page/{i}/")

soup = BeautifulSoup(response.content, "html.parser")
pagination()
all_jobs = []
for url in urls:
    response = requests.get(
    url, verify=False,
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("div", class_="bsj-template__b").find_all("li")
    for job in jobs:
        title = job.find("h4").text
        company = job.find("a", class_="bjs-jlid__b").text
        description = job.find("div", class_="bjs-jlid__description").text
        link = job.find("h4").find('a')["href"]
        job_data = {
            "title": title,
            "company": company,
            "description": description,
            "link": link
        }
        all_jobs.append(job_data)
    
print(all_jobs)

# /YOUR CODE