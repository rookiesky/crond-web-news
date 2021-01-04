from Request import Request
import json
from bs4 import BeautifulSoup
import re
import time
from urllib import parse

request = Request()
list_url = []
webapi = 'https://www.industryweek.com/technology-and-iiot'
host = 'https://www.industryweek.com'

def getAfter(response):
    k = re.findall('"after":(.*?)}',response,re.S)
    if len(k) <= 0:
        request.logger.error('arter is empty')
        return False
    return k[0]

def postData(after,page):  
    data= '{"appendTo":".page-grid__bottom-row","expand":500,"componentName":"lazarus-shared-content-load-more-flow","componentInput":{"adunit":{"location":"taxonomy","position":"infinitescroll","context":{"sectionId":65862}}},"fragmentName":"content-list","queryName":"website-scheduled-content","queryParams":{"sectionId":65862,"limit":7,"queryName":"LoadMore","after":'+after+'},"pageInput":{"for":"website-section","id":65862},"pageNumber":'+str(page)+'}'
    return 'https://www.industryweek.com/__load-more/?input=' + parse.quote(data)

def articleListUrl(soup):
    global list_url
    urls = soup.select(".node__title > a")
    list_url = [host + item.get('href') for item in urls]

def articleFormat(soup):
    title = soup.find('h1',attrs={'class','content-page-card__content-name'}).string
    post_excerpt = soup.find('p',attrs={'class','content-page-card__content-teaser'}).string
    post_author = soup.find('span',attrs={'class','page-attribution__content-name'})
    author = post_author.contents[0].string
    create_time = soup.find('div',attrs={'class','page-dates__content-published'}).string
    body = str(soup.find('div',attrs={'class','page-contents__content-body'}))
    return {'post_title': title, 'post_excerpt': post_excerpt, 'post_content': body, 'post_author': post_author, 'post_date': create_time, 'post_category': 136}


def article():
    global list_url,request
    for url in range(len(list_url)):
        response = request.request(url=list_url[0])
        if response == False:
            continue
        soup = BeautifulSoup(response,'html.parser')
        try:
            data = articleFormat(soup)
            request.requestPost(wordpress_api='https://www.simtf.com/wordpress_post_api.php?action=save',data=data)
            request.logger.info(data['post_title'])
        except Exception as e:
            request.logger.error('article format error,url:{},msg:{}'.format(url,e))
            continue
        finally:
            soup = ''
            del list_url[0]
        

def main():
    global webapi,list_url
    headers = {'referer':'https://www.industryweek.com/technology-and-iiot','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    
    response = request.request(url=webapi,headers=headers)   
    if response == False:
        exit()

    soup = BeautifulSoup(response,'html.parser')
    response = ''
    articleListUrl(soup)
    soup = ''
    list_url = list_url[9:]
    request.logger.info(len(list_url))
    exit()
    article()
    request.logger.info('Success!')

main()
