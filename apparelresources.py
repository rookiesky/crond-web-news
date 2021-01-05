from bs4 import BeautifulSoup
import time
from Request import Request

request = Request()
list_url = []
wordpress_api = 'https://www.simtf.com/wordpress_post_api.php?action=save'

def articleFormat(soup):
    title = soup.find('h1',attrs={"class",'post-title single-post-title entry-title'}).string
    excerpt = soup.find('div',attrs={'class','post-subtitle'}).string
    create_time,sep,tail = (soup.find('time',attrs={'class','entry-date color-default'}).string).partition('|')
    create_time = create_time.rstrip(' \xa0')
    soup.find('div',attrs={'class','penci-single-link-pages'}).extract()
    soup.find('section',attrs={'class','rel_artmainbg'}).extract()
    soup.find(id="midlnwltr").extract()
    tages = [item.string for item in soup.select('.post-tags > a')]
    if len(tages) > 0 :
        tages = ",".join(tages)

    soup.find('div',attrs={'class','post-tags'}).extract()
    content = str(soup.find('div',attrs={'class','inner-post-entry entry-content'}))
    author = soup.find('a',attrs={'class','author-url'}).string
    return {'post_title': title, 'post_excerpt': excerpt, 'tag': tages, 'post_content': content, 'post_author': author, 'post_date': create_time, 'post_category': 2}

def article():
    global list_url, request, wordpress_api
    for item in range(len(list_url)):
        article_html = request.request(list_url[0])
        if article_html == False:
            continue

        soup = BeautifulSoup(article_html,'html.parser')

        try:
            data = articleFormat(soup)
            request.requestPost(wordpress_api,data)
            request.logger.info('Success! post_title:{}'.format(data['post_title']))
        except Exception as e:
            request.logger.error('article format error,msg:{}'.format(e))
            continue
        finally:
            del list_url[0]
            soup = ''

def articleList(url):
    global list_url
    res = request.request(url)
    soup = BeautifulSoup(res,'html.parser')
    article_list = soup.select(".entry-title > a")
    list_url = [item.get('href') for item in article_list ]
    article()
    time.sleep(3)
    request.logger.info('sleep 3S loading...')

def main():
    urls = [
        'https://apparelresources.com/technology-news/',
        'https://apparelresources.com/business-news/'
    ]
    for url in urls:
        articleList(url)
    
    request.logger.info('get apparelresources Success!')

try:
    main()
except:
    exit()