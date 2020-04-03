from prettytable import PrettyTable
import json
import requests
import datetime
import time
import csv

self_URL = "http://13.59.255.194:5000/notificationCompletedRate"
contact_URL = "http://13.59.255.194:5000/checkContactStatusRate"
dump_URL = "http://13.59.255.194:5000/checkDumpData"
lastDumpData_URL = "http://13.59.255.194:5000/lastDumpData"
word_URL = "http://13.59.255.194:5000/wordToMe"
whoCheckMe_URL = "http://13.59.255.194:5000/whoCheckMyStatus"
presentWayResult_URL = "http://13.59.255.194:5000/idealStatusResult"
contactStatusPresentResult_URL = "http://13.59.255.194:5000/contactStatusPresentResult"

user_ids = {
    "test": ["test"],
    "王培霖": ["asazelur", "kid", "chengt"], # 主要參與者
    # "王培霖": ["3939889", "wendy60612913"] # 半參與者
    "老鼠會": ["nano1201", "鳥尹", "zxc012"],
    "g2": ["larrypig", "scyang", "jason"],
    "清大化學": ["dingkevin", "jbchang5", "ts09leo"], 
    "畢業旅行": ["dorayaki", "Waiting", "laiheng"],
    "g6": ["renee", "igloo", "綠"],
    "余貞安": ["julie", "jjcat", "88888866"],
    "薛丁格的劉劉": ["阿榛", "Brenda", "nata0601"],
    "大家不睡覺": ["abbysayhi", "OWO", "Zelda", "sharon07088"],
    # "partial": ["River", "littlebaby", "ywr", "ronnie77", "yjessie", "mushroom", "88888877", "88888888"],
    "322": ["李睿", "stark", "Titan"],
    "227打switch": ["蛋蛋", "kao", "m.chao", "小李"],
    "partial": [],
}

while True:
    group = input("Which group do you want to query? # Type 'q' or 'Q' to exit the program: ")
    if group == "q" or group == "Q":
        break
    print ("'1' 檢查資料: query 'Self Questionnaire'")
    print ("'d' 最後一筆Dump資料")
    print ("'2' 檢查資料: query 'Contact Questionnaire'")
    print ("'3' 檢查資料: query 'dump data'")
    print ("'4' 看誰留言給我: to see who send me messages")
    print ("'5' 看誰查看我的狀態: to see who check my status")
    print ("'6' 實際狀態呈現方式統計: for Self ideal present way count result")
    print ("'7' 看聯絡人狀態呈現方式統計: for contact status present way count result")
    # print ("'e' for every day query job ()")
    service = input(": ")

    date_range = input("Please indicate the time range you're querying for (e.g. '0720-0721') Your Answer: ")
    #if a user didn't enter time interval
    #suppose is Today
    if date_range == '':
        today = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        print (today)
        date_range_tmp = today.split()[0]
        date_range = date_range_tmp.split("-")
        start_month = int(date_range[1])
        start_date = int(date_range[2])
        end_month = start_month
        end_date = start_date

    else:
        start_month = int(date_range.strip().split("-")[0][0:2])
        start_date = int(date_range.strip().split("-")[0][2:4])
        end_month = int(date_range.strip().split("-")[1][0:2])
        end_date = int(date_range.strip().split("-")[1][2:4])


    print ("start_month: ", start_month)
    print ("start_date: ", start_date)
    print ("end_month: ", end_month)
    print ("end_date: ", end_date)

    outputFile = input("Output .csv File?  (y/n): ")
    print ("Now querying '" + group + "' between " + str(start_date) + " and " + str(end_date))

    if service == '1':
        print ("####### Quering: SELF Questionnaire #######")
        systemTotal = 0
        totalSelfCompleted = 0
        totalSelfEdit = 0
        editTotal = 0
        selfTable = PrettyTable(['User ID','Total System Notifications','Notifications Completed','Notifications Completed Rate', '# Total Edit Status', '# Edit Completed', '# Edit Completed Rate'])
        for user in user_ids[group]:
            # print (user)
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(self_URL, json = query)
            userData = json.loads(res.text)
            print (userData)
            # Id, 總共幾筆通知問卷, 完成幾筆通知問卷, 完成比率, 自行編輯狀態問卷有幾筆, 完成幾筆自行編輯問卷, 完成比率 #
            selfTable.add_row([user, userData['systemTotal'], userData['selfCompleted'], userData['selfCompletedRate'], userData['editTotal'], userData['selfEditCompleted'], userData['editCompletedRate']])
            systemTotal += userData['systemTotal']
            editTotal += userData['editTotal']
            totalSelfCompleted += userData['selfCompleted']
            totalSelfEdit += userData['selfEditCompleted']
        selfTable.add_row(['Total', systemTotal, totalSelfCompleted, '#', editTotal, totalSelfEdit, '#'])
            
        print(selfTable)

    elif service == 'd':
        for user in user_ids[group]:
            data = {'id': user}
            query = json.dumps(data)
            res = requests.post(lastDumpData_URL, json = query)
            userData = json.loads(res.text)
            print (userData)

    elif service == '2':
        print ("####### Quering: CONTACT Questionnaire #######")
        contactTable = PrettyTable(['User ID','Contact ID','count'])
        for user in user_ids[group]:
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(contact_URL, json = query)
            userData = json.loads(res.text)
            for key, value in userData.items():
                contactTable.add_row([user, key, value])
                # print (key, " ", value)
            # if outputFile == 'y':  ##  TODO: output csv file
        print (contactTable)

    elif service == '3':
        print ("####### Quering: DUMP Data #######")
        dumpTable = PrettyTable(['User ID', 'Total Data Count'])
        for user in user_ids[group]:
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(dump_URL, json = query)
            userData = json.loads(res.text)
            dumpTable.add_row([user, userData['count']])
        print (dumpTable)
    
    elif service == '4':
        print ("####### See Who Send Me Messages #######")
        wordTable = PrettyTable(['To', 'From', 'Say Something...'])
        for user in user_ids[group]:
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(word_URL, json = query)
            userData = json.loads(res.text)
            if outputFile == 'y':
                with open(user+'.csv', 'a+', newline='') as csvfile:
                    w = csv.writer(csvfile)
                    w.writerow(['我的聯絡人', '對我說...'])
                    for key, value in userData.items():
                        w.writerow([key, value])
            for key, value in userData.items():
                wordTable.add_row([user, key, value])
        print (wordTable)

    elif service == '5':
        print ("####### See Who Check My Status #######")
        for user in user_ids[group]:
            checkTable = PrettyTable(['Who Check my Status', 'Count'])
            print ("id: ", user)
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(whoCheckMe_URL, json = query)
            userData = json.loads(res.text)
            if outputFile == 'y':
                with open(user+'.csv', 'a+', newline='') as csvfile:
                    w = csv.writer(csvfile)
                    w.writerow(['我的聯絡人', '查看我的狀態的次數'])
                    for key, val in userData.items():
                        w.writerow([key, val])
                
            for key, value in userData.items():
                checkTable.add_row([key, value])
            print (checkTable)

    elif service == '6':
        print ("####### Ideal Present Way Result Computing #######")
        for user in user_ids[group]:
            presentWayTable = PrettyTable(['Present Way', 'Count'])
            print ("id: ", user)
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(presentWayResult_URL, json = query)
            userData = json.loads(res.text)
            for key, val in userData.items():
                presentWayTable.add_row([key, val])
            print (presentWayTable)

    elif service == '7':
        print ("####### Contact Status Present Way Result Computing #######")
        for user in user_ids[group]:
            contactPresentTable = PrettyTable(['項目', 'score'])
            print ("id: ", user)
            data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            query = json.dumps(data)
            res = requests.post(contactStatusPresentResult_URL, json = query)
            userData = json.loads(res.text)
            for key, val in userData.items():
                contactPresentTable.add_row([key, val])
            print (contactPresentTable)