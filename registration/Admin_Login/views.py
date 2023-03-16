from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
import pyrebase


firebaseConfig = {
  "apiKey": "AIzaSyB-YlDEnwxFcRQy1ZQXTW0SnMis1SAPkoI",
  "authDomain": "line-free-c2f74.firebaseapp.com",
  "databaseURL": "https://line-free-c2f74-default-rtdb.firebaseio.com",
  "projectId": "line-free-c2f74",
  "storageBucket": "line-free-c2f74.appspot.com",
  "messagingSenderId": "608412692251",
  "appId": "1:608412692251:web:affdb3d208b921c2532dbe",
  "measurementId": "G-F8J0WQV9CT"
};

firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database=firebase.database()

Golbal_Token = 0

# Create your views here.
def index(request):
    if request.method=='POST':
        Admin_name=request.POST.get('Username')
        Password=request.POST.get('Password')
        all_admins = database.child("Admin").get()
        for adm in all_admins.each():
            name=adm.val()['Username']
            pas=adm.val()['Password']
            pwd=str(pas)
            if name==Admin_name:
                if pwd==Password:
                    return redirect('Admin_dashboard')
                    # print('pass')
                    
    return render(request,'Admin_Login/index.html')

def Customer_login(request):
    if request.method=='POST':
        phone=request.POST.get('phone')
        tokenno=request.POST.get('tokenno')
        global Golbal_Token
        Golbal_Token = tokenno
        all_queue = database.child("queue").child("Enteries").get()
        # print('A ',all_queue)
        # queue = database.child("queue").child("Enteries").get()
        # if queue.val():
        #     print(queue.val()[4]['mobile'])
        # i=1
        for adm in all_queue.each():
            if adm.val()==None:
                continue
            else:
                print(adm.val())
                toke=adm.val()["token"]
                mob=adm.val()["mobile"]
                mobi=str(mob)
                tok=str(toke)
                if tok==tokenno:
                    if mobi==phone:
                        return redirect('Custmor_dashboard')
    return render(request,'Admin_Login/Customer_login.html')

def Admin_dashboard(request):
    data={}
    queue=database.child("queue").get().val()
    total=len(queue)
    print("Total = ",total)
    data["Total"]=total
    return render(request,'Admin_Login/Admin_dashboard.html',data)

def Custmor_dashboard(request):
    global Golbal_Token
    print("Global Token = ",Golbal_Token)
    User_info = database.child("queue").child("Enteries").child(Golbal_Token).get().val()
    print("user info = ",User_info)
    data={}
    for key,val in User_info.items():
        print(key," : ",val)
        data[key]=val
    queue=database.child("queue").get().val()
    total=len(queue)
    print("Total = ",total)
    data['total']=total
    # estimatedtime= 0
    # if total == 1:
    #     estimatedtime_1 = "No Waiting"
    # if total > 1:
    #     estimatedtime = data['Register_time'] * total
    # data['estimatedtime_1']=estimatedtime_1
    # data['estimatedtime']=estimatedtime
    # register_time, mobile, reason, token, usename =  User_info['Register_time'], User_info['mobile'], User_info['token'], User_info['usename']
    # data = {
    #     'rt': register_time,
    #     'mob': mobile,
    #     'rea': reason,
    #     'tok': token,
    #     'user': usename,
    # }
    return render(request,'Admin_Login/Custmor_dashboard.html',data)

def manage(request):
    return render(request,'Admin_Login/manage.html')