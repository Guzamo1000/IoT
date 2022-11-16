
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

web=Blueprint('web',__name__)

# web.permanent_session_lifetime = timedelta(minutes=1)
@web.route("/")
@web.route("/home", methods=['GET','POST'])
def home():
    if request.method=='GET':
        cur=mysql.get_db().cursor()
        cur.execute("select ID_thungrac,ViTriThungRac from thungrac")
        listkhuvuc=cur.fetchall()
        print(listkhuvuc)
        lskhuvuc=[]
        for i in listkhuvuc:
            dictkhuvuc={}
            dictkhuvuc["ID_thungrac"]=i[0]
            dictkhuvuc["ViTriThungRac"]=i[1]
            lskhuvuc.append(dictkhuvuc)
        print(lskhuvuc)
        
        return jsonify({"status":"success","listkhuvuc":lskhuvuc})
    if request.method=='POST':
        location=request.form['location']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        cur=mysql.get_db().cursor()
        cur.execute(f"select ID_khoangrac,ID_Thungrac, KhoiLuong, TenNhan from khoangrac where ID_Thungrac='{location}'")
        db=cur.fetchall()
        lsrachientai=[]
        for i in db:
            dictrachientai={}
            dictrachientai['ID_Khoangrac']=i[0]
            dictrachientai['ID_Thungrac']=i[1]
            dictrachientai['KhoiLuong']=i[2]
            dictrachientai['TenNhan']=i[3]
            lsrachientai.append(dictrachientai)
        # if start_time and end_time:
        

        return jsonify({"status":"success","soluongrachientai":lsrachientai})
        
        