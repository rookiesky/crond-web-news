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
    headers = {'referer':'https://www.industryweek.com/technology-and-iiot','cookie':'_ga=GA1.2.755273177.1609322463; oly_enc_id=null; oly_anon_id=%22d6439226-2d11-433a-88a9-4ea93dee998b%22; _fbp=fb.1.1609322466636.702579838; __sapience_v=%7B%22id%22%3A%22d0bde6f8-68fb-433b-a512-005b4930d819%22%2C%22customerId%22%3Anull%7D; bounceClientVisit3211=; gadsTest=test; _gid=GA1.2.591654537.1609580780; sbtsck=javUyMSmEf9KF5tHqRApbyLatDU6ze2HLKhJZLkPINv7XQ=; SPSI=4ab2358275197b74e902e4451e3399dc; SPSE=3v4+bOvWw24aZAIJ5h048oED+CgnypUfat26f6DleWzioN/WXjVFEKhAeKkL0fE0CJnkoYS4UP/vFcnWKW72Gg==; spcsrf=0aedd0854b89b2645294cba7a987a4f3; PRLST=Zv; UTGv2=h40833b419c70faf10706aceeb4338704445; feathr_session_id=5ff18a7a888e5e5270f1d9b8; __sapience_s=%7B%22id%22%3A%2264ac77bb-794e-4aa0-be48-6b05b4faf6a3%22%2C%22createdAt%22%3A%22Sun%2C%2003%20Jan%202021%2009%3A12%3A26%20GMT%22%7D; bounceClientVisit3211v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0AlgHYAmAriggE4CexApuwNZkDGA9gFsiCdrzhV+YfgHMWAWgCGteRQr8ERRUwQVeYdkVwBGYwFYADAHYAbMaLsqM6pyYolvAYIhgKKOPLs2ghwAI50ilzs8iiKAGbsCAo07CgUMlQgADQgTDAgpMSUtAzMbJw8XiAAvkA; __idcontext=eyJjb29raWVJRCI6IkZWU0tFTkZBQ01EUFo1RlpVRFZFNkFNVlpVWUNVTlRFTjU3WFpMTzZBTVZRPT09PSIsImRldmljZUlEIjoiRlZTS0VORkJLWUxOWEo1VVJYWFVZQ1VZNE1VVE1GMk1NSUVXSkI2U041NEE9PT09IiwiaXYiOiJLSDNPUEdZQ05BWEROVjRHQVRBTkVNVUhGQT09PT09PSIsInYiOjF9; adOtr=3SaL42b7815','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    
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
