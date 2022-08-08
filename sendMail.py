
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def sendMail():
    try:

        #Dosyayı gönderecek olan mail adresi
        fromaddress = "ramazan_yikmis@hotmail.com"
        #Dosyayı alacak olan mail adresi
        toaddress = "ramazan.yikmis@icloud.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddress
        msg['To'] = toaddress
        #Mail Başlığı
        msg['Subject'] = "İzin Formu"
        #Mail Konusu
        body = "Gest-Avd İzin Formu Excel Verileri"
        msg.attach(MIMEText(body, 'plain'))
        #Gönderilecek Dosya Adını tanımlıyoruz
        filename = "pythondeneme.xlsx"
        #Dosyayı Açıyoruz
        attachment = open("pythondeneme.xlsx", "rb")
        part = MIMEBase('application', 'octet-stream')
        #Dosyayı okuyoruz
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        #Hangi mail türünde gönderim yapılacaksa o mailin IMAP verileri
        server = smtplib.SMTP("outlook.office365.com",587)
        #Mailin Güvenliği İçin Kullanılan Komut
        server.starttls()
        #Bilgi Doğrulama & Sorgulama
        server.login(fromaddress, "5462468144ra")
        text = msg.as_string()
        server.sendmail(fromaddress, toaddress, text)
        server.quit()
        print("Mail İşlemi Başarılı")
    except Exception as e:
            print("Hata Oluştu\n{0}".format(e))

