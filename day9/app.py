from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def scrape_berlinstartupjobs(search_term):
    base_url = f"https://berlinstartupjobs.com/skill-areas/{search_term}/"
    response = requests.get(
        base_url,
        verify=False,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    
    job_listings = soup.find_all("li", class_="bjs-jlid")
    for job in job_listings:
        title = job.find("h4").text.strip()
        company = job.find("a", class_="bjs-jlid__b").text.strip()
        description = job.find("div", class_="bjs-jlid__description").text.strip()
        link = job.find("h4").find("a")["href"]
        
        jobs.append({
            "title": title,
            "company": company,
            "description": description,
            "link": link,
            "source": "Berlin Startup Jobs"
        })
    
    return jobs

def scrape_web3career(search_term):
    base_url = f"https://web3.career/{search_term}-jobs"
    response = requests.get(
        base_url,
        verify=False,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    
    job_listings = soup.find_all("tr", class_="table_row")
    for job in job_listings:
        try:
            title_elem = job.find("h2")
            company_elem = job.find("h3")
            description_elem = job.find("td", class_="job_description")
            link_elem = job.find("a")
            
            if title_elem and company_elem and description_elem and link_elem:
                title = title_elem.text.strip()
                company = company_elem.text.strip()
                description = description_elem.text.strip()
                link = link_elem["href"]
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "description": description,
                    "link": link,
                    "source": "Web3 Career"
                })
        except Exception as e:
            print(f"Error parsing Web3 Career job: {e}")
            continue
    
    return jobs

def scrape_weworkremotely(search_term):
    base_url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={search_term}"
    response = requests.get(
        base_url,
        verify=False,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    
    job_listings = soup.find_all("li", class_="feature")
    for job in job_listings:
        title = job.find("span", class_="title").text.strip()
        company = job.find("span", class_="company").text.strip()
        description = job.find("span", class_="region").text.strip()
        link = "https://weworkremotely.com" + job.find("a")["href"]
        
        jobs.append({
            "title": title,
            "company": company,
            "description": description,
            "link": link,
            "source": "We Work Remotely"
        })
    
    return jobs

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    search_term = request.args.get("q", "")
    if not search_term:
        return jsonify([])
    
    all_jobs = []
    all_jobs.extend(scrape_berlinstartupjobs(search_term))
    all_jobs.extend(scrape_web3career(search_term))
    all_jobs.extend(scrape_weworkremotely(search_term))
    
    return jsonify(all_jobs)

if __name__ == "__main__":
    app.run(debug=True) 