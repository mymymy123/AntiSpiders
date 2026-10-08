import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

'''browser = webdriver.Chrome()
browser.get('https://antispider3.scrape.center')
WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.item')))
html = browser.page_source
doc=pq(html)
names=doc('.item .name')
for name in names.items():
    print(name.text())#字体的顺序是乱的，网页中每个字对应一个span标签，通过css显示正确的位置
browser.close()'''


url='https://antispider3.scrape.center'

def parse_name(name_html):

    chars=name_html('.char')
    items=[]
    for char in chars.items():
        items.append({
            'text':char.text(),
            'left':int(re.search('(\d+)px',char.attr('style')).group(1))
        })
    items.sort(key=lambda x:x.get('left'))
    return ''.join([item.get('text') for item in items])
options=webdriver.ChromeOptions()
options.add_argument('--headless')
browser=webdriver.Chrome(options=options)
browser.get(url)
WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.item')))
html=browser.page_source
doc=pq(html)
names=doc('.item .name')
for name in names.items():
    print(parse_name(name))

