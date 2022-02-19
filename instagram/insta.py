from datetime import datetime
import os
import time
import urllib.request

from selenium import webdriver


class InstagramScraper:
    
    def __init__(self):
        
        with open('proxy.txt','r') as file:
            apply_proxy = file.read().split('\n')[0]
        
        if apply_proxy.lower() == 'yes':
            with open('proxy.txt','r') as file:
                proxy_data = file.read().split('\n')
            
            PROXY = proxy_data[0]
            
            webdriver.DesiredCapabilities.CHROME['proxy']={
                "httpProxy": PROXY,
                "httpsProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,
                "proxyType": "MANUAL",
            }
       
        self.driver = webdriver.Chrome(r'/usr/local/bin/chromedriver')
          
    
    def data_reader(self):
        with open('login_information.txt','r') as file:
            data = file.read().split('\n')

        login_username = data[0]
        login_password = data[1]

        with open('instagram_accounts_urls.txt','r') as file:
            urls = file.read().split('\n')
        
        return login_username, login_password, urls
    
    
    def login(self, login_username, login_password):
        
        self.driver.get("https://www.instagram.com/")
        #login
        time.sleep(3)
        username = self.driver.find_element_by_css_selector("input[name='username']")
        password = self.driver.find_element_by_css_selector("input[name='password']")
        username.clear()
        password.clear()

        username.send_keys(login_username)
        password.send_keys(login_password)

        self.driver.find_element_by_css_selector("button[type='submit']").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not now')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        time.sleep(3)
        
    def get_post_links(self, urls):
        
        for url in urls:
            path = url.split('/')[3]
            posts = []
            
            if not os.path.exists(path):
                os.mkdir(path)
                
            self.driver.get(url)
            time.sleep(3)

            scroll = "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document" \
                ".body.scrollHeight;return scrolldown;"
                
            scrolldown = self.driver.execute_script(scroll)
            match=False
            while(match==False):
                last_count = scrolldown
                time.sleep(3)
                links = self.driver.find_elements_by_tag_name('a')
                for link in links:
                    post = link.get_attribute('href')
                    if '/p/' in post:
                        posts.append(post)
                scrolldown = self.driver.execute_script(scroll)
                if last_count==scrolldown:
                    match=True
                    
            posts = list(set(posts))
            
            for post in posts:	
                self.driver.get(post)
                time.sleep(3)

                if len(self.driver.find_elements_by_css_selector('.tWeCl')) > 0:
                    continue
                
                download_urls = self.driver.find_elements_by_css_selector(".ZyFrc .KL4Bh > img")
                
                for url in download_urls:
                    img_name = f"{self.driver.current_url.split('/')[-2]}_{datetime.now().strftime('%Y%m-%d%H-%M%S-')}"
                    time.sleep(2)
                    d_url = url.get_attribute('src')
                    
                    if d_url:
                        urllib.request.urlretrieve(d_url, path +'/'+'{}.jpg'.format(img_name))
            
            
    def InstaBOT(self, username, password, urls):
        
        self.login(username, password)
        self.get_post_links(urls)
            
            
if __name__ == '__main__':
    instagrambot = InstagramScraper()
    
    username, password, urls = instagrambot.data_reader()
    instagrambot.InstaBOT(username, password, urls)
    
    