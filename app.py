import time, re, pyperclip, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from find_contact import *
from pyhunter import PyHunter
from dotenv import load_dotenv
load_dotenv()


def main():
    linkedin_username = os.getenv("LINKEDIN_USER")
    linkedin_passkey = os.getenv("LINKEDIN_PASS")
    hunter_apikey = os.getenv("HUNTER_API")
    chromedriver_dir = os.getenv("CHROMEDRIVER")

    listing_url = input("Welcome to Recruit_Link!  Please enter a job listing's LinkedIn url:\n")
    name, title, profile, company, company_website, job_title = \
        find_contact(listing_url, linkedin_username, linkedin_passkey, chromedriver_dir)
    company_website = company_website.replace("bit.ly", f"{company}.com").replace("/careers", "")
    print(f"Now searching for: {name.strip()}, {title.strip()}\n")

    email_message = f"Hi {name.split()[0]},\n" \
              f"\n" \
              f"I hope this email finds you well.  I just recently saw a posting for a {job_title} position at {company}" \
              f" and would love to learn more.  My experience with Python, SQL, SKILLS HERE feels like a great fit for " \
                    f"the role.\n" \
              f"\n" \
              f"Could you tell me more about the data science team and what it's like to work for the company?  " \
              f"I believe you would have great insight as a {title.strip()} for {company}.\n" \
              f"\n" \
              f"I appreciate any information you could provide, looking forward to hearing from you!\n" \
              f"\n" \
              f"Thank you,\n" \
              f"\n"

    linkedin_message = f"Hi {name.split()[0]}, I recently saw a {job_title} position at {company} and I wanted " \
                       f"to learn more about your company! My experience with Python, SQL, FILL feels like a great fit " \
                       f"for the role. Would love any more information you have, thanks!"

    name = name.lower()
    company_email = company_website.replace("https://www.", "@")\
                                   .replace("http://www.", "@")\
                                   .replace("http:", "@")\
                                   .replace("https:", "@")\
                                   .replace("jobs.", "")\
                                   .replace(r"\.com.*$", ".com")\
                                   .replace("/", "")
    patterns = ["finitiallast", "finitial.last", "firstlast", "first.last",
                "first", "last", "firstlinitial", "first.linitial", "first_linitial", "finitial_last"]
    patterns = [pattern
                    .replace("first", name.split()[0])
                    .replace("last", name.split()[-1])
                    .replace("finitial", name.split()[0][0])
                    .replace("linitial", name.split()[-1][0]) + company_email for pattern in patterns]

    hunter = PyHunter(hunter_apikey)  # Hunter API Key here
    hunter_email, confidence_score = hunter.email_finder(company_website, full_name=name)
    if hunter_email:
        emails = [hunter_email] + patterns
    else:
        emails = patterns

    for email in emails:
        print(f"Checking {email}...")
        try:
            verification = hunter.email_verifier(email)
        except:
            continue
        if verification['result'] == 'deliverable':
            print("Success, found the following email:\n")
            print(email)
            pyperclip.copy(email_message)
            print("Message pasted to clipboard.")
            exit()
        elif email == emails[-1]:
            print(f"Email search failed, try to contact on LinkedIn:\n" 
                  f"{profile}")
            pyperclip.copy(linkedin_message)
            print("Message pasted to clipboard.")
            exit()
        else:
            continue


if __name__ == "__main__":
    main()
