import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
c = ["歌名",'歌手',"作詞","作曲",'歌詞']
df = pd.DataFrame(columns=c)

def writeFile(ii):
    try:
        j = ii.get('href')
        sub_resp = requests.get("https://mojim.com" + j)
        sub_soup = BeautifulSoup(sub_resp.text, 'html.parser')

        list1 = []

        sub_name1 = sub_soup.find('dl', 'fsZx1')
        sub_name2 = sub_soup.find('dt', 'fsZx2')
        sub_name3 = sub_soup.find('dd', 'fsZx3')

        abc = sub_name2.text.split("(")[0] + ' '
        list1.append(abc)
        eee = sub_name1.text.replace("\n", "").split(" ")[0]
        list1.append(eee)

        try:
            sub_name3_list = sub_name3.contents
            aaa = ''
            lyrics = ''
            composer = ''
            for tx in sub_name3_list:

                if tx.string != None:
                    if '[' in tx.string or '更多更詳盡歌詞' in tx.string or '※ Mojim.com　魔鏡歌詞網 ' in tx.string:
                        pass
                    elif '作詞：' in tx.string and '[' not in tx.string:
                        lyrics = tx.string
                        list1.append(lyrics.split("：")[1])
                    elif '作曲：' in tx.string and '[' not in tx.string:
                        composer = tx.string
                        list1.append(composer.split("：")[1])
                    elif '編曲：' in tx.string and '[' not in tx.string:
                        pass
                    elif '演唱：' in tx.string and '[' not in tx.string:
                        pass
                    elif '主唱：' in tx.string and '[' not in tx.string:
                        pass
                    elif '原唱：' in tx.string and '[' not in tx.string:
                        pass
                    elif '合唱：' in tx.string and '[' not in tx.string:
                        pass
                    elif '和聲：' in tx.string and '[' not in tx.string:
                        pass
                    elif '監製：' in tx.string and '[' not in tx.string:
                        pass
                    elif '監制：' in tx.string and '[' not in tx.string:
                        pass
                    elif '製作：' in tx.string and '[' not in tx.string:
                        pass
                    elif '製作人：' in tx.string and '[' not in tx.string:
                        pass
                    elif '改編詞：' in tx.string and '[' not in tx.string:
                        pass
                    elif 'RAP詞：' in tx.string and '[' not in tx.string:
                        pass
                    elif 'RAP：' in tx.string and '[' not in tx.string:
                        pass
                    elif 'Rap：' in tx.string and '[' not in tx.string:
                        pass
                    elif '男聲：' in tx.string and '[' not in tx.string:
                        pass
                    elif '女聲：' in tx.string and '[' not in tx.string:
                        pass
                    elif '童聲：' in tx.string and '[' not in tx.string:
                        pass
                    elif '主題曲' in tx.string and '[' not in tx.string:
                        pass
                    elif '插曲' in tx.string and '[' not in tx.string:
                        pass
                    elif '片尾曲' in tx.string and '[' not in tx.string:
                        pass
                    elif '片頭曲' in tx.string and '[' not in tx.string:
                        pass
                    elif '廣告曲' in tx.string and '[' not in tx.string:
                        pass
                    elif '印象曲' in tx.string and '[' not in tx.string:
                        pass
                    elif 'feat' in tx.string and '[' not in tx.string:
                        pass
                    else:
                        bbb = re.sub(r'\w:', "", tx.string)
                        ccc = re.sub(r'\w：', "", bbb)
                        ddd = re.sub(r'\(\w+\)', "", ccc)
                        aaa += ddd.replace("\u3000", "")\
                                   .replace("REPEAT", "")\
                                   .replace("＊", "")\
                                   .replace("＃", "")\
                                   .replace("△", "")\
                                   .replace("#", "")\
                                   .replace("Repeat", "")\
                                   .replace("☆", "")\
                                   .replace("…", "")\
                                   .replace("●", "")\
                                   .replace("report", "")\
                                   .replace(".", "")\
                                   .replace("*", "")\
                                   .replace("~", "")\
                                   .replace("！", "")\
                                   .replace("repeat", "")\
                                   .replace("？","")+ " "

            list1.append(aaa)

            if len(list1) == 5:
                s = pd.Series([abc, eee, lyrics, composer, aaa.rstrip()], index=c)
                print(s)
                global df
                df = df.append(s, ignore_index=True)
                print(len(df))

            print(len(list1))
        except AttributeError:
            pass
    except AttributeError:
        pass

#listpage = ['twza1','twzb1','twzc1']
#for a in listpage:
url = 'https://mojim.com/twzb1.htm'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
block = soup.find_all('ul', 's_listA')
for i in block:
    urll = i.find_all('li')
    for j in urll:
        sl = j.find_all('a')
        for k in sl:
            page = k.get('href')

            resp = requests.get('https://mojim.com' + page)
            soup = BeautifulSoup(resp.text, 'html.parser')
            block = soup.find_all('dd', 'hb2')
            block2 = soup.find_all('dd', 'hb3')

            for i in block:
                song_left = i.find_all('span', 'hc3')
                for j in song_left:
                    sl = j.find_all('a')
                    for k in sl:
                        writeFile(k)

                song_right = i.find_all('span', 'hc4')
                for j in song_right:
                    sr = j.find_all('a')
                    for k in sr:
                        writeFile(k)


            for i in block2:
                song_left = i.find_all('span', 'hc3')
                for j in song_left:
                    sl = j.find_all('a')
                    for k in sl:
                        writeFile(k)

                song_right = i.find_all('span', 'hc4')
                for j in song_right:
                    sr = j.find_all('a')
                    for k in sr:
                        writeFile(k)
print(df)
df.to_csv("test5.csv",encoding="utf-8",index=False,line_terminator='')