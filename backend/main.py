import requests
from bs4 import BeautifulSoup
import math

filtered_job_links = []
external_link_comp = []

def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name="a", attrs={"class":"result-card__full-card-link"}):
        jobs.append(div.text.strip())
    return jobs

def extract_company_from_result(soup):
    companies = []
    for div in soup.find_all(name="a", attrs={"class":"result-card__subtitle-link"}):
        companies.append(div.text.strip())
    return companies

def extract_location_from_result(soup):
    locations = []
    for div in soup.find_all(name="span", attrs={"class":"job-result-card__location"}):
        locations.append(div.text.strip())
    return locations

def extract_job_description_from_result(soup):
    descriptions = []
    for div in soup.find_all(name="p", attrs={"class":"job-result-card__snippet"}):
        descriptions.append(div.text.strip())
    return descriptions

def extract_salary_from_result(soup):
    salaries = []
    for div in soup.find_all(name="span", attrs={"class":"job-result-card__salary-info"}):
        salaries.append(div.text.strip())
    return salaries

def extract_job_links_from_result(soup):
    links = []
    for div in soup.find_all(name="a", attrs={"class":"result-card__full-card-link"}):
        links.append(div['href'])
    return links

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_titles = extract_job_title_from_result(soup)
    companies = extract_company_from_result(soup)
    locations = extract_location_from_result(soup)
    descriptions = extract_job_description_from_result(soup)
    salaries = extract_salary_from_result(soup)
    links = extract_job_links_from_result(soup)
    jobs = []
    for i in range(len(job_titles)):
        jobs.append({
            'title': job_titles[i],
            'company': companies[i],
            'location': locations[i],
            'description': descriptions[i],
            'salary': salaries[i],
            'link': links[i]
        })
    return jobs

if __name__ == '__main__':
    job_type = input("Enter job type (internship, entry-level, associate): ").strip().lower()
    keywords = input("Enter job keywords (e.g., software engineer): ").strip().lower()

    # Base URLs for each job type
    base_urls = {
        "internship": "https://www.linkedin.com/jobs/search/?currentJobId=3931759919&distance=25&f_E=1&f_TPR=r86400&keywords=information%20technology&location=&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true",
        "entry-level": "https://www.linkedin.com/jobs/search/?currentJobId=3931572926&distance=25&f_E=2&f_TPR=r86400&keywords=information%20technology&location=&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&start=25",
        "associate": "https://www.linkedin.com/jobs/search/?currentJobId=3922745482&distance=25&f_E=3&f_TPR=r86400&keywords=information%20technology&location=&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
    }

    job_type_mapping = {
        "internship": "1",
        "entry-level": "2",
        "associate": "3"
    }

    if job_type not in base_urls:
        print("Invalid job type selected.")
    else:
        # Replace keywords in the base URL
        search_url = base_urls[job_type].replace("information%20technology", keywords.replace(' ', '%20'))
        print(f"Scraping URL: {search_url}")
        
        # Make the initial request and parse the response
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find the job count and initial job ID
        job_count = soup.find(class_="results-context-header__job-count")
        iterator_query = int(job_count.text) if job_count else 0
        if iterator_query == 0:
            print("There are no available jobs for today.")
        else:
            job_cards = soup.find_all('div', class_='base-card')
            initial_job_id = None
            for card in job_cards:
                if 'data-entity-urn' in card.attrs:
                    initial_job_id = ''.join(filter(str.isdigit, card['data-entity-urn']))
                    break

            if initial_job_id is None:
                print("No initial job ID found.")
            else:
                # Fetch additional job listings
                target_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords.replace(' ', '%20')}&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&f_E={job_type_mapping[job_type]}&currentJobId={initial_job_id}&start={{}}"
                for i in range(0, math.ceil(iterator_query / 25)):
                    res = requests.get(target_url.format(i), headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    alljobs_on_this_page = soup.find_all("li")

                    for job in alljobs_on_this_page:
                        job_title = job.find('h3', class_='base-search-card__title')
                        if job_title:
                            job_title_text = job_title.text.strip()  # Preserve case for display
                            job_link = job.find('a', class_='base-card__full-link')['href']
                            filtered_job_links.append((job_title_text, job_link))

                        if len(filtered_job_links) >= 10:
                            break

                # Fetch external links
                for job_title, link in filtered_job_links:
                    res = requests.get(link, headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    external_link = soup.find(class_="sign-up-modal__direct-apply-on-company-site")
                    if external_link:
                        company_site_link = external_link.find('a', class_='sign-up-modal__company_webiste')
                        if company_site_link:
                            external_link_comp.append((job_title, company_site_link['href']))

                # Print the external links with job titles
                for job_title, link in external_link_comp:
                    print(f"{job_title}: {link}")
