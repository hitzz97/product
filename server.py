from flask import Flask, render_template, redirect, url_for, request, jsonify,Response
import os
import sys
import sqlite3 as sql
import smtplib,ssl

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
'''this function EMAILs the user his or her interests" '''

''' '''
def valid():
	global Email
	Email=Email.lower()
	if '@' in Email and '.' in Email and (96<ord(Email[0])<123) and (96<ord(Email[-1])<123):
		return True
	return False

@app.route('/email_user')
def email_user():
	global INTERESTS,Email
	try:
		message="""\
		Subject: Your Interests\n\nMESSAGE.\n\nhave a nice day.
		"""
		body=""
		for i in INTERESTS:
			for name,image,company,price,buy in get_details(i):
				pro="Product name: {}\nCompany: {}\nPrice:RS. {}\nBuy at: {}\n\n".format(name,company,price,buy)
				body+=pro
		message=message.replace("MESSAGE",body)
		print("Emailing user:",Email)
		
		From="gooogle.atus@gmail.com"    #YOUR EMAIL ID HERE
		To=Email
		
		s=smtplib.SMTP('smtp.gmail.com',587)
		s.starttls()
		s.login("gooogle.atus@gmail.com","itzawesome")   #YOUR EMAIL AND PASSWORD
		
		s.sendmail(From,To,message)

		print("Message sent to:",Email)
		return jsonify("OK")
	except Exception as e:
		print(e)
		return jsonify("Error")
#function to retrieve details of products form the database
def get_details(name):
	conn=sql.connect(os.path.join("\\".join(os.path.abspath(__file__).split("\\")[:-1]),"products.db"))
	print("opened")
	cur=conn.execute("select name,img,company,price,buy from items where name like '{}%'".format(name.strip()))
	for row in cur:
		yield row[0],row[1],row[2],row[3],row[4]
#the function is querried on document load to print the producths on the html from database
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
#this function is invoked when the user enters the email and hence stores the user emails
@app.route('/get_email')
def get_email():
	global Email
	Email=str(request.args.get('email'))
	print("User Email received: ",Email)
	if valid():
		return jsonify("OK")
	return jsonify("ERROR")
#this function is invoked when the user presses on the interested buttons and hence the product name is sent from html to server
@app.route('/interested')
def interested():
	global INTERESTS
	INTERESTS.add(str(request.args.get('name')))
	print("User interests: ",INTERESTS)

	return "OK"

#this function serarches for the matching keyword and is invoked when the user searches
@app.route('/search')
def search():
	global output,NOT_FOUND
	name=str(request.args.get('name'))
	print(name)
	out=''
	try:
		for name,image,company,price,buy in get_details(name):
			html=output
			html=html.replace('NAME',name)
			html=html.replace('IMAGE',image)
			html=html.replace('COMPANY',company)
			html=html.replace('AMOUNT',price)
			out+=html
	except:
		return jsonify(NOT_FOUND)
	return jsonify(out)                      #add recommendations
#This function is used to print the intrested products on the page when user visits the interested url
@app.route('/get_interested_products')
def interested_products():
	global INTERESTS,output
	out=""
	print("Serving the INTERESTS from the database")
	if not INTERESTS:
		return jsonify(NOT_FOUND)
	for i in INTERESTS:
		html=output

		for name,image,company,price,buy in get_details(i):
		
			html=html.replace('NAME',name)
			html=html.replace('IMAGE',image)
			html=html.replace('COMPANY',company)
			html=html.replace('AMOUNT',price)
			out+=html
	return jsonify(out)
#this is the url of interested page 
@app.route('/interest',methods=["GET","POST"])
def interest_page():
    try:
        return render_template("interests.html")
    except Exception as e:
        print(e)
        return str(e)
#url to the home page 
@app.route('/home',methods=["GET","POST"])
def home():
    try:
        return render_template("home.html")
    except Exception as e:
        return str(e)
#url to the page when user visits for the first time 
@app.route('/',methods=["GET","POST"])
def page():
    try:
        return render_template("products.html")
    except Exception as e:
        print(e)
        return str(e)

#the ip can be changed to 127.0.0.1 or any thing else.
app.run('0.0.0.0',debug=True,port=PORT)
