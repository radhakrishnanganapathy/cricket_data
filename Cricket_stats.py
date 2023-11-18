import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import json
import os

def cricket_data(url,venue,matchid,team1,team2,Toss,tournament,stage,won,match_type):
     try:

          driver = webdriver.Chrome()  # You need to have the ChromeDriver executable in your path or provide the path here
          driver.get(url)

          # Wait for the dynamic content to load
          element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, 'grd_sld-wrp.commentaryInnerBox-1'))
          )

          # Get the page source after dynamic content has loaded
          page_source = driver.page_source

          # Use BeautifulSoup to parse the HTML
          soup = BeautifulSoup(page_source, 'html.parser')

          # Now you can find the content inside grd_sld-wrp.commentaryInnerBox-1
          matach_data = []
          for i in range(1,3):
               print(f"innings-{i} start...")
               extra = ''
               innings = i
               matchID = 'INDNZ1723'
               if i == 1:
                    batting_Team = team1
               else:
                    batting_Team = team2


               content = soup.find('div', class_=f'grd_sld-wrp commentaryInnerBox-{i}')
               if content:
                    data = content.find_all('div', class_='lst_cir-scl')
                    
                    for i in data:
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
                                   extra = '1'
                              if lb:
                                   ball = lb.text.strip()
                                   extra = '1'
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
                                   venue,matchid,team1,team2,Toss,tournament,stage,won,match_type
                              ball_data = {
                                   "venue" :venue,
                                   "team1" : team1,
                                   "team2": team2,
                                   "matchID": matchid ,
                                   "tournament" : tournament,
                                   "stage" : stage,
                                   "match_type":match_type,
                                   "won":won,
                                   "Toss" : Toss,
                                   "Innings":innings,
                                   "batting Team":batting_Team,
                                   "over" : overs,
                                   "ball" : ball,
                                   "runs" : runs,
                                   "extra" : extra,
                                   "batsman" : batsman,
                                   "bowler" : bowler
                              }
                              matach_data.append(ball_data)
                              # print(overs,runs, bowler,batsman)
               if os.name == 'posix':  # Unix-like system (Linux, macOS)
                    internal_storage_path = os.path.expanduser("~/Downloads")
               elif os.name == 'nt':  # Windows
                    internal_storage_path = os.path.join(os.path.expanduser("~"), "Downloads")
               else:
                    internal_storage_path = "/storage/emulated/0/Download"
                    
               
               if not os.path.exists(internal_storage_path):
                    os.makedirs(internal_storage_path)
               file_path = os.path.join(internal_storage_path, f"{matchID}.json")
               # file_path = "Z:/radhakrishnan/webscrap/data.json"
               with open(file_path, 'w') as f:
                    json.dump(matach_data, f,indent=4)
               with open('data.json','r') as f:
                    d = json.load(f)

          driver.quit()  # Close the browser
          return(st.write(matach_data))
     except Exception as e:
          return (st.write(e))
     
st.title("hello")
url = st.text_input('url') #1
venues = ['chennai','mumbai']
teams = ['IND','AUS','RSA','NZ','SL','BAN','PAK']
venue = st.sidebar.selectbox("select venues",venues) #2
matchid = st.sidebar.text_input("MatchID") #3
st.sidebar.write("Note team1 is first batting ")
team1 = st.sidebar.selectbox("Team 1", teams) #4
team2 = st.sidebar.selectbox("Team 2",teams) #5
Toss = st.sidebar.selectbox("Toss", teams) #6
tournaments = ['ICC WC ODI', 'ICC WC T20','CT','TC','IPL','TOUR']
tournament = st.sidebar.selectbox("tournament ", tournaments) #7
stages = ['LEAGUE','SEMI','FINALS','SERIES']
stage = st.sidebar.selectbox("stages", stages) #8
won = st.sidebar.selectbox("won",teams) #9
match_types = ['ODI','T20','TEST']
match_type = st.sidebar.selectbox('matchtype',match_types) #10

if st.button("submit"):
     cricket_data(url,venue,matchid,team1,team2,Toss,tournament,stage,won,match_type)
