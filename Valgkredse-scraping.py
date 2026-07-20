import urllib
import urllib.request
import urllib.error
#import urllib.parse
import time
import random
import os


#os.chdir('C:/Users/jan_c/OneDrive/Data science/DS804 Datamining/Fri leg/FT26')


urls_2011 = "https://www.dst.dk/valg/Valg1204271/valgopg/valgopgOpst"
urls_2015 = "https://www.dst.dk/valg/Valg1487635/valgopg/valgopgOpst"
urls_2019 = "https://www.dst.dk/valg/Valg1684447/valgopg/valgopgOpst"
urls_2022 = "https://www.dst.dk/valg/Valg1968094/valgopg/valgopgOpst"
urls_2026 = "https://www.dst.dk/valg/Valg2546527/valgopg/valgopgOpst"
urls_stor = "https://www.dst.dk/valg/Valg2546527/valgopg/valgopgStor"

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}


def entry(urls,path,start,end):
    if not os.path.exists(path):
        os.mkdir(path)
    for kreds in range(start,end+1):
        try:
            link = urls+str(kreds)+'.htm'
            request = urllib.request.Request( link, None, headers )
            response = urllib.request.urlopen( request )
            with open(path+'/'+str(kreds)+".html", 'w',encoding="utf-8") as f:
                f.write(str(response.read().decode('utf-8')))
            print("Valget", path, "valgkreds",kreds,"scraped")
            time.sleep(random.random())
        except urllib.error.HTTPError as e:
            print(e)

entry(urls_2011,'2011',20,111)
entry(urls_2015,'2015',20,111)
entry(urls_2019,'2019',20,111)
entry(urls_2022,'2022',20,111)
entry(urls_2026,'2026',20,111)
#entry(urls_stor,'storkredse',10,19)
