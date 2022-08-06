from flask import Flask, request, render_template
from openpyxl import Workbook,load_workbook
import pandas as pd
import numpy as np


app = Flask(__name__)

@app.route('/')
def Definitions():
    return render_template('anasayfa.html')


@app.route('/',methods=['GET', 'POST'])
def upload():
    name= request.form["firstname"]
    tcidentityno= request.form["tcidentityno"]
    email= request.form["email"]
    department = request.form["department"]
    permissiontype = request.form["permissiontype"]
    permissionstart = request.form["permissionstart"]
    permissionfinished = request.form["permissionfinished"]
    startingwork = request.form["startingwork"]
    permissionperiod = request.form["permissionperiod"]

    dictionary = {
        'Adı':[name],
        'TC No':[tcidentityno],
        'Email':[email],
        'Çalıştığı Bölüm':[department],
        'İzin Türü':[permissiontype],
        'İzin Başlangıç':[permissionstart],
        'İzin Bitiş':[permissionfinished],
        'İşe Başlama':[startingwork],
        'İzin Süresi':[permissionperiod],
        }
    df = pd.DataFrame(dictionary)
    df = df.append(dictionary,ignore_index=True)
    writer = pd.ExcelWriter('deneme.xlsx',engine='xlsxwriter')
    df.to_excel(writer,sheet_name='Sheet1',index=False)
    writer.save()
    return render_template('anasayfa.html')
    