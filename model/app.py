import base64
import os
# import datetime
# from ODT import ObjectDetection
from db.db import mysql
from flask import Flask, jsonify, render_template, redirect,url_for,request,Blueprint, flash, session
from datetime import timedelta, datetime,date
import cv2
import urllib.request
import numpy as np
import json
from utils.group import group
web=Blueprint('web',__name__)

# web.permanent_session_lifetime = timedelta(minutes=1)
@web.route("/")
@web.route("/home", methods=['GET','POST'])
def home():
    if request.method=='GET':
        cur=mysql.get_db().cursor()
        cur.execute("select Id_thungrac,ViTriThungRac from thungrac")
        listvitri=cur.fetchall()
        cur.execute("select ID_khoangrac,ID_Thungrac,TenNhan,ViTriThungRac,SoLanDo, Sum(KhoiLuong) from (select khoangrac.ID_khoangrac, thungrac.ID_Thungrac, TenNhan, ViTriThungRac ,KhoiLuong,SoLanDo from ractrongkhoang,khoangrac, thungrac where thungrac.ID_thungrac=khoangrac.ID_Thungrac and khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac order by thungrac.ID_Thungrac) as T group by TenNhan")
        khoangrac=cur.fetchall()
        lskhuvuc=[]
        dict_vitri=[]
        for id_khoangrac in listvitri:
            vt={}
            vt["ID_thungrac"]=id_khoangrac[0]
            vt["ViTriThungRac"]=id_khoangrac[1]
            for i in khoangrac:
                if i[1]==id_khoangrac[0]:
                    dictkhuvuc={}
                    dictkhuvuc["ID_khoangrac"]=i[0]
                    # dictkhuvuc["ID_Thungrac"]=i[1]
                    dictkhuvuc['TenNhan']=i[2]
                    # dictkhuvuc['ViTriThungRac']=i[3]
                    dictkhuvuc['SoLanDo']=i[4]
                    dictkhuvuc['KhoiLuong']=i[5]
                    lskhuvuc.append(dictkhuvuc)
            vt['Khoangrac']=lskhuvuc
            dict_vitri.append(vt)
        # print(lskhuvuc)
        # lskhuvuc=set(lskhuvuc)
        return jsonify({"status":"success","listkhuvuc":dict_vitri})
    if request.method=='POST':
        location=request.form['location']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        cur=mysql.get_db().cursor()
        cur.execute(f"select NgayRacVao, KhoiLuong, TenNhan, ViTriThungRac from ractrongkhoang ,khoangrac, thungrac where thungrac.ID_thungrac='{location}' and thungrac.ID_Thungrac=khoangrac.ID_Thungrac and khoangrac.ID_khoangrac=ractrongkhoang.ID_khoangrac and NgayRacVao>='{start_time}' and NgayRacVao<='{end_time}' order by RacTrongKhoang.NgayRacVao")
        db=cur.fetchall()
        dir_time={}
        valuetime=db[0][0].strftime("%Y-%d-%m")
        # print(f"valuetime: {valuetime}")
        ngay=[]
        for i in db:
            ls_time={}
            tm=i[0].strftime("%Y-%d-%m")
            print(type(i))
            if tm==valuetime:
                
                ls_time['NgayRacVao']=tm
                ls_time['KhoiLuong']=i[1]
                ls_time['NhanRac']=i[2]
                ls_time['KhuVuc']=i[3]
                ngay.append(ls_time)
            else: 
                ngay=group(ngay)
                dir_time[valuetime]=ngay
                ngay=[]
                ls_time['NgayRacVao']=tm
                ls_time['KhoiLuong']=i[1]
                ls_time['NhanRac']=i[2]
                ls_time['KhuVuc']=i[3]
                ngay.append(ls_time)
                valuetime=tm
                # print(ls_time)

        dir_time[valuetime]=ngay
        print(dir_time)
        return jsonify({"status":"success","data": dir_time})


@web.route('/reset/<id_thungrac>/<id_khoangrac>/<SoLanDo>',methods=['GET'])
def reset(id_thungrac,id_khoangrac,SoLanDo):
    """
    reset KhoiLuong=0 and SoLanDo + 1
    """
    if request.method=='GET':
        id_thungrac=id_thungrac
        id_khoangrac=id_khoangrac
        SoLanDo=int(SoLanDo)+1
        print(SoLanDo)
        print(id_khoangrac)
        print(id_thungrac)
        cur=mysql.get_db().cursor()
        cur.execute(f"update khoangrac set KhoiLuong=0,SoLanDo='{SoLanDo}' where ID_Thungrac='{id_thungrac}' and ID_khoangrac='{id_khoangrac}'")
        mysql.get_db().commit()
     
        return jsonify({"Status":"Success"})
