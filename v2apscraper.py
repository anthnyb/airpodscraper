from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import urllib.request, json 
import time

stores_instock = []

def scrape():
    with urllib.request.urlopen("https://www.isinstock.com/apple/airpods/white/locations.json?latitude=33.4438042&longitude=-112.13109859999997&meters=32187&nearby=true") as url:
        data = json.loads(url.read().decode())
        count = 0
        for store in data['features']:
            store_name = data['features'][count]['properties']['title']
            available = data['features'][count]['properties']['available']

            if 'AT&T' not in store_name:
                if available:
                    stores_instock.append(store_name)
            count = count + 1

def send_email(stores):
    text = "There are airpods in these stores: " + ", ".join(stores)

    myEmail = input('What Email is this coming from?')
    myPassword = input('Email Password: ')
    recipient1 = 'anthony.benites17@gmail.com'

    recipients = [myEmail, recipient1]

    msg = MIMEMultipart()
    text = MIMEText(text)
    msg.attach(text)

    # Send email
    msg['Subject'] = "Airpods in stock! "
    msg['To'] = ", ".join(recipients)
    msg['From'] = myEmail

    mail = smtplib.SMTP(host='smtp.office365.com', port=587)
    mail.starttls()
    mail.login(myEmail, myPassword)
    mail.sendmail(myEmail, recipients, msg.as_string())
    mail.quit()

while True:
    scrape()
    if stores_instock:
        send_email(stores_instock)
        print("Airpods in stock! Email sent!")
    else:
        print("No stores have airpods in stock")
    time.sleep(200)
