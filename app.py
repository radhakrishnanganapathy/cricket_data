import requests
from bs4 import BeautifulSoup
import json
import re


url = 'https://sports.ndtv.com/cricket/live-commentary/ind-vs-nz-1st-semi-final-mumbai-innz11152023228844'

response  = requests.get(url)

if response.status_code == 200:
     soup = BeautifulSoup(response.text, 'html.parser')
     link = soup.find('div', class_='pg_cnt-wrp')
     if link:
        sub_container = link.find('div', class_='mid_wrp') 
        if sub_container:
            # data = sub_container.find('div', class_='grd_sld-wrp commentaryInnerBox-2')
            data = sub_container.find('div', class_='grd_sld-wrp commentaryInnerBox-1')
            if data:
               data2 = link.find_all('div', class_='lst_cir-scl')
               matach_data = []
               for i in data2:
                    over = i.find('div', class_='ful_scr-bwl')
                    dot = i.find('div', class_='lst_cir-itm cir_0')
                    one = i.find('div', class_='lst_cir-itm cir_1')
                    two = i.find('div', class_='lst_cir-itm cir_2')
                    four = i.find('div', class_='lst_cir-itm cir_4')
                    six = i.find('div', class_='lst_cir-itm cir_6')
                    wkt = i.find('div', class_='lst_cir-itm cir_w')
                    wide = i.find('div', class_='lst_cir-itm cir_wd')
                    title_info = i.find('div', class_='ful_scr-ttl')
                    lb = i.find('div', class_='lst_cir-itm cir_lb')
                    description = i.find('div', class_='ful_scr-txt')
                    if over:
                        overs = over.text.strip()
                        if dot:
                              runs = dot.text.strip()
                              ball = None
                        if one:
                              runs = one.text.strip()
                              ball = None
                        if two:
                              runs = two.text.strip()
                              ball = None
                        if four:
                              runs = four.text.strip()
                              ball = None
                        if six:
                              runs = six.text.strip()
                              ball = None
                        if wkt:
                              ball = wkt.text.strip()
                              runs = '0'
                              # runs = wkt.text.strip()
                        if wide:
                              ball = wide.text.strip()
                              runs = 1
                        if lb:
                             ball = lb.text.strip()
                             runs = '1'
                           #   if description:
                           #       sentences = description.split('. ')
                           #       if sentences:
                           #             first_word = sentences[0]
                           #             words = first_word.split()
                           #             if words:
                           #                   if words == 'Four':
                           #                      runs = '4'
                        if title_info:
                           title = title_info.text.strip()
                           action_text = re.sub(r'\s*OUT!\s*', '', title)
                           parts = action_text.split(" To ")
                           bowler = parts[0]
                           batsman = parts[1]
                        ball_data = {
                             "venue" :'Wankhede Stadium, Mumbai',
                             "team" : "IND vs NZ",
                             "match" : "semi1",
                             "Toss" : "IND",
                             "Innings":'1',
                             "batting Team":"ind",
                             "over" : overs,
                             "ball" : ball,
                             "runs" : runs,
                             "batsman" : batsman,
                             "bowler" : bowler
                        }
                        matach_data.append(ball_data)
                        # print(overs,runs, bowler,batsman)
               print(matach_data)
               file_path = "Z:/radhakrishnan/webscrap/data.json"
               with open(file_path, 'w') as f:
                    json.dump(matach_data, f,indent=4)
               with open('data.json','r') as f:
                    d = json.load(f)

   
     
else:
     print("no response")