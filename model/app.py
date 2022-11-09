
import base64
import os
# import datetime
# from ODT import ObjectDetection
from db.db import mysql
from flask import Flask, jsonify, render_template, redirect,url_for,request,Blueprint, session, flash
from datetime import timedelta, datetime,date
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
        - data from khoangrac, ractrongkhoang,thungrac
        - data_bin: VitriThungRac,ID_thungrac
        - bin: khoangrac.ID_khoangrac,TenKhoang, SUM(KhoiLuong)
        - img
    # """
    if "id" not in session:
        return redirect(url_for("web.login"))
    if request.method=='GET':


        cur= mysql.get_db().cursor()
        cur.execute("select ViTriThungRac,ID_thungrac from thungrac") #ID and location
        data_bin=cur.fetchall()
        
        cur.execute("select khoangrac.ID_khoangrac,TenKhoang, SUM(KhoiLuong)   from khoangrac, ractrongkhoang where khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac group by TenKhoang")
        bin=cur.fetchall() #trash in bin
        #image
        cur.execute("select AnhRac, ThoiGianRacVao, NhanRac from khoangrac, ractrongkhoang, thungrac where thungrac.ID_thungrac=khoangrac.ID_Thungrac and khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac order by ThoiGianRacVao;")
        image=cur.fetchall()
        # return render_template("home.html", vitri=d,chart_5=chart_5, image=image)
        return jsonify({"status": "success", "Bin": data_bin, "data table bin": bin,"img":image})
    if request.method=="POST":
        time=request.form['time']
        location=request.form['location']
        print(time)
        cur=mysql.get_db().cursor()
        cur.execute(f"select * from khoangrac, ractrongkhoang, thungrac where ractrongkhoang.ThoiGianRacVao='{time}' and thungrac.ViTriThungRac='{location}' and thungrac.ID_thungrac=khoangrac.ID_Thungrac and khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac order by ThoiGianRacVao ;")
        data=cur.fetchall()
        return jsonify({"status":"success","data":data})
@web.route("/post_data_cam",methods=['POST'])
def insert_data_from_AI():
    """
    post data from model AI to database
    input: video
    output: save to table ractrongkhoang(img,time)
    """
    if request.method=="POST":
        try:
            data=request.get_json()
            id_bin=data['id_bin']
            label=data['label']
            image=data['img']
            time=str(datetime.now())
            directory = str(date.today())
            # Parent Directory path
            parent_dir = os.getcwd()
            # Path
            path = parent_dir+"\\"+"static"+"\\"+"images"+"\\"+directory
            print(f"path {path}")
            try:
                os.mkdir(path)
            except:
                print('Folder exist!')
            filename = str(datetime.now())
            specialChars = "!#$%^&*():.- "
            for specialChar in specialChars:
                filename = filename.replace(specialChar, '')
            url_save_to_db = "static\\images\\"+directory+"\\"+filename+".jpg"
            url_img = path+"\\"+filename
            url_img += '.jpg'
            with open(url_img, "wb") as f:
                f.write(base64.b64decode(image.encode('utf-8')))
            cur=mysql.get_db().cursor()
            print(f"label {label}")
            print(f"id_bin {id_bin}")
            id_khoang=cur.execute(f"select * from khoangrac,thungrac where TenNhan='{label}' and khoangrac.ID_Thungrac='{id_bin}' ")
            print(id_khoang)
            cur.execute(f"INSERT INTO `iot`.`ractrongkhoang` (`ID_khoangrac`, `AnhRac`, `ThoiGianRacVao`) VALUES ('{id_khoang}','{url_save_to_db}','{time}')")
            # cur.execute("INSERT INTO `iot`.`ractrongkhoang` (`ID_khoangrac`, `AnhRac`, `ThoiGianRacVao`) VALUES ({},{},{})".format())
            return jsonify({"status":"insert complete"})
        except Exception as e:
            print(e)
            return jsonify({"status":"failed","msg":str(e)})
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
            # return redirect(url_for('web.home'))
            print('Logged in success!')
            return jsonify({'status': "sus","account": account, 'password':password})
        else: 
            flash("User doesn't exist!", category="error")
            print("login fail")
            return jsonify({"status":"fail"})
@web.route("/reset/{ID_thungrac}",methods=['POST'])
def reset(ID_thungrac):
    """
    reset weight in bin
    input: ID_thungrac
    output: update table khoangrac in database
    """
    ID_thungrac=ID_thungrac
    cur=mysql.get_db().cursor()
    cur.execute(f"update khoangrac set KhoiLuong=1, SoLuong=1 where khoangrac.ID_khoangrac={ID_thungrac}")
    return jsonify({"status":"reset success"})
@web.route("/logout", methods=['GET','POST'])
def logout():
    """
    logout user
    reset session
    """
    session.clear()
    # return redirect(url_for("web.login"))
    return jsonify({"status": "logout success"})

@web.route("/setting", methods=['GET','POST'])
def setting():
    pass


