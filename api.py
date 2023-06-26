from flask import Flask, jsonify,request, Blueprint,flash,json
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/<date>', methods =['GET', 'POST'])

def get_matches(date):
    page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    championships = soup.find_all("div", {'class': 'matchCard'})
    def get_match_info(championships):
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all('li')
        number_of_matches = len(all_matches)
        for i in range(number_of_matches):

            # get channel names
            ch = all_matches[i].find('div', {'class': 'channel'})
            if ch is not None:
                channel = ch.text.strip()
            else:
                channel = "غير معلوم"

            #get penaltyRes
            penalty = all_matches[i].find('div', {'class': 'penaltyRes'})
            if penalty is not None:
                penaltyr = penalty.text.strip()
            else:
                penaltyr = "لا يوجد"

            #get groups names
            groups = all_matches[i].find('div', {'class': 'date'}).text.strip()

            #get matchStatus
            matchStatus = all_matches[i].find('div', {'class': 'matchStatus'}).text.strip()

            # get teams names
            team_A = all_matches[i].find('div', {'class': 'teamA'}).text.strip()
            team_B = all_matches[i].find('div', {'class': 'teamB'}).text.strip()

            #get score
            match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # get match time
            match_time = all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

            # add matches info to matches_details
            matches_details.append({
                'نوع البطولة': championship_title,
                'الفريق الاول': team_A,
                'الفريق الثانى': team_B,
                'ميعاد المباراة': match_time,
                'النتيجه': score,
                'ضربات جزاء': penaltyr,
                'القناه الناقله': channel,
                'المجموعه': groups,
                'حاله المباراه' : matchStatus,
            })

    for i in range(len(championships)):
        get_match_info(championships[i])

    json_dump = json.dumps(matches_details,ensure_ascii=False)
    return json_dump

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)