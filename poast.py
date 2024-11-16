import os
import sys
import requests
from bs4 import BeautifulSoup

MASTODON_API_URL = 'https://your.instance.url/api/v1/statuses'
ACCESS_TOKEN = os.getenv('MASTODON_API_KEY')
POSTED_URLS_FILE = os.path.expanduser('~/masto-poast/posted_urls.txt')

def extract_summary_and_tag(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the first <p> tag within the .indent div as a summary
    indent_div = soup.find('div', {'class': 'indent'})
    if indent_div:
        paragraphs = indent_div.find_all('p')
        summary = paragraphs[0].get_text() if paragraphs else "No summary available"
    else:
        summary = "No summary available"
    
    # Extract the tag from the <span> within the #main div
    main_div = soup.find('div', {'id': 'main'})
    tag_span = None
    if main_div:
        for span in main_div.find_all('span'):
            if 'tag:' in span.get_text().lower():
                tag_span = span
                break
    
    if tag_span:
        tag_link = tag_span.find('a')
        if tag_link:
            tag = tag_link.get_text(strip=True)
            print(f"Extracted tag: {tag}")
        else:
            tag = ""
            print("No <a> tag found within <span>")
    else:
        tag = ""
        print("No <span> tag found with 'tag:' text")
    
    hashtag = f"#{tag.replace(' ', '').lower()}" if tag else ""
    
    return summary, hashtag

def post_to_mastodon(content):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'status': content
    }
    response = requests.post(MASTODON_API_URL, headers=headers, json=data)
    print(f'Request URL: {MASTODON_API_URL}')
    print(f'Request Headers: {headers}')
    print(f'Request Data: {data}')
    print(f'Response Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    if response.status_code == 200:
        print('Successfully posted to Mastodon')
    else:
        print(f'Error posting to Mastodon: {response.status_code} - {response.text}')

def has_been_posted(post_url):
    if not os.path.exists(POSTED_URLS_FILE):
        return False
    with open(POSTED_URLS_FILE, 'r') as file:
        posted_urls = file.read().splitlines()
    return post_url in posted_urls

def mark_as_posted(post_url):
    with open(POSTED_URLS_FILE, 'a') as file:
        file.write(post_url + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python poast.py "Post URL"')
        sys.exit(1)
    post_url = sys.argv[1]
    print(f'Received post URL: {post_url}')
    
    if has_been_posted(post_url):
        print(f'Post URL has already been posted: {post_url}')
        sys.exit(0)
    
    summary, hashtag = extract_summary_and_tag(post_url)
    post_content = f"Your custom text for when it posts: {post_url}\n\n{summary}\n\n{hashtag}"
    print(f'Constructed post content: {post_content}')
    
    post_to_mastodon(post_content)
    mark_as_posted(post_url)
