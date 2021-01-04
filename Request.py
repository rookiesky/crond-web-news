import requests
import random
import logging

class Request():

    def __init__(self):
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        #DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

        self.logger = logging.getLogger('mytest')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)


    def userAgent(self):
        ua = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/87.0.4280.88 Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
            'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
            'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62'
        ]
        return random.choice(ua)


    def request(self,url, headers = {}):
        try:
            ua = {'user-agent': self.userAgent()}
            head = {}
            head.update(ua)
            head.update(headers)
            response = requests.get(url,headers = head, timeout = 120)
            return response.text
        except requests.exceptions.ConnectTimeout:
            self.logger.error('http connect time out,url:{},'.format(url))
            return False
        except requests.exceptions.ConnectionError:
            self.logger.error('http connection error,url:{},'.format(url))
            return False
        except requests.exceptions.HTTPError as e:
            self.logger.error('http status error,status code:{},url:{}'.format(e.code,url))
            response.close()
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error('error:{}'.format(e))
            return False
                    
    def requestPost(self,wordpress_api,data):
        try:
            response = requests.post(wordpress_api,data=data)
            return response.text
        except requests.exceptions.ConnectTimeout:
            self.logger.error('http connect time out')
            return False
        except requests.exceptions.ConnectionError:
            self.logger.error('http connection error')
            return False
        except requests.exceptions.HTTPError as e:
            self.logger.error('http status error:{}'.format(e.code))
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error('error:{}'.format(e))
            return False
        finally:
            response.close()
