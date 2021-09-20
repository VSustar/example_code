#Vid Sustar
#Web scrapper to gather data about sold appartments/houses in Finland from https://asuntojen.hintatiedot.fi/haku/
#it creates a csv file containing all the information given for the specified locations of interest

import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re


start_time = time.time()


#important specify the places:
area_list=("Turku", "Kaarina")

# html parsing
filename = "asuntojen.csv"
f = open(filename, "w")

headers = "area, housetype, roomnumb, area_part, rooms, msquare, eur_msqr, price, yearbuilt, floor, floortt, elevator, state, energylvl, energylvlyr \n" #floor total stems from breaking the floor in 1/4 format into 1,4
f.write(headers)

def inter_area_loop(area_list):
    for area in area_list:
        inter_page_loop(area)

def inter_page_loop(area):
    counter=1
    while 1:
        my_url = "https://asuntojen.hintatiedot.fi/haku/?c=" + area + "&cr=1&h=1&h=2&h=3&r=1&r=2&r=3&r=4&t=3&l=0&z="+str(counter)+"&search=1&sf=0&so=a&submit=%C2%AB+edellinen+sivu"
        uClient = uReq(my_url)  # opening up connection, grabbing the page
        page_html = uClient.read()
        uClient.close()  # close the client
        page_soup = soup(page_html, "html.parser")
        maintable = page_soup.find(id="mainTable")
        oddclass = maintable.find_all(class_="odd")
        time.sleep(1.5)  # delay between url requests to not overburden the servers
        if len(oddclass)>1:
            counter+=1
            intra_page_loop(oddclass, area)#calling intra page loop
        else:
            break

def intra_page_loop(oddclass, area):
    trs = oddclass[1].findAll('tr')
    count = 0
    trs: object
    roomnumb=trs[0].td.text.rstrip().replace('\n','')  #getting house type (yksio, etc)
    if roomnumb == "Yksiö":
        roomnumb = 1
    elif roomnumb == "Kaksi huonetta":
        roomnumb = 2
    elif roomnumb == "Kolme huonetta":
        roomnumb = 3
    elif roomnumb == "Neljä huonetta tai enemmän":
        roomnumb = 4
    print("WORKING")
    print("ROOMNUMBER2x:",roomnumb, roomnumb)
    itertrs=iter(trs) #skipping first element that has housetype inside
    next(itertrs)
    for tr in itertrs:
        try:
            count += 1
            print("tr NUMBER ",count," :")#,tr)
            tds = tr.find_all("td")
            #print("TDS: ",tds)
            consnumb=count
            print("tds[0].text",tds[0].text)
            area_part=tds[0].text.replace('\n','').replace(",", " ")
            rooms=tds[1].text.replace(",", "+").rstrip().replace('\n','')
            housetype=tds[2].text.rstrip().replace('\n','')
            if housetype=="ok":
                housetype=0
            elif housetype=="rt":
                housetype=1
            elif housetype=="kt":
                housetype=2
            msquare=tds[3].text.replace(",", ".").rstrip().replace('\n','')
            price=tds[4].text.rstrip().replace('\n','')
            eur_msqr=tds[5].text.rstrip().replace('\n','')
            yearbuilt=tds[6].text.rstrip().replace('\n','')
            floor=tds[7].text.rstrip().replace('\n','')
            print("FLOOR",floor)
            if "/" in floor:
                print("slash found!")
                floor=floor.split("/")#var floor total stems from breaking the floor in 1/4 format into split , therefore floor total header should always be after floor header
                floortot=floor[1].rstrip().replace('\n','')
                floor=floor[0].rstrip().replace('\n','')
            else:
                print("slash not found!")
                floortot=floor.rstrip().replace('\n','')
            print ("floor, floortot",floor, floortot)
            elevator=tds[8].text
            if elevator=="ei":
                elevator=0
            elif elevator=="on":
                elevator=1
            state=tds[9].text.rstrip().replace('\n','')
            if state=="huono":
                state=0
            elif state=="tyyd.":
                state=1
            elif state=="hyvä":
                state=2
            energylvl=tds[10].text.rstrip().replace('\n','')
            print("energylvl",energylvl)
            print(len(energylvl))
            #energy level, spliting if also year of estimation, conversion from letter to number A-..-G into 7 -..- 1
            en_lvl_dict = {"A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}
            if (len(energylvl)>1):
                energlvllist=re.split('(\d+)', energylvl)
                print ("energlvllist",energlvllist)
                energylvl=energlvllist[0]
                energylvl=en_lvl_dict.get(energylvl, "")
                energylvlyr = energlvllist[1]
                print(energylvl)
                print(energylvlyr)
            elif (len(energylvl)==1):
                energylvl = en_lvl_dict.get(energylvl, "")
                energylvlyr=""
            else:
                energylvlyr = ""
            print("rooms, housetype, msquare,price,eur_msqr,yearbuilt,floor,elevator,state,energylvl",rooms, housetype, msquare,price,eur_msqr,yearbuilt,floor,elevator,state,energylvl)
            print("price", price)
            print("str price", str(price))
            f.write(area  + "," + str(housetype) + "," + str(roomnumb) + "," + str(area_part)+ "," + str(rooms)+ "," + str(msquare)+ "," + str(eur_msqr)+ "," + str(price)+ "," + str(yearbuilt)+ "," + str(floor) + "," + str(floortot)+"," + str(elevator)+ "," + str(state)+ "," + str(energylvl)+"," + str(energylvlyr)+"\n")
            print("break")
            print("Process took --- %s seconds ---" % (time.time() - start_time))
        except Exception:
            pass

inter_area_loop(area_list)


f.close()

