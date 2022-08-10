from ast import arguments
from email import message
from os import sendfile
from turtle import onclick
from unicodedata import name
from flask import Flask, request, render_template, make_response
import numpy as np
from smtplib import SMTP
import json
import sendMail
import pandas as pd
from openpyxl import Workbook, load_workbook
import io

app = Flask(__name__)


@app.route('/')
def Definitions():
    return render_template('anasayfa.html')


wrongPass = "Şifreniz yanlış"
wrongUser = "User yanlış"


@app.route('/', methods=['GET', 'POST'])
def upload():
    readUser = open('metaUser.json')
    data = json.load(readUser)
    metaUser = data['users']
    # Formdaki verileri teker teker bir değişkene atadık.
    username = request.form["username"]
    password = request.form["password"]
    tcidentityno = request.form["tcidentityno"]
    email = request.form["email"]
    department = request.form["department"]
    permissiontype = request.form["permissiontype"]
    permissionstart = request.form["permissionstart"]
    permissionfinished = request.form["permissionfinished"]
    startingwork = request.form["startingwork"]
    permissionperiod = request.form["permissionperiod"]
    radioButton = request.form["radio"]

    i = 0
    userList = len(metaUser)
    while i < userList:
        user = metaUser[i]
        if user['user'] == username:
            if user['pass'] == password:
                # Atama Yaptığımız değişkenleri burada bir dictionary haline getiriyoruz.
                dictionary = {
                    'Firma Adı': [radioButton],
                    'Kullanıcı Adı': [username],
                    'Şifre': [password],
                    'TC No': [tcidentityno],
                    'Email': [email],
                    'Çalıştığı Bölüm': [department],
                    'İzin Türü': [permissiontype],
                    'İzin Başlangıç': [permissionstart],
                    'İzin Bitiş': [permissionfinished],
                    'İşe Başlama': [startingwork],
                    'İzin Süresi': [permissionperiod],
                }
                # Excele Textbox'tan alınana verileri kaydetme
                df = pd.DataFrame(dictionary)
                # # df = df.append(dictionary,ignore_index=True)
                writer = pd.ExcelWriter(
                    'pythondeneme.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=True)
                writer.save()
                # #Mail Gönderme Fonksiyonu
                sendMail.sendMail()
                return dictionary
            else:
                return wrongPass
        else:
            return wrongUser
    i += 1
