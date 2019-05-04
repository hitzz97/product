from flask import Flask, render_template, redirect, url_for, request, jsonify,Response
import os
import sys
import sqlite3 as sql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app=Flask(__name__)
Email=""
PORT = int(os.getenv('PORT', 8000))

'''THe output i am returning from the server '''
output='''
<div class="items" style="position:relative;">
				<img src=IMAGE width="300px" height="200px" style="padding-left:2.5%;padding-top:2.5%">
				<hr width="50%" style="background-color:#000000;height:1.5px">
				<div style="padding-bottom:4%;" class="ani">
				<font size="5px" color="green" style="padding-left:7%">
					NAME
				</font>
				<br>
				<font size="4px" color="black" style="padding-left:7%">
					COMPANY
				</font>
				<br>
				<font size="5px" color="black" style="padding-left:7%">
					Price: Rs AMOUNT
				</font>
				</div>
				<div style="position:absolute;top:3%;right:8%;">
					<img id="NAME" class="heart" src="https://image.flaticon.com/icons/svg/148/148836.svg" height="25px" width="25px" style="padding-left:46%" onclick="intrested(this);">
				</div>
			</div>
'''
NOT_FOUND='''
<div>
				<div style="position: relative;top:20%;left:30%">
					<img src="https://comps.canstockphoto.com/not-found-red-stamp-text-image_csp28055073.jpg">					
				</div>
				<font size="6px" color="black" style="padding-left:22%" >The Item you are looking for is not present with us</font>
				<br>
				<font size="4px" color="black" style="padding-left:38%" >Please refine your search</font>	
			</div>
'''
INTERESTS=set([])
'''this function searches the file database.txt for matches and the format
of each line in database.txt is "name:website address" '''

''' '''
@app.route('/email_user')
def email_user():
	global INTERESTS,Email
	try:
		body=""
		for i in INTERESTS:
			name,image,company,price,buy=get_details(i)
			pro="Product name: {}\nCompany: {}\nPrice:RS. {}\nBuy at: {}\n\n".format(name,company,price,buy)
			body+=pro
		print("Emailing user:",Email)
		text=MIMEMultipart()
		text['From']="gooogle.atus@gmail.com"
		text['To']=Email
		text['Subject']="Your Interests"
		text.attach(MIMEText(body,"plain"))
		s=smtplib.SMTP('smtp.gmail.com',587)
		s.starttls()
		s.login("gooogle.atus@gmail.com","itzawesome")
		# s.sendmail('hitzzkushwaha@gmail.com','gooogle.atus@gmail.com',text)
		s.send_message(text)
		s.quit()
		print("Message sent to:",Email)
		return jsonify("OK")
	except Exception as e:
		Print(e)
		return jsonify("Error")

def get_details(name):
	conn=sql.connect(os.path.join("\\".join(os.path.abspath(__file__).split("\\")[:-1]),"products.db"))
	print("opened")
	cur=conn.execute("select name,img,company,price,buy from items where name='{}'".format(name))
	for row in cur:
		return row[0],row[1],row[2],row[3],row[4]

@app.route('/get_products')
def get_products():
	global output
	conn=sql.connect(os.path.join("\\".join(os.path.abspath(__file__).split("\\")[:-1]),"products.db"))
	print("database connected\n")
	cur=conn.execute("select name,img,company,price from items")
	print("Serving the Products from the database")
	out=""
	for row in cur:
		html=output
		name,image,company,price=row[0],row[1],row[2],row[3]
		html=html.replace('NAME',name)
		html=html.replace('IMAGE',image)
		html=html.replace('COMPANY',company)
		html=html.replace('AMOUNT',price)
		out+=html
	conn.close()
	return jsonify(out)

@app.route('/get_email')
def get_email():
	global Email
	Email=str(request.args.get('email'))
	print("User Email received: ",Email)
	return "OK"

@app.route('/interested')
def interested():
	global INTERESTS
	INTERESTS.add(str(request.args.get('name')))
	print("User interests: ",INTERESTS)

	return "OK"


@app.route('/search')
def search():
	global output,NOT_FOUND
	name=str(request.args.get('name'))
	print(name)
	html=output
	try:
		name,image,company,price,buy=get_details(name)
		html=html.replace('NAME',name)
		html=html.replace('IMAGE',image)
		html=html.replace('COMPANY',company)
		html=html.replace('AMOUNT',price)
	except:
		return jsonify(NOT_FOUND)
	return jsonify(html)                        #add recommendations

@app.route('/get_interested_products')
def interested_products():
	global INTERESTS,output
	out=""
	print("Serving the INTERESTS from the database")
	if not INTERESTS:
		return jsonify(NOT_FOUND)
	for i in INTERESTS:
		html=output
		name,image,company,price,buy=get_details(i)
		html=html.replace('NAME',name)
		html=html.replace('IMAGE',image)
		html=html.replace('COMPANY',company)
		html=html.replace('AMOUNT',price)
		out+=html
	return jsonify(out)

@app.route('/interest',methods=["GET","POST"])
def interest_page():
    try:
        return render_template("interests.html")
    except Exception as e:
        return str(e)

@app.route('/home',methods=["GET","POST"])
def home():
    try:
        return render_template("home.html")
    except Exception as e:
        return str(e)

@app.route('/',methods=["GET","POST"])
def page():
    try:
        return render_template("products.html")
    except Exception as e:
        return str(e)


app.run('0.0.0.0',debug=True,port=PORT)
