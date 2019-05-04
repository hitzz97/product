Flask project:

Required modules to run: Flask and sqlite3.

File orientation:.

    products.db:Contains the database of product name, image location,comapny,price, location to buy from.
  
    server.py: the main python file to be run.
  
    Templates:contains the necessary html files like
  
        products.html:the file to be served when user visits for the first time.
    
        interest.html:the file to be server when user clicks the intrest link
    
        home.html:visited when user clicks on home.
    
Running the server:

  With python in the environment and required modules installed. just run the server.py file with same file structure as in the 
  repository. After running go the localhost:8000 to visit the website or http://127.0.0.1:8000/ to visit it.
  
Website interface:

  Automatically receive emails for the items you click intrested in. to receive the Email click on the Email icon on the bottom 
  right corner. you can also check your intrests in the intrest section.
  
  The search bar will work only if exactly same name of the product is typped.
  
  Press the heart icon on the products to make them fall into interested category.
  
  Also i am using a dummy gmail id to send email from you may change the gmail id and password in the server.py file.
  
CONFIGURING FOR EMAIL:

    my email will probably not work from your pc as google may ask for verification so for proper working of email system you
    must give your email and password in the server.py file where it is mentioned also you need to enable less secure app 
    permission for the gmail account through you  want to send emails.
    To enable less secure app go to settings in your gmail account and look for Less secured app permission and turn it ON.
