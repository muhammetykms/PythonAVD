from ast import arguments
from email import message
from os import sendfile
from unicodedata import name
from flask import Flask, request, render_template , make_response
import numpy as np
from smtplib import SMTP
import json
import sendMail
import pandas as pd
from openpyxl import Workbook,load_workbook
import io

app = Flask(__name__)

@app.route('/')
def Definitions():
    return render_template('anasayfa.html')





@app.route('/',methods=['GET', 'POST'])
def upload():
    #Formdaki verileri teker teker bir değişkene atadık.
    firstname= request.form["firstname"]
    tcidentityno= request.form["tcidentityno"]
    email= request.form["email"]
    department = request.form["department"]
    permissiontype = request.form["permissiontype"]
    permissionstart = request.form["permissionstart"]
    permissionfinished = request.form["permissionfinished"]
    startingwork = request.form["startingwork"]
    permissionperiod = request.form["permissionperiod"]
    #Atama Yaptığımız değişkenleri burada bir dictionary haline getiriyoruz.
    dictionary = {
    'Adı':[firstname],
    'TC No':[tcidentityno],
    'Email':[email],
    'Çalıştığı Bölüm':[department],
    'İzin Türü':[permissiontype],
    'İzin Başlangıç':[permissionstart],
    'İzin Bitiş':[permissionfinished],
    'İşe Başlama':[startingwork],
    'İzin Süresi':[permissionperiod],
     }
    #Excele Textbox'tan alınana verileri kaydetme
    df = pd.DataFrame(dictionary)
    # # df = df.append(dictionary,ignore_index=True)
    writer = pd.ExcelWriter('pythondeneme.xlsx',engine='xlsxwriter')
    df.to_excel(writer,sheet_name='Sheet1',index=True)
    writer.save()
    # #Mail Gönderme Fonksiyonu
    sendMail.sendMail()
    return dictionary


    


    