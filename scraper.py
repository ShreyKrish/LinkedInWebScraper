import requests
from bs4 import BeautifulSoup

def perform_scrape(job_type, keywords):
    filtered_job_links = []

    # Base URLs for each job type
    base_urls = {
        "internship": "https://www.linkedin.com/jobs/search/?distance=25&f_E=1&f_TPR=r86400&keywords=information%20technology&location=&refresh=true",
        "entry-level": "https://www.linkedin.com/jobs/search/?distance=25&f_E=2&f_TPR=r86400&keywords=information%20technology&location=&refresh=true",
        "associate": "https://www.linkedin.com/jobs/search/?distance=25&f_E=3&f_TPR=r86400&keywords=information%20technology&location=&refresh=true"
    }

    if job_type not in base_urls:
        return {"error": "Invalid job type selected."}

    # Generate search URL
    search_url = base_urls[job_type].replace("information%20technology", keywords.replace(' ', '%20'))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    
    # Request the search URL
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Extract job count
    job_count_elem = soup.find(class_="results-context-header__job-count")
    if job_count_elem:
        job_count_text = job_count_elem.text.strip().replace(',', '').replace('+', '')
        try:
            job_count = int(job_count_text)
        except ValueError:
            job_count = 0
    else:
        job_count = 0

    if job_count == 0:
        return {"error": "There are no available jobs for today."}

    # Extract job postings
    job_cards = soup.find_all('div', class_='base-card')
    for card in job_cards:
        job_title_elem = card.find('h3', class_='base-search-card__title')
        job_link_elem = card.find('a', class_='base-card__full-link')
        if job_title_elem and job_link_elem:
            job_title = job_title_elem.text.strip()
            job_link = job_link_elem['href']
            filtered_job_links.append((job_title, job_link))

        if len(filtered_job_links) >= 10:
            break

    # Final result should be a list of tuples (job title, job link)
    return filtered_job_links
