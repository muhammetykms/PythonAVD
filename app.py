from ast import arguments
from email import message
from os import sendfile
from turtle import left, onclick
from unicodedata import name
from flask import Flask, request, render_template, make_response
import numpy as np
from smtplib import SMTP
import json
import sendMail
import pandas as pd
from openpyxl import Workbook, load_workbook
import io
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def Definitions():
    return render_template('anasayfa.html')


wrongPass = "Şifreniz yanlış"
wrongUser = "User yanlış"
wrongLeaveDay = "İzin gününüz kalmadı"


@app.route('/', methods=['GET', 'POST'])
def upload():

    with open('metaUser.json') as readUser:
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

        if username != "":
            i = 0
            userList = len(metaUser)

            while i < userList:
                user = metaUser[i]
                dateNow = datetime.now()
                year = int(user['year'])
                mounth = int(user['mounth'])
                day = int(user['day'])
                jobStartDate = datetime(year, mounth, day)
                totalDay = dateNow-jobStartDate
                workDays = totalDay.days
                print(workDays)
                if user['user'] == username:
                    if user['pass'] == password:
                        if int(permissionperiod) > 0 and int(user['kalanIzinGunu']) > int(permissionperiod):
                            leftDays = int(user['kalanIzinGunu']) - int(permissionperiod)
                            user['kalanIzinGunu'] = str(leftDays)
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
                            print(user['kalanIzinGunu'])
                            # Excele Textbox'tan alınana verileri kaydetme
                            df = pd.DataFrame(dictionary)
                            # # df = df.append(dictionary,ignore_index=True)
                            writer = pd.ExcelWriter(
                                'pythondeneme.xlsx', engine='xlsxwriter')
                            df.to_excel(writer, sheet_name='Sheet1', index=True)
                            writer.save()
                            # #Mail Gönderme Fonksiyonu
                            sendMail.sendMail()
                            jsonDictionary = json.dumps(dictionary)
                            return jsonDictionary

                        else:
                            return wrongLeaveDay
                    else:
                        i += 1
                else:
                    i += 1
        else:
            return wrongUser
        