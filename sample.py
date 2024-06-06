from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo, MongoClient
import os
from werkzeug.security import check_password_hash,generate_password_hash
app = Flask(__name__)
app.secret_key='raj'
app.config["MONGO_URI"] = os.getenv('mongo_url')
client=MongoClient(os.getenv('mongo_url'))
db=client['FitTrac']

# mongo =PyMongo(app,uri="mongodb://localhost:27017/fitness_tracker")
# db=mongo.db
# Dummy user database
#users = {'username': 'password'}

@app.route('/')
def home():
      return render_template('dashboard.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
         return render_template('home.html')

    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
      if request.method=='POST':
            existing_user = db.user.find_one({'email': request.form['email']})
            if existing_user is None:
                  name=request.form['username']
                  email=request.form['email']
                  # password=request.form['confirmpassword']
                  hash_pass = generate_password_hash(request.form['confirmpassword'], method='pbkdf2:sha256')
                  query={'email':email}
                  doc ={'$set':{'email':email,'name':name,"password":hash_pass}}
                  db.user.update_one(query,doc,upsert=True)
                  flash("Registered successfully")
            # mongodb.user.insert_one({"name":name,"phone_no":phone_no,"email":email,"password":hash_pass})
                  return render_template('login.html')
            else:
                  flash("User already exists!")
                  return render_template("login.html")
      else:
            return render_template('login.html')
      


@app.route('/fp')
def fp():
   
      return render_template('fp.html')
      
@app.route('/logout')
def logout():
      # session['username'] = request.form['username']
      if "username" in session:
            session.pop('username', None)
            return render_template('home.html')
      return 'please login'

        

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
      if request.method=='POST':
            login_email= db.user.find_one({'email' : request.form['email']})
            session['username'] =login_email['name']
            session['email'] = login_email['email']
            if login_email:
                  if check_password_hash(login_email['password'], request.form['password']):
                         return render_template('dashboard.html',name=session['username'])
                  else:
                        return"Invalid username/password combination"
            else:
                  return 'Username not found'
      else:
            return render_template('dashboard.html', name=session['username'])
    # name=request.form['username']
#     if request.method=='POST':
#          em=request.form.get('email')
#          un=request.form.get('username')
#          cp=request.form.get('createpassword')
#          p=request.form.get('confrimpassword')
#          db.user.insert_many([{'email':em,'username':un,'createpassword':cp,'confrimpassword':p }])
#          return render_template('dashboard.html', username=un)

      #   return render_template('login.html')


@app.route('/started', methods=['GET','POST'])
def started():
      email=session['email']
      name=session['username']
      if request.method=='POST':
      
              we=int(request.form.get('weight'))
              he=int(request.form.get('height'))
              bmi=round(we/((he/100)**2),2)
              fin = "your bmi is " + str(bmi)
              query={'email':email}
              doc ={'$set':{'weight':we,'height':he,'bmi':bmi}}
              db.user.update_one(query,doc,upsert=True)
            #   db.user.update_one([{'weight':we,'height':he,'bmi':bmi}])
              if bmi<=18.5:
                    res="You are underweight"
              elif 18.5<=bmi<=24.9:
                    res="Healthy weight"
              elif 24.9<=bmi<=30.0:
                    res="Over weight"
              else:
                    res="obesity"
              return render_template('started.html',bmi=fin,resp=res, name=name) #  p=request.form.get('password')
      return render_template('started.html', name=name)



# @app.route('/bmi',)
# def calculate():
      #   if request.method=='POST':
      #         we=int(request.form.get('weight'))
      #         he=int(request.form.get('height'))
      #         bmi=round(we/((he/100)**2),2)
      #         db.user.insert_many([{'weight':we,'height':he,'bmi':bmi}])
      #         if bmi<=18.5:
      #               res="You are underweight"
      #         elif 18.5<=bmi<=24.9:
      #               res="Healthy weight"
      #         elif 24.9<=bmi<=30.0:
      #               res="Over weight"
      #         else:
      #               res="obesity"
      #         return render_template('bmi.html',bmi=bmi,resp=res)
        
      #   return render_template('started.html')

# @app.route('/weightgain')
# def weightgain():
#       return render_template("weightgain.html")


# @app.route('/weightloss')
# def weightloss():-=909=========================]
#       if request.method=='POST':
#             if "name":
#                   return render_template('weightloss.html')


@app.route('/togg')
def togg():
      name=session['username']
      return render_template('togg.html', name=name)

@app.route('/about')
def about():
      name=session['username']
      return render_template('about.html', name=name)

@app.route('/exer')
def exer():
      name=session['username']
      return render_template('exer.html', name=name)
      

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")