from django.shortcuts import render
import json
from django.http.response import JsonResponse
from bs4 import BeautifulSoup as scraper
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random


def main(request):
    return render(request,template_name="scrape/intro.html")


def images(request):
    if request.method == 'POST':
        try:
            form = json.loads(request.body.decode('utf-8'))
            url = form['weburl']
            html_content = get_html_with_selenium(url)
            soup = scraper(html_content, 'html.parser')
        
            image_tags = soup.find_all('img')
            image_urls = []
            for img in image_tags:
                img_url = img.get('src')
                print(img_url)
                if img_url:
                    img_url = urljoin(url, img_url)
                    image_urls.append(img_url)
            
            return JsonResponse(image_urls, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
    
    return render(request, 'scrape/ImagesScraper.html')

def links(request):
    if request.method=='POST':
        try:
            form=json.loads(request.body)
            url=form['weburl']
            content=get_html_with_selenium(url)
            soup=scraper(content,'html.parser')
            links=soup.find_all('a')
            weblinks=[]
            for link in links:
                href=link.get('href')
                if href:
                    full_url=urljoin(url,href)
                    weblinks.append(full_url)
            return JsonResponse(weblinks,safe=False)

        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
    return render(request,template_name='scrape/LinksScraper.html')


def table(request):
    if request.method=="POST":
        try:
            print("called")
            form=json.loads(request.body)
            url=form['weburl']
            content=get_html_with_selenium(url)
            soup=scraper(content,'html.parser')
            tables = soup.find_all('table')
            scraped_data = []
            for table in tables:
                table_data = []
                rows = table.find_all('tr')  
                for row in rows:
                    row_data = []
                    cells = row.find_all(['th', 'td']) 
                    for cell in cells:
                        row_data.append(cell.text.strip()) 
                    table_data.append(row_data)
                scraped_data.append(table_data)
            print(scraped_data)
            return JsonResponse(scraped_data,safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
    return render(request,template_name='scrape/TableScraper.html')




def custome(request):
    if request.method=='POST':
        try:
            print('called')
            form=json.loads(request.body)
            url=form['weburl']
            content=get_html_with_selenium(url)
            soup=scraper(content,'html.parser')
            content = {
                'class': [],
                'id': [],
                'tag': []
            }
            tag=form['tag']
            tags=soup.find_all(tag)
            print(tag)
            for tag in tags:
                print("called")
                tag_class = tag.get('class', None)
                if form['class'] and isinstance(tag_class, list) and form['class'] in tag_class:
                    content['class'].append(tag.get_text())

                tag_id = tag.get('id', None)
                if form['id'] and tag_id and form['id'] in tag_id:
                    content['id'].append(tag.get_text())

                # If both class and id are empty and the tag itself is not empty
                if not form['class'] and not form['id'] and tag:
                    content['tag'].append(tag.get_text())

            return JsonResponse(content,safe=False)
        except Exception as e:
            return JsonResponse({'error':f"Error: {str(e)}"},status=500)

    return render(request,'scrape/Custome.html')













def get_html_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')  # To evade detection

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.implicitly_wait(10)  # Set implicit wait time

    try:
        driver.get(url)

        # Wait for the document to be ready
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        # Wait for images to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        )
    except Exception as e:
        content="error retriving data"
        return content
    finally:
        content = driver.page_source
        driver.quit()
    return content