import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime


# STEP 1: Get HTML from Internshala
def get_html(url):
    response = requests.get(url)
    return response.text


# STEP 2: Extract Job Listings
def get_jobs(html):
    soup = BeautifulSoup(html, 'html.parser')
    job_list = []

    job_cards = soup.find_all('div', class_='internship_meta')

    for card in job_cards:
        title_tag = card.find('div', class_='heading_4_5')
        company_tag = card.find('div', class_='company_name')
        link_tag = card.find('a')

        if title_tag and company_tag and link_tag:
            title = title_tag.text.strip()
            company = company_tag.text.strip()
            link = "https://internshala.com" + link_tag['href']
            job_list.append(f"{title} at {company} - {link}")

    return job_list


# STEP 3: Filter by Keywords
def filter_jobs(job_list, keywords):
    filtered = []
    for job in job_list:
        for word in keywords:
            if word.lower() in job.lower():
                filtered.append(job)
                break
    return filtered


# STEP 4: Send Email (Plain SMTP)
#import smtplib

def send_email(from_email, password, to_email, subject, body):
    # Build a plain email message
    email_text = (
        "From: " + from_email + "\n" +
        "To: " + to_email + "\n" +
        "Subject: " + subject + "\n\n" +
        body
    )

    # Create connection to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)  # 587 means STARTTLS (secure)

    server.starttls()  # Start encrypted connection
    server.login(from_email, password)  # Login with your Gmail + app password
    server.sendmail(from_email, to_email, email_text)  # Send the actual email
    server.close()  # Close the connection


# STEP 5: Main Script
def main():
    url = "https://internshala.com/internships"
    keywords = ["python", "developer", "remote"]  # Add your own
    from_email = "lovechess2736@gmail.com"  # Change this
    to_email = "g.ashutosh2502@gmail.com"  # Change this
    password = "xdvvxokxzsztvdhe"  # Use Gmail App Password

    html = get_html(url)
    jobs = get_jobs(html)
    matching_jobs = filter_jobs(jobs, keywords)

    if matching_jobs:
        body = "Here are the jobs matching your keywords:\n\n" + "\n".join(matching_jobs)
    else:
        body = "No matching jobs found today."

    now = datetime.now()
    subject = f"Job Alert - {now.strftime('%d %b %Y')}"

    send_email(from_email, password, to_email, subject, body)
    print("✅ Email sent!")


# Run it once
main()
