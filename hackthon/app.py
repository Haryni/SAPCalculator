from flask import Flask,render_template,redirect,session,g,url_for,request,flash
import os 
import sqlite3
 
app=Flask(__name__)
app.secret_key='sahith020'

app.config["UPLOAD_FOLDER"] = "static/image"

con=sqlite3.connect('database.db')
cur=con.cursor()
cur.execute("create table if not exists first(pid integer primary key,email text,username text,roll text,password text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

cur.execute("""
        CREATE TABLE IF NOT EXISTS user(
            pid INTEGER PRIMARY KEY,
            email text,
            name text,
            roll text,
            act TEXT,
            sap TEXT,
            status TEXT,
            college text,
            event text,
            date text,
            ac_status text,
            dept TEXT,
            year Text,
            section text,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

cur.execute("create table if not exists sduser(id integer primary key autoincrement,userid integer,act text,sap integer,user_image integer,filename text,status text,foreign key(userid) references user(pid))")
cur.execute("create table if not exists user_image(id integer primary key autoincrement,userid integer,filename text,foreign key(userid) references user(pid))")
cur.execute("create table if not exists admin(pid integer primary key,email text,username text,password text,role text,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
cur.execute("create table if not exists admin_detail(pid integer primary key,dept text,role text,section text,email text)")
cur.execute("create table if not exists admin_student(pid integer primary key,email text,st_id text,foreign key(st_id)references sduser(userid) )")

con.commit()

def fetch_sap(email):
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT sap FROM user WHERE email=?", (email,))
        sapdata = cur.fetchone()
        if sapdata:
            return sapdata['sap']
        else:
            return None
def update_sap(email,act,status, sap,event,date,college):
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE user SET sap=?, act=?, status=?,event=?,date=?,college=? WHERE email = ?", (sap,act,status,event,date,college,email))
        con.commit()
def add_signup(name, password, email, year, dept, section, roll):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        
        
        cursor.execute("SELECT * FROM first WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            
            cursor.execute("UPDATE first SET password=?, username=?, roll=? WHERE email=?", (password, name, roll, email))
            cursor.execute("UPDATE user SET year=?, dept=?, section=?,name=?,roll=? WHERE email=?", (year, dept, section, email,name,roll))
        else:
            
            cursor.execute("INSERT INTO first(email, password, username, roll) VALUES (?,?,?,?)", (email, password, name, roll))
            cursor.execute("INSERT INTO user(email, year, section, dept,name,roll) VALUES (?,?,?,?,?,?)", (email, year, section, dept,name,roll))
        
        connection.commit()

def add_admin(name, password, email, dept, role,section):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        
        
        cursor.execute("SELECT * FROM admin WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            
            cursor.execute("UPDATE admin SET password=?, username=?,email=?,role=? WHERE email=?", (password, name,email,role, email))
            cursor.execute("UPDATE admin_detail SET dept=?,email=?,section=? WHERE email=?", ( dept,email,section, email))
        else:
            
              cursor.execute("INSERT INTO admin(email, password,username,role) VALUES (?,?,?,?)", (email, password,name,role))
              cursor.execute("INSERT INTO admin_detail(email,dept,role,section) VALUES (?,?,?,?)", (email,dept,role,section))
        
        connection.commit()
class user:
      def init(self,username,email,status):
          self.username=username
          self.email=email
          self.status=status


@app.route('/')
def index():
     
     return render_template("select.html")

#######admin side start###########

@app.route('/adlogin',methods=['GET','POST'])
def adlogin():
    if request.method=="POST":
       email=request.form['email']
       password=request.form['password']
       with sqlite3.connect('database.db') as connection:
              connection.row_factory = sqlite3.Row
              cursor = connection.cursor()
              cursor.execute("SELECT * FROM admin WHERE email=? AND password=?", (email, password))
              data = cursor.fetchone()
              """if data:
                session["ademail"] = data["email"]
                session["adpassword"] = data["password"]
                session['adname']=data['username']
                session["admin_id"] = data["pid"]
                return redirect(url_for('adwelcome', username=session["ademail"]))
              else:
                 return redirect(url_for('adsignup'))"""
              
              
              if data['role']=='Advisor':
                  session["advisoremail"] = data["email"]
                  session["advisorpassword"] = data["password"]
                  session['advisorname']=data['username']
                  return redirect(url_for('advisor', username=session["advisoremail"]))
              
              elif data['role']=='Coordinator':
                  session["coemail"] = data["email"]
                  session["copassword"] = data["password"]
                  session['coname']=data['username']
                  return redirect(url_for('coordinator', username=session["coemail"]))

              else:
                  session['ademail']=data["email"]
                  session["adpassword"] = data["password"]
                  session['adname']=data['username']
                  return redirect(url_for('adwelcome', username=session["ademail"]))

    return render_template("adlogin.html")

####admin details start#######
add_admin("Reema","20-08-2005","hari020@kongu.edu","AIDS","Advisor","A")
add_admin("Jeni","21-08-2005","hari021@kongu.edu","AUTO","Advisor","B")
add_admin("Vasu","22-08-2005","hari022@kongu.edu","AIDS","HOD","none")
add_admin("Mukesh","23-08-2005","hari023@kongu.edu","AUTO","HOD","none")
add_admin("Sara","24-08-2005","hari024@kongu.edu","AIDS","Mentor","none")
add_admin("Nare","25-08-2005","hari025@kongu.edu","AIDS","Mentor","none")
add_admin("Peter","26-08-2005","hari026@kongu.edu","AUTO","Mentor","none")
add_admin("Sundar","27-08-2005","hari027@kongu.edu","AUTO","Mentor","none")
add_admin("Aneline","28-08-2005","hari028@kongu.edu","AUTO","Coordinator","none")
add_admin("Darshini","29-08-2005","hari029@kongu.edu","AUTO","Coordinator","none")
add_admin("Sneha","30-08-2005","hari030@kongu.edu","AIDS","Coordinator","none")
add_admin("Padma","31-08-2005","hari031@kongu.edu","AIDS","Coordinator","none")
######admin details end######
@app.route('/adwelcome')
def adwelcome():
    
    return render_template("adwelcome.html")
@app.route('/teach_status',methods=['GET','POST'])
def teach_status():
    with sqlite3.connect('database.db') as con:
            con.row_factory=sqlite3.Row 
            cur=con.cursor()
            cur.execute("select * from user order by timestamp desc limit 1 ")
            data=cur.fetchall()
   
    if not data:
        return render_template("teach_status.html", data=None)
    
    if request.method == "POST":
            
            selected_action = request.form.get('accept', request.form.get('reject'))

            if selected_action:
                
                cur.execute("UPDATE user SET status = ? WHERE pid = ?", (selected_action, data[0]['pid'])) 
                con.commit()
                
    return render_template("teach_status.html",data=data)
@app.route('/coordinator',methods=['GET','POST'])
def coordinator():
    coemail = session['coemail']
    with sqlite3.connect('database.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT dept FROM admin_detail WHERE email=?", (coemail,))
        co_data = cursor.fetchone()
    if co_data:
            co_section = co_data['dept']
            cursor.execute("SELECT * FROM user WHERE dept=?", (co_section,))
            student_data = cursor.fetchall()
            cursor.execute("SELECT * FROM user WHERE dept=?", (co_section,))
            image_data = cursor.fetchone()
            if image_data:
                img=image_data['pid']
                cursor.execute("SELECT * FROM user_image WHERE userid=?",(img,))
                imgdata=cursor.fetchall()
                return render_template("coordinator.html", student_data=student_data,imgdata=imgdata)
    data=session['email']
    if request.method == "POST":
            
            accept=request.form['accept']
            reject=request.form['rej']

            if accept:
               selected=accept
            else:
                selected=reject
                
            cur.execute("Insert into ac_status(acid,status) VALUES(?,?)", (session['user_id'],"selected")) 
            con.commit()
           

    return render_template("coordinator.html")
@app.route('/ac_status',methods=['GET','POST'])
def status():
    data=session['email']
    if request.method == "POST":
            
            accept=request.form['accept']
            reject=request.form['reject']

            if accept:
               selected=accept
            else:
                selected=reject
            cur.execute("UPDATE user SET status = ? WHERE email = ?", (selected, data)) 
            con.commit()

    return redirect(url_for('coordinator'))

@app.route('/advisor', methods=['GET', 'POST'])
def advisor():
    ademail = session['advisoremail']
    with sqlite3.connect('database.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT section FROM admin_detail WHERE email=?", (ademail,))
        advisor_data = cursor.fetchone()
        if advisor_data:
            advisor_section = advisor_data['section']
            cursor.execute("SELECT * FROM user WHERE section=?", (advisor_section,))
            student_data = cursor.fetchall()
            return render_template("advisor.html", user_sap=student_data)
        else:
            return "Advisor section not found"

    return render_template("advisor.html", user_sap=[])

@app.route('/st_status',methods=['GET','POST'])
def st_status():
     with sqlite3.connect('database.db') as con:
            con.row_factory=sqlite3.Row 
            cur=con.cursor()
            cur.execute("select * from user order by timestamp desc limit 1 ")
            data=cur.fetchall()
     return render_template("st_status.html",data=data)



####student side starts#############
@app.route('/reset',methods=['GET','POST'])
def reset():

    return render_template("resetpass.html")
@app.route('/stlogin',methods=['GET','POST'])
def stlogin():
    if request.method == "POST":
           email = request.form['username']
           password = request.form['password']
           with sqlite3.connect('database.db') as connection:
              connection.row_factory = sqlite3.Row
              cursor = connection.cursor()
              cursor.execute("SELECT * FROM first WHERE email=? AND password=?", (email, password))
              data = cursor.fetchone()
              
              if data:
                session["email"] = data["email"]
                session["password"] = data["password"]
                session['name']=data['username']
                session['roll']=data['roll']
                session['sap']=fetch_sap(email)
                session["user_id"] = data["pid"]
                return redirect(url_for('welcome', username=session["email"]))
              else:
                 return redirect(url_for('stlogin'))
      
     


              
    
    return render_template("student.html")

####student details######
add_signup("Sahith","20-08-2005","brothersa020@kongu.edu","I","AIDS","A","23ADR001")
add_signup("Hari","21-08-2005","brothersa021@kongu.edu","II","AUTO","A","23ADR002")
add_signup("Sai","22-08-2005","brothersa022@kongu.edu","II","AUTO","A","23ADR003")
add_signup("Sanjay","23-08-2005","brothersa023@kongu.edu","I","AUTO","A","23ADR004")
add_signup("Sham","24-08-2005","brothersa024@kongu.edu","I","AUTO","A","23ADR005")
add_signup("Haryni","25-08-2005","brothersa025@kongu.edu","I","AUTO","B","23ADR006")
add_signup("Abdul","26-08-2005","brothersa026@kongu.edu","II","AIDS","B","23ADR007")
add_signup("Selva","27-08-2005","brothersa027@kongu.edu","II","AIDS","B","23ADR008")
add_signup("Nithin","28-08-2005","brothersa028@kongu.edu","I","AIDS","B","23ADR009")
add_signup("Santhosh","29-08-2005","brothersa029@kongu.edu","I","AIDS","B","23ADR010")
#######student details end########


@app.route('/welcome')
def welcome():
    return render_template("stwelcome.html")
@app.route('/home', methods=['GET', 'POST'])

def home():
    if request.method == "POST": 
        try:
            act = request.form['act']
            status = request.form['status']
            sap = request.form['sap']
            event=request.form['event']
            college=request.form['college']
            date=request.form['date']
            update_sap(session['email'],act,status, sap,event,date,college)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO sduser(userid,act, status, sap) VALUES (?,?, ?, ?)", (session['user_id'],act, status, sap))
                con.commit()
           
                
            

            images = request.files['images']
            if images.filename != '':
               filepath = os.path.join(app.config["UPLOAD_FOLDER"], images.filename)
               images.save(filepath)

            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute("insert into user_image (userid,filename) values (?,?)" ,(session['user_id'] ,images.filename))
                connection.commit()
            print("Image uploaded successfully.")
            
            
            
           

        except sqlite3.Error as e:
            print("An error occurred while updating user activity status. Please try again later.")
            return redirect(url_for('index'))
    return render_template("home.html", sap=session.get('sap'))


@app.route('/sdview')
def sdview():
    if 'email' not in session:
        flash("You need to be logged in to view this page.")
        return redirect(url_for('stlogin'))
    
    username = session['email']
    with sqlite3.connect('database.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (username,))
        user_details = cursor.fetchone()
        cursor.execute("SELECT * FROM sduser WHERE userid = ? ", (user_details['pid'],))
        sddata = cursor.fetchall()
        
        cursor.execute("SELECT * FROM user_image WHERE userid = ? ", (user_details['pid'],))
        imgdata = cursor.fetchall()


     

     
    return render_template("sdview.html",sddata=sddata,imgdata=imgdata)

########students sdie ends###########
 
if __name__=="__main__":
    app.run(debug=True)