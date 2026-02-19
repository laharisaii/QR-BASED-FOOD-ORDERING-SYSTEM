from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import datetime
import pyqrcode
import png
from pyqrcode import QRCode
import time

global username, usertype

def ScanQR(request):
    if request.method == 'GET':
       return render(request, 'ScanQR.html', {}) 

def CreateMenu(request):
    if request.method == 'GET':
       return render(request, 'CreateMenu.html', {})  

def AddChairs(request):
    if request.method == 'GET':
       return render(request, 'AddChairs.html', {})  

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})  

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def UserLoginAction(request):
    global username, usertype
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t1', False)
        usertype = "none"      
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select usertype FROM register where username='"+username+"' and password='"+password+"'")
            rows = cur.fetchall()
            for row in rows:
                usertype = row[0]
                break		
        if usertype == "Restaurant Owner":
            context= {'data':'welcome '+username}
            return render(request, 'RestaurantScreen.html', context)
        elif usertype == "Customer":
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'Login.html', context)        

def DownloadAction(request):
     if request.method == 'GET':
        username = request.GET['username']
        print("===="+username)
        infile = open('FoodOrderingApp/static/qrcodes/'+username+'.png', 'rb')
        data = infile.read()
        infile.close()
        response = HttpResponse(data, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=%s' % username+".png"
        return response

def CreateMenuAction(request):
    if request.method == 'POST':
        global username
        name = request.POST.get('t1', False)
        price = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        image = request.FILES['t4']
        item_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(item_id) from menu")
            rows = cur.fetchall()
            for row in rows:
                item_id = row[0]
        print(str(item_id)+"====================")        
        if item_id == None:
            item_id = 0
        item_id = item_id + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO menu(username, item_id, item_name, item_price, picture) VALUES('"+username+"','"+str(item_id)+"','"+name+"','"+price+"','"+desc+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'Menu details added with ID '+str(item_id)           
            fs = FileSystemStorage()
            filename = fs.save('FoodOrderingApp/static/menus/'+str(item_id)+".png", image)
        context= {'data':output}
        return render(request, 'CreateMenu.html', context)

def ViewRestaurants(request):
    if request.method == 'GET':
        global username
        columns = ['Restaurant Name', 'Contact No', 'Email ID', 'Address', 'QR Code', 'Download QR Code']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username, contact_no, email, address from register where usertype='Restaurant Owner'")
            rows = cur.fetchall()
            for row in rows:
                item_id = str(row[1])
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
                output+='<td><img src="/static/qrcodes/'+row[0]+'.png" width="200" height="200"></img>'
                output+='<td><a href=\"DownloadAction?username='+str(row[0])+'"\'><font size=3 color=black>Click Here</font></a></td></tr>'
        context= {'data': output}
        return render(request, 'UserScreen.html', context)    

def getRestaurant(item_id):
    name = "None"
    item = ""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select username,item_name FROM menu where item_id='"+item_id+"'")
        rows = cur.fetchall()
        for row in rows:
            name = row[0]
            item = row[1]
            break
    return name, item    

def ViewBills(request):
    if request.method == 'GET':
        global username
        columns = ['Ordered ID', 'Customer Name', 'Restaurant Name', 'Item ID', 'Item Name', 'Amount', 'Ordered Date']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM bookorder where customer_name='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                item_id = str(row[2])
                name, item = getRestaurant(item_id)
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(name)+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(item)+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
                output += "<td>"+font+str(row[4])+"</td></tr>"                
        context= {'data': output}
        return render(request, 'UserScreen.html', context)


def BookOrder(request):
    if request.method == 'GET':
        global username
        pid = request.GET['pid']
        price = request.GET['price']
        dd = str(time.strftime('%Y-%m-%d'))
        order_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(order_id) from bookorder")
            rows = cur.fetchall()
            for row in rows:
                order_id = row[0]
        if order_id == None:
            order_id = 0
        order_id = order_id + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO bookorder(order_id, customer_name, item_id, price, order_date) VALUES('"+str(order_id)+"','"+username+"','"+pid+"','"+price+"','"+dd+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'Your order is confirmed with order ID : '+str(order_id)            
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
        

def ViewOrders(request):
    if request.method == 'GET':
        global username
        dd = str(time.strftime('%Y-%m-%d'))
        columns = ['Ordered ID', 'Customer Name', 'Restaurant Name', 'Item ID', 'Item Name', 'Ordered Date']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM bookorder where order_date='"+dd+"'")
            rows = cur.fetchall()
            for row in rows:
                item_id = str(row[2])
                name, item = getRestaurant(item_id)
                if name == username:
                    output += "<tr>"
                    output += "<td>"+font+str(row[0])+"</td>"
                    output += "<td>"+font+str(row[1])+"</td>"
                    output += "<td>"+font+str(name)+"</td>"
                    output += "<td>"+font+str(row[2])+"</td>"
                    output += "<td>"+font+str(item)+"</td>"
                    output += "<td>"+font+str(row[4])+"</td></tr>"                
        context= {'data': output}
        return render(request, 'RestaurantScreen.html', context)


def ShowMenu(request):
    if request.method == 'GET':
        restaurant_name = request.GET['t1']
        print(restaurant_name)
        columns = ['Restaurant Name', 'Item ID', 'Item Name', 'Price', 'Description', 'Picture', 'Book Order']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM menu where username='"+restaurant_name+"'")
            rows = cur.fetchall()
            for row in rows:
                item_id = str(row[1])
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
                output += "<td>"+font+str(row[4])+"</td>"
                output+='<td><img src="/static/menus/'+item_id+'.png" width="200" height="200"></img></td>'
                output+='<td><a href=\"BookOrder?pid='+str(item_id)+'&price='+str(row[3])+'"\'><font size=3 color=black>Click Here</font></a></td></tr>'
        context= {'data': output}
        return render(request, 'UserScreen.html', context)

def ViewMenu(request):
    if request.method == 'GET':
        global username
        columns = ['Restaurant Name', 'Item ID', 'Item Name', 'Price', 'Description', 'Picture', 'QR Code']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM menu where username='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                item_id = str(row[1])
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
                output += "<td>"+font+str(row[4])+"</td>"
                output+='<td><img src="/static/menus/'+item_id+'.png" width="200" height="200"></img></td>'
                output+='<td><img src="/static/qrcodes/'+username+'.png" width="200" height="200"></img></tr>'
        context= {'data': output}
        return render(request, 'RestaurantScreen.html', context)


def AddChairsAction(request):
    if request.method == 'POST':
        global username
        size = request.POST.get('t1', False)
        chairs = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO addchairs(username, dining_room, num_chairs, description) VALUES('"+username+"','"+size+"','"+chairs+"','"+desc+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'Chair details added for Restaurant '+username        
        context= {'data':output}
        return render(request, 'AddChairs.html', context)    

def SignupAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        usertype = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'foodordering',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username, password, contact_no, email, usertype, address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+usertype+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Signup process completed'
                if usertype == "Restaurant Owner":
                    url = pyqrcode.create(username)
                    url.png('FoodOrderingApp/static/qrcodes/'+username+'.png', scale = 6)
        context= {'data':output}
        return render(request, 'Register.html', context)
      


