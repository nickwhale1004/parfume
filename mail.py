import smtplib

def sendEmail(message):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    email = "nikita.shlayh@gmail.com"
    password = 'cfcnealmwyauocvl'
    smtpObj.starttls()
    smtpObj.login(email, password)
    smtpObj.sendmail(email, "nikita-shlyah@yandex.ru", message.encode('utf-8'))
