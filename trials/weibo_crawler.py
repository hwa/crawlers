#-*- coding: utf-8 -*-

import bs4
import requests
import re
import urllib


def login(username, password):
    r = requests.get('http://3g.sina.com.cn/prog/wapsite/sso/login.php?backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=4&revalid=2&ns=1')
    rb = bs4.BeautifulSoup(r.text)
    submit_url = 'http://3g.sina.com.cn/prog/wapsite/sso/' + rb.find('form')['action']
    password_name = rb.find(name='input', attrs={'type':'password'})['name']

    post_data = {'mobile': username}
    post_data[password_name] = password
    post_data['backURL'] = rb.find(name='input', attrs={'name':"backURL"})['value']
    post_data['backTitle'] = rb.find(name='input', attrs={'name':"backTitle"})['value'].encode('utf-8')
    post_data['vk'] = rb.find(name='input', attrs={'name':"vk"})['value']
    post_data['submit'] = rb.find(name='input', attrs={'name':"submit"})['value'].encode('utf-8')

    r = requests.post(str(submit_url), data = post_data)
    rb = bs4.BeautifulSoup(r.text)
    #redirect_url = rb.find('meta', attrs={'http-equiv':'refresh'})['content'][6:]
    redirect_url = rb.find('a')['href']
    cookies = r.cookies
    r = requests.get(redirect_url, cookies=cookies)
    home_url = r.url
    gsid = re.search(r'gsid=(.*)', home_url).groups()[0]

    return dict(url = home_url,
                gsid = gsid,
                cookies = cookies)

def get_weibo_comments(uid, weibo_id, gsid, cookies):
    wb_url = 'http://weibo.cn/comment/%s?&uid=%s&&gsid=%s' % (weibo_id, uid, gsid)
    rb = bs4.BeautifulSoup(requests.get(wb_url, cookies=cookies).content.decode('utf-8'))
    repost_num = int(re.search(r'\d+', rb.find('a', href=re.compile(r'^\/repost\/')).text).group())
    comments_num = int(re.search(r'\d+', rb.find('span', class_='pms').text).group())
    comments_url = rb.find('form', action=re.compile(r'\/comment\/'))['action']
    comments = [i.text for i in rb.find_all('span', class_='ctt')]
    for page in range(1, comments_num/10+2):
        r = requests.get('http://weibo.cn' + comments_url + '&page=%d' % page)
        rb = bs4.BeautifulSoup(r.content.decode('utf-8'))
        c = [i.text for i in rb.find_all('span', class_='ctt')]
        comments += c
    return comments
    

def get_weibo_repost():
    url_base = 'http://m.weibo.cn/2143550005/zlfhsfUIE?format=json&type=zf&st=f2e4&page=1'
    

