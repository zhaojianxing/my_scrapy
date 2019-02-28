# coding:utf-8
import requests
import MySQLdb
from scrapy.selector import Selector


cnn = MySQLdb.connect("localhost", "root", "178178", "xici_ips", charset="utf8", use_unicode=True)
cursor = cnn.cursor()

def crawl_ips():
    # request 爬去西祠的免费IP代理
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
    n = 1
    while True:
        response = requests.get(url="https://www.xicidaili.com/nn/{a}".format(a=n), headers=headers)
        selector = Selector(text=response.text)

        all_selector = selector.css('#ip_list tr')
        proxy_list = []
        for tr in all_selector[1:]:
            speed_str = tr.css('.bar::attr(title)').extract()[0]
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            td = tr.css('td::text').extract()
            ip = td[0]
            port = td[1]
            proxy_type = td[5]
            proxy_list.append((ip, port, proxy_type, speed))
        sql = """
            insert into proxy_ips(ip, port, speed, proxy_type)VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (ip, port, speed, proxy_type))
        cnn.commit()

        next_page = selector.css('.next_page::attr(href)').extract()
        if not next_page:
            break
        n += 1

class GetIp(object):
    def judge_ip(self,ip, port, proxy_type):
        url = 'http://www.baidu.com'
        proxy_url = '{a}//:{b}:{c}'.format(a=proxy_type, b=ip, c=port)
        try:
            proxy_dict = {
            proxy_type:proxy_url,
            }

            response = requests.get(url=url, proxies=proxy_dict)
            code = response.status_code
        except Exception as e:
            print("ip and port unavaiilable")
            self.delete_ip(ip)
            return  False
        else:
            if code >= 200 and code <= 300:
                return True
            else:
                print("ip and port unavaiilable")
                self.delete_ip(ip)
                return False

    def delete_ip(self, ip):
        delete_ip = """
            delete from proxy_ips where ip = '{a}'    
        """.format(a=ip)
        return True

    def get_random_ip(self):
        random_sql = """
            SELECT ip, port, proxy_type FROM proxy_ips ORDER BY RAND() LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_result in cursor.fetchall():
            ip = ip_result[0]
            port = ip_result[1]
            proxy_type = ip_result[2]
            successd = self.judge_ip(ip, port, proxy_type)
            if successd:
                return (ip, port, proxy_type)
            else:
                return self.get_random_ip()



if __name__ == '__main__':
    # crawl_ips()
    get_ip = GetIp()
    print(get_ip.get_random_ip())