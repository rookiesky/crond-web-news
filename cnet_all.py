from Request import Request
from bs4 import BeautifulSoup
import time

request = Request()
list_url = []
url = 'https://www.cnet.com/topics/culture/'
host = 'https://www.cnet.com'
wordpress_api='https://www.simtf.com/wordpress_post_api.php?action=save'

def articleListUrl(url):
    global list_url, host
    response = request.request(url)
    if response == False:
        return False
    
    soup = BeautifulSoup(response,'html.parser')
    links = soup.select(".fullListing > .row > div > .assetBody > a")
    list_url = [host + item.get('href') for item in links]

def articleFormat(soup):
    title = soup.find('h1',attrs={'class','speakableText'}).next
    post_excerpt = soup.find('p',attrs={'class','c-head_dek'}).get_text()
    author = soup.find('a',attrs={'class','author'}).string
    create_date = soup.find('div',attrs={'class','c-assetAuthor_date'}).contents[1].attrs['datetime']
    try:
        soup.find('div',attrs={'section':'subscribeNewsletter'}).extract()
    except:
        pass
    try:
        soup.find('svg',attrs={'class','svg-symbol playerControls'}).extract()
    except:
        pass
    try:
        soup.find('div',attrs={'class','shortcode video v2'}).extract()
    except:
        pass
    try:
        soup.find('p',attrs={'data-component':'lazyloadElement'}).extract()
    except:
        pass
    try:  
        soup.find('a',attrs={'class','allLink'}).extract()
    except:
        pass
    
    try:
        
        for item in soup.find_all('div',attrs={'data-item':'image'}):
            item.contents[1].attrs['href'] = ''
    except:
        pass

    try:
        soup.find('span',attrs={'class','more'}).extract()
    except:
        pass
    
    try:
        for item in soup.find_all('img',attrs={'class','lazy'}):
            item.extract()
    except:
        pass

    try:
        soup.find('img',attrs={'class','recommendationCallback'}).extract()
    except:
        pass
    try:
        soup.find('footer',attrs={'class','row c-foot'}).extract()
    except:
        pass

    body = soup.find(id="article-body")
   
    try:
        for item in body.find_all('a'):
            if 'https://www.cnet.com/news' in item.attrs['href']:
                item.attrs['rel'] = 'noopener noreferrer nofollow'
                continue
            if 'news' in item.attrs['href']:
                item.attrs['href'] = item.attrs['href'].replace('news','archives')
            else:
                item.attrs['rel'] = 'noopener noreferrer nofollow'
    except:
        pass
    
    return {'post_title': title, 'post_excerpt': post_excerpt,'post_content': str(body), 'post_author': author, 'post_date': create_date, 'post_category': 143}


def article():
    global list_url,wordpress_api
    for url in list_url:
        response = request.request(url)
        if response == False:
            continue

        soup = BeautifulSoup(response,'html.parser')
        try:
            data = articleFormat(soup)
            request.requestPost(wordpress_api,data=data)
            request.logger.info('Success!title:{}'.format(data['post_title']))
        except Exception as e:
            request.logger.error('article format is error,msg:{}'.format(e))
        finally:
            soup = ''
            response = ''
            data = ''
        
def main():
    global url, list_url
    for i in range(2600,0,-1):
        link = url + str(i) + '/'
        articleListUrl(link)
        if(len(list_url) <= 0):
            continue
        article()
        request.logger.info('Reptile Page:{}'.format(i))
        request.logger.info('sleep 5s loadding...')
        time.sleep(5)

main()
