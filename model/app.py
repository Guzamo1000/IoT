
from db.db import mysql
from flask import Flask, render_template, redirect,url_for,request,Blueprint, session, flash
from datetime import timedelta
import cv2
import urllib.request
import numpy as np



web=Blueprint('web',__name__)

web.permanent_session_lifetime = timedelta(minutes=1)
@web.route("/")
@web.route("/home", methods=['GET','POST'])
def home():
    """
    create page home
    input:
        - date
        - location
    output:
        - chart column by label (chart_1):
            + x: label
            + y: amount
        - chart round on total label (char_2):
            + percent of label
        - chart Roads of all labels (chart_3):
            + x: time
            + y: amount
        + chart columns of all labels (chart_4):
            + x: Time
            + y: amount
        + amount of trash currently in the bin (chart_5)
        + image (image)
    # """
    if "id" not in session:
        return redirect(url_for("web.login"))
    if request.method=='GET':
        cur= mysql.get_db().cursor()
        cur.execute("select ViTriThungRac from thungrac")
        d=cur.fetchall()
        # print(d)
        # loca=d[:][3]
        cur.execute("select khoangrac.ID_khoangrac,TenKhoang, SUM(KhoiLuong), TrangThai   from khoangrac, ractrongkhoang where khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac group by TenKhoang")
        chart_5=cur.fetchall()
        #image
        cur.execute("select AnhRac, ThoiGianRacVao, NhanRac from khoangrac, ractrongkhoang, thungrac where thungrac.ID_thungrac=khoangrac.ID_Thungrac and khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac order by ThoiGianRacVao;")
        image=cur.fetchall()
        return render_template("home.html", vitri=d,chart_5=chart_5, image=image)
    if request.method=="POST":
        time=request.form['time']
        location=request.form['location']
        print(time)
        cur=mysql.get_db().cursor()
        cur.execute(f"select * from khoangrac, ractrongkhoang, thungrac where ractrongkhoang.ThoiGianRacVao='{time}' and thungrac.ViTriThungRac='{location}' and thungrac.ID_thungrac=khoangrac.ID_Thungrac and khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac order by ThoiGianRacVao ;")
        data=cur.fetchall()
        #chart column by label
        chart_1=data[2:4] #x(TenKhoang): chart_1[0] and y(KhoiLuong): chart_1[1]
        #chart round on total label
        chart_2_query=data[2:4] #x(TenKhoang): chart_2[0] and y(KhoiLuong):chart_2[1]
        total_weight=sum(chart_2_query[1])
        chart_2=()
        for i in chart_2_query[1]:
            chart_2+=(i/total_weight)*100
        #chart Roads of all labels
        chart_3=[]
        chart_3_mass=data[3]
        chart_3.append(chart_3_mass)
        chart_3_time=data[9]
        chart_3.append(chart_3_time)
        #chart columns of all labels 
        chart_4=[]
        chart_4.append(data[9])
        chart_4.append(data[2])
        chart_4.append(data[3])
        return render_template("home.html",chart_1=chart_1,chart_2=chart_2,chart_3=chart_3,chart_4=chart_4,chart_5=chart_5,image=image)

@web.route("/login", methods=['GET','POST'])
def login():
    """
    Login user
    create session user
    """
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        account=request.form['account']
        password=request.form['password']
        cur=mysql.get_db().cursor()
        cur.execute(f"select * from users where accounts ='{account}' and passwords='{password}'")
        user = cur.fetchall()
        if user:
            # session['account']
            session['id']= user[0][0]
            flash("Logged in success!", category="success")
            return redirect(url_for('web.home'))
        else: 
            flash("User doesn't exist!", category="error")
            return render_template("login.html")
@web.route("/control")
def control():
    url='http://192.168.0.115/cam-lo.jpg'
    while(True):
        img=urllib.request.urlopen(url)
        img_np= np.array(bytearray(img.read()),dtype=np.uint8)
        frame=cv2.imdecode(img_np,-1)
        print(frame)
        cv2.imshow("img",frame)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            frame.release()
            cv2.destroyAllWindowns()
            break
@web.route("/reset/<ID_thungrac>",methods=['POST'])
def reset(ID_thungrac):
    """
    reset weight in bin
    input: ID_thungrac
    output: update table khoangrac in database
    """
    ID_thungrac=ID_thungrac
    cur=mysql.get_db().cursor()
    cur.execute(f"update khoangrac set KhoiLuong=1, SoLuong=1 where khoangrac.ID_khoangrac={ID_thungrac}")
    return redirect(url_for("web.home"))
@web.route("/logout", methods=['GET','POST'])
def logout():
    """
    logout user
    reset session
    """
    session.clear()
    return redirect(url_for("web.login"))

@web.route("/setting", methods=['GET','POST'])
def setting():
    pass


