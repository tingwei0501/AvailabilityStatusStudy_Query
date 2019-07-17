from prettytable import PrettyTable
import json
import requests
import datetime
import time

self_URL = "http://13.59.255.194:5000/notificationCompletedRate"
contact_URL = "http://13.59.255.194:5000/checkContactStatusRate"
dump_URL = "http://13.59.255.194:5000/checkDumpData"

user_ids = {
    "test": ["armuro"],
    "312": ["lucy", "yang", "mandytsai"]
}

while True:
    group = input("Which group do you want to query? # Type 'q' or 'Q' to exit the program: ")
    if group == "q" or group == "Q":
        break
    print ("'1' to query 'Self Questionnaire'")
    print ("'2' to query 'Contact Questionnaire'")
    print ("'3' to query 'dump data'")
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

    print ("Now querying '" + group + "' between " + str(start_date) + " and " + str(end_date))

    data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
    query = json.dumps(data)

    if service == '1':
        print ("####### Quering: SELF Questionnaire #######")
        selfTable = PrettyTable(['User ID','Total Notifications','Completed','Completed Rate'])
        for user in user_ids[group]:
            # print (user)
            
            res = requests.post(self_URL, json = query)
            userData = json.loads(res.text)
            # Id, 總共幾筆通知問卷, 完成幾筆通知問卷, 完成比率, 自行編輯狀態問卷有幾筆 #
            selfTable.add_row([user, userData['total'], userData['selfCompleted'], userData['completedRate'], userData['selfEditCompleted']])
            
        print(selfTable)

    elif service == '2':
        print ("####### Quering: CONTACT Questionnaire #######")
        contactTable = PrettyTable(['User ID','Contact ID','count'])
        for user in user_ids[group]:
            # data = {'id': user, 'query_start_month': start_month, 'query_end_month': end_month, 'query_start_date': start_date, 'query_end_date': end_date}
            # query = json.dumps(data)
            res = requests.post(contact_URL, json = query)
            userData = json.loads(res.text)
            for key, value in userData.items():
                contactTable.add_row([user, key, value])
                # print (key, " ", value)
        print (contactTable)

    elif service == '3':
        print ("####### Quering: DUMP Data #######")
        dumpTable = PrettyTable(['User ID', 'Total Data Count'])
        for user in user_ids[group]:
            
            res = requests.post(dump_URL, json = query)
            userData = json.loads(res.text)
            dumpTable.add_row([user, userData['count']])
        print (dumpTable)