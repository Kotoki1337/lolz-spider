from dhooks import Webhook, Embed
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from redis import Redis
import urllib.request
import requests
import json
import time
import pytz
import re

with open('TOKEN.json', mode='r', encoding='u8') as jfile:
    token = json.load(jfile)

rankDisc = {
    1 : "白银 I",
    2 : "白银 II",
    3 : "白银 III",
    4 : "白银 IV",
    5 : "白银精英",
    6 : "大师级白银精英",
    7 : "黄金新星 I",
    8 : "黄金新星 II",
    9 : "黄金新星 III",
    10 : "大师级黄金新星",
    11 : "大师级守护者 I",
    12 : "大师级守护者 II",
    13 : "大师级守护者精英",
    14 : "杰出大师级守护者",
    15 : "传奇之鹰",
    16 : "大师级传奇之鹰",
    17 : "无上之首席大师",
    18 : "全球精英"
}

medalsDisc = {
    "Медаль за службу в 2015" : "15服役",
    "Медаль за службу в 2016" : "16服役",
    "Медаль за службу в 2017" : "17服役",
    "Медаль за службу в 2018" : "18服役",
    "Медаль за службу в 2019" : "19服役",
    "Медаль за службу в 2020" : "20服役",

    "Медаль за верность" : "忠诚",

    "Монета за 5 лет службы" : "五年老兵",
    "Монета за 10 лет службы" : "十年老兵",

    "Бронзовый трофей прогнозов на ESL One Cologne 2014" : "2014年科隆锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на ESL One Cologne 2014" : "2014年科隆锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на ESL One Cologne 2014" : "2014年科隆锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на DreamHack Winter 2014" : "2014年 DreamHack 冬季锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на DreamHack Winter 2014" : "2014年 DreamHack 冬季锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на DreamHack Winter 2014" : "2014年 DreamHack 冬季锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на ESL One Katowice 2015" : "2015年卡托维兹锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на ESL One Katowice 2015" : "2015年卡托维兹锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на ESL One Katowice 2015" : "2015年卡托维兹锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на ESL One Cologne 2015" : "2015年科隆锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на ESL One Cologne 2015" : "2015年科隆锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на ESL One Cologne 2015" : "2015年科隆锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на DreamHack Cluj-Napoca 2015" : "2015年克卢日-纳波卡锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на DreamHack Cluj-Napoca 2015" : "2015年克卢日-纳波卡锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на DreamHack Cluj-Napoca 2015" : "2015年克卢日-纳波卡锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на MLG Columbus 2016" : "2016年哥伦布锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на MLG Columbus 2016" : "2016年哥伦布锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на MLG Columbus 2016" : "2016年哥伦布锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на ESL One Cologne 2016" : "2016年科隆锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на ESL One Cologne 2016" : "2016年科隆锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на ESL One Cologne 2016" : "2016年科隆锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на ELEAGUE Atlanta 2017" : "2017年亚特兰大锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на ELEAGUE Atlanta 2017" : "2017年亚特兰大锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на ELEAGUE Atlanta 2017" : "2017年亚特兰大锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на PGL Krakow 2017" : "2017年克拉科夫锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на PGL Krakow 2017" : "2017年克拉科夫锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на PGL Krakow 2017" : "2017年克拉科夫锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на ELEAGUE Boston 2018" : "2018年波士顿锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на ELEAGUE Boston 2018" : "2018年波士顿锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на ELEAGUE Boston 2018" : "2018年波士顿锦标赛竞猜黄金级纪念奖牌",

    "Бронзовый трофей прогнозов на FACEIT London 2018" : "2018年伦敦锦标赛竞猜青铜级纪念奖牌",
    "Серебряный трофей прогнозов на FACEIT London 2018" : "2018年伦敦锦标赛竞猜白银级纪念奖牌",
    "Золотой трофей прогнозов на FACEIT London 2018" : "2018年伦敦锦标赛竞猜黄金级纪念奖牌",

    "монета IEM Katowice 2019" : "2019年卡托维兹锦标赛纪念奖牌",
    "Серебряная монета IEM Katowice 2019" : "2019年卡托维兹锦标赛白银级纪念奖牌",
    "Золотая монета IEM Katowice 2019" : "2019年卡托维兹锦标赛黄金级纪念奖牌",
    "Бриллиантовая монета IEM Katowice 2019" : "2019年卡托维兹锦标赛钻石级纪念奖牌",

    "Монета StarLadder Berlin 2019" : "2019年柏林锦标赛纪念奖牌",
    "Серебряная монета StarLadder Berlin 2019" : "2019年柏林锦标赛白银级纪念奖牌",
    "Золотая монета StarLadder Berlin 2019" : "2019年柏林锦标赛黄金级纪念奖牌",
    "Бриллиантовая монета StarLadder Berlin 2019" : "2019年柏林锦标赛钻石级纪念奖牌",

    "Монета операции «Расплата»" : "回馈大行动挑战币",
    "Серебряная монета операции «Расплата»" : "回馈大行动银币",
    "Золотая монета операции «Расплата»" : "回馈大行动金币",

    "Монета операции «Авангард»" : "先锋大行动挑战币",
    "Серебряная монета операции «Авангард»" : "先锋大行动银币",
    "Золотая монета операции «Авангард»" : "先锋大行动金币",

    "Монета операции «Браво»" : "英勇大行动挑战币",
    "Серебряная монета операции «Браво»" : "英勇大行动银币",
    "Золотая монета операции «Браво»" : "英勇大行动金币",

    "Монета операции «Феникс»" : "凤凰大行动挑战币",
    "Серебряная монета операции «Феникс»" : "凤凰大行动银币",
    "Золотая монета операции «Феникс»" : "凤凰大行动金币",

    "Монета операции «Дикое пламя»" : "野火大行动挑战币",
    "Серебряная монета операции «Дикое пламя»" : "野火大行动银币",
    "Золотая монета операции «Дикое пламя»" : "野火大行动金币",

    "Монета операции «Прорыв»" : "突围大行动挑战币",
    "Серебряная монета операции «Прорыв»" : "突围大行动银币",
    "Золотая монета операции «Прорыв»" : "突围大行动金币",

    "Монета операции «Бладхаунд»" : "血猎大行动挑战币",
    "Серебряная монета операции «Бладхаунд»" : "血猎大行动银币",
    "Золотая монета операции «Бладхаунд»" : "血猎大行动金币",

    "Монета операции «Гидра»" : "九头蛇大行动挑战币",
    "Серебряная монета операции «Гидра»" : "九头蛇大行动银币",
    "Золотая монета операции «Гидра»" : "九头蛇大行动金币",
    "Бриллиантовая монета операции «Гидра»" : "九头蛇大行动钻石币",

    "Монета операции «Расколотая сеть»" : "裂网大行动挑战币",
    "Серебряная монета операции «Расколотая сеть»" : "裂网大行动银币",
    "Золотая монета операции «Расколотая сеть»" : "裂网大行动金币",
    "Бриллиантовая монета операции «Расколотая сеть»" : "裂网大行动钻石币"
}

medalsList_abb = [
    "Расплата",
    "Авангард",
    "Браво",
    "Феникс",
    "Дикое пламя",
    "Прорыв",
    "Бладхаунд",
    "Гидра",
    "Расколотая сеть"
    ]

medalsPrefix = [
    "",
    "Серебряная ",
    "Золотая ",
    "Бриллиантовая "
]

def main(redis_client):
    driver = webdriver.Chrome("./chromedriver.exe")
    print("Current session is {}".format(driver.session_id))
    driver.get(token["marketUrl"])
    time.sleep(10)
    cookie = driver.get_cookie("df_id")
    df_id = cookie["value"]
    print("Get cookie done")
    driver.close()

    for medalsName in medalsList_abb: # hardcode
        if medalsName == "Гидра" or medalsName == "Расколотая сеть": # 判断是否是九头蛇和破网
            medalsPrefix = ["Монета", "Серебряная%20монета", "Золотая%20монета", "Бриллиантовая%20монета"] # 钻石币
        else:
            medalsPrefix = ["Монета", "Серебряная%20монета", "Золотая%20монета"] # 无钻石币
        for medalsPrefix_i in medalsPrefix:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4170.0 Safari/537.36 Edg/85.0.552.1',
                'cookie': f'df_id={df_id}'
            }
            response = requests.get(f'https://lolz.guru/market/steam/?no_vac=1&no_mm_ban=1&medal[]={medalsPrefix_i}%20операции%20«{medalsName}»&order_by=price_to_up', headers=headers)

            w = open('readPage.html', 'w', encoding='utf-8')
            w.write(response.text)
            print("Get website done")
            w.close()

            file = open("./readPage.html", "rb")
            html = file.read()
            bs = BeautifulSoup(html, "html.parser")

            tList = bs.find_all(attrs={"id":re.compile(r"marketItem--\d")})

            for i in tList:
                bs1 = BeautifulSoup(str(i), "html.parser")

                urlTag = BeautifulSoup(str(bs1.find_all(class_="marketIndexItem--Title")[0]), "html.parser").a
                url = urlTag["href"]

                if not redis_client.sadd("lolz", url):
                    continue

                price = BeautifulSoup(str(bs1.find_all(class_="marketIndexItem--Price")[0]), "html.parser").span.text
                ownerRecent = BeautifulSoup(str(bs1.find_all(class_="stat")[0]), "html.parser").span.text.strip()
                user = BeautifulSoup(str(bs1.find_all(class_="username")[0]), "html.parser").span.text
                title = BeautifulSoup(str(bs1.find_all(class_="marketIndexItem--Title")[0]), "html.parser").get_text()
                try:
                    restorePercents = BeautifulSoup(str(bs1.find_all(class_="restorePercents")[0]), "html.parser").get_text()
                except:
                    restorePercents = "Unknown Percents or Never sold account."

                try:
                    dateTag = BeautifulSoup(str(bs1.find_all(class_="DateTime muted")[0]), "html.parser").abbr
                    dateTimestamp = dateTag["data-time"]
                    tz = pytz.timezone('Asia/Taipei')
                    date = datetime.fromtimestamp(int(dateTimestamp), tz).isoformat()
                except:
                    date = "now"

                try:
                    oge = BeautifulSoup(str(bs1.find_all(class_="extendedGuarantee hasFirstEmail")[0]), "html.parser").span.text
                except:
                    oge = "None"

                try:
                    rankTag = BeautifulSoup(str(bs1.find_all(class_="marketIndexItem--CsgoRankImg")[0]), "html.parser").img
                    rankInt = rankTag["src"].replace("//raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/0e457516ba13817a45b6c2a1d262fe7d0599bcbc/csgo/pak01_dir/resource/flash/econ/status_icons/skillgroup", "").replace(".png", "")
                    rank = rankDisc[int(rankInt)]
                except:
                    rank = "None"

                try:
                    steamCsgoMedals = BeautifulSoup(str(bs1.find_all(class_="steamCsgoMedals")[0]), "html.parser")
                    medalsList = steamCsgoMedals.find_all(class_="medalImg")
                    medals = []
                    for i in medalsList:
                        medalsTag = BeautifulSoup(str(i), "html.parser").img
                        medals_RU = medalsTag["alt"]
                        medals_CN = medalsDisc.get(medals_RU, medals_RU)
                        medals.append(medals_CN)
                        medalsResult = ", ".join(medals)
                except:
                    medalsResult = "Unknown"
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4170.0 Safari/537.36 Edg/85.0.552.1',
                    'cookie': f'df_id={df_id}'
                }
                response = requests.get(f'https://lolz.guru/{url}', headers=headers)

                w1 = open('accountPage.html', 'w', encoding='utf-8')
                w1.write(response.text)
                w1.close()

                with open("./accountPage.html", "r", encoding='UTF-8') as fs:
                    accountHtml = fs.readlines()
                accountPage = BeautifulSoup(str(accountHtml), "html.parser")
                try:
                    originTag = BeautifulSoup(str(accountPage.find_all(class_="counter long")[0]), "html.parser")
                    origin = BeautifulSoup(str(originTag.find_all(class_="label")[0]), "html.parser").get_text()
                except:
                    try:
                        if "You have opened an ad for the sale of a phishing account." in str(accountHtml):
                            origin = "Phishing (fake site)"
                        else:
                            origin = "Unknown"
                    except:
                        origin = "Unknown"

                try:
                    soldtag = BeautifulSoup(str(accountPage.find_all(class_="marketItemView--sameItemsContainer")[0]), "html.parser")
                    sold = BeautifulSoup(str(soldtag.find_all(class_="title mn-0-0-15")[0]), "html.parser").get_text()
                except:
                    sold = "This account is not sold before"

                hook = Webhook(token["TOKEN"])
                embed = Embed(
                description = f'By seller: **{user}** {restorePercents}',
                url = f'https://lolz.guru/{url}',
                timestamp = f'{date}'  # sets the timestamp to current time
                )
                embed.set_author(name = title, icon_url = "https://i.imgur.com/LwvJYdH.png", url = f"https://lolz.guru/{url}")
                embed.add_field(name = "Price", value = f'{price}руб')
                embed.add_field(name = "OGE", value = f'{oge}')
                embed.add_field(name = "Account origin", value = f'{origin}')
                embed.add_field(name = "CS:GO Rank", value = f'{rank}')
                embed.add_field(name = "Medals", value = f"{medalsResult}")
                embed.add_field(name = "Recent Play", value = f'{ownerRecent}')
                embed.add_field(name = "Direct Url", value = f'https://lolz.guru/{url}')
                embed.set_footer(text = f'{sold}')

                print(medals)

                if origin == "Phishing (fake site)" or origin == "Resale (Phishing (fake site))":
                    if int(price.replace(" ", "").replace(",", "")) < 1000:
                        hook.send(embed=embed)
                else:
                    if int(price.replace(" ", "").replace(",", "")) < 3500:
                        hook.send(embed=embed)


if __name__ == "__main__":
    redis_client = Redis.from_url("redis://:@localhost:6379/0?decode_responses=True")
    while True:
        main(redis_client)
        print("Waiting 10 min")
        time.sleep(1800)
