import settings

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'localhost')

from pymongo import MongoClient
client = MongoClient(SECRET_KEY, 27017)
db = client.cplists

import requests
from bs4 import BeautifulSoup

#  캠핑장소 스크랩핑
def item_scrap():
    indexId = 1;
    for n in range(9, 18):
        for i in range(1, 4):
            url = f'https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=c_rdcnt&searchDo=,{n},&pageIndex={i}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
            data = requests.get(url, headers=headers)
            soup = BeautifulSoup(data.text, 'html.parser')
            all_list = soup.select(
                "#cont_inner > div > div.camp_search_list > ul > li")

            for li in all_list:
                title = li.select_one('div > div > h2 > a').text
                comment = li.select_one('div > div > span.camp_stt').text
                url = 'https://www.gocamping.or.kr' + li.select_one('div > div > h2 > a')['href']
                img = 'https://www.gocamping.or.kr'+li.select_one('div > a > div > img')['src']
                views = li.select_one('div > div > p > span.item_t03').text[4:]
                address = li.select_one('div > div > ul > li.addr').text
                phone = li.select_one('div > div > ul > li.call_num')
                
                if phone is not None:
                    phone = phone.text
                else:
                    phone = '업데이트 예정'
                
                if comment == "":
                    comment = title

                try:
                    detail_data = get_detail(url)

                    area_name = title.split(']')[0][1:]
                    doc ={
                    'id':  indexId,
                    'area': area_name,
                    'title': title,
                    'comment': comment,
                    'desc': detail_data[0],
                    'camp_env' :detail_data[1],
                    'camp_type' :detail_data[2],
                    'views': int(views),
                    'address': address,
                    'phone':phone,
                    'img': img,
                    'url': url,
                    }

                    # db.cplist.insert_one(doc)
                    print(indexId)
                    indexId += 1

                except:
                    print("넘김")
                    


# og:image, og:description 데이터 추출
def get_detail(url_receive):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    camp_desc = soup.select_one('#contents > div > div.layout > div > p > span:nth-child(1)')


    check_env = soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(3) > th').text

    camp_env=''
    camp_type=''
    camp_period=''

  

    if check_env =='캠핑장 환경':
        camp_env = soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(3) > td').text
        camp_type = soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(4) > td').text
     
      
    else:
        camp_env = soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(2) > td').text
        camp_type = soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(3) > td').text
       
       

    
    print(camp_period)
    
    if camp_desc is None:
        camp_desc = "업데이트 예정"
    else:
        camp_desc=camp_desc.text


    return [camp_desc,camp_env,camp_type]

item_scrap()


