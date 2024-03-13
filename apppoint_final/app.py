from flask  import Flask, render_template, request, redirect, url_for
import jinja2
import mysql.connector
import uuid
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    password = "root",
    database = "appoint"
)

mycursor = mydb.cursor()

usr_dict = {'admin' : 'pwd1'}

@app.route('/')  
def home():
    return render_template('/blogin.html')
@app.route('/admin1')  
def home10():
    return render_template('/admin.html')


@app.route('/blogin')  
def home7():
    return render_template('/index.html')
@app.route('/home')  
def home8():
    return render_template('/home.html')
 
@app.route('/upcomingappointments')
def upcomingappointments():
    query = "select * from appointments"
    mycursor.execute(query)
    data = mycursor.fetchall()
    
    return render_template('upcomingappointments.html', sqldata=data)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/makeanappointment', methods = ['GET', 'POST'])
def addemp():
    if request.method == 'POST':
       appointment_id = str(uuid.uuid4())
       service_name = request.form['service_name']
       person_name = request.form['person_name']
       appointment_date = str(request.form['appointment_date'])
       appointment_time = str(request.form['appointment_time'])
       appointment_duration = str(request.form['appointment_duration'])
       appointment_description = request.form['appointment_description']
       query = "insert into appointments values (%s, %s, %s, %s, %s, %s, %s)"
       data = (appointment_id, service_name, person_name, appointment_date, appointment_time, appointment_duration, appointment_description)
       mycursor.execute(query, data)
       mydb.commit()
       return render_template('/home.html', msg = "Booking Successful")
    else:
        return render_template('/makeanappointment.html', msg = "Error")

@app.route('/deleteappointment', methods=['POST', 'GET'])
def deleteappointment():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        query = "delete from appointments where appointment_id like '%{}%'".format(appointment_id)
        mycursor.execute(query)
        data = mycursor.fetchall()
        mycursor.execute(query, data)
        mydb.commit()
        return render_template('home.html', msg = "Successfully Deleted the appointment")
    if request.method == 'GET':
        query = "select * from appointments"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('deleteappointment.html', sqldata = data)


@app.route('/updateappointment', methods=['POST', 'GET'])
def updateappointment():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        appointment_duration = request.form.get('appointment_duration')
        query = f"update appointments set appointment_duration = '{appointment_duration}' where appointment_id = '{appointment_id}'"
        mycursor.execute(query)
        data = mycursor.fetchall()
        mycursor.execute(query, data)
        mydb.commit()
        return render_template('home.html', msg = "Successfully Updated the appointment")
    if request.method == 'GET':
        query = "select * from appointments"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('updateappointment.html', sqldata = data)
    
@app.route('/analytics')
def analytics():
    query = "select * from appointments"
    mycursor.execute(query)
    data = mycursor.fetchall()
    service_dict = {'doctor':0, 'hairdresser':0, 'technician':0}
    for j in service_dict:
        for i in range(len(data)):
            if(j==data[i][1]):
                service_dict[data[i][1]]+=1
    services = list(service_dict.keys())
    counts = list(service_dict.values())

    plt.bar(services, counts, color='skyblue')
    plt.xlabel('Services')
    plt.ylabel('Count')
    plt.title('Services vs Count')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()

    return render_template('analytics.html', plot_data = plot_data)

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/hm')
def home1():
    return render_template('home1.html')
@app.route('/hm2')
def home2():
    return render_template('home2.html')


@app.route('/hm2', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        name = request.form.get('Name')
        email = request.form.get('Email')
        password = request.form.get('Password')
       
 
        query = "insert into login values (%s,%s,%s)"
        data=(name,email,password)
       
       
        mycursor.execute(query,data)
        mydb.commit()
        return render_template('index.html')
    return render_template('home1.html')


@app.route('/hm',methods=['post'])
def login():
   
    uname = request.form['Email']
    pwd = request.form['Password']
   
   
    # Execute a query to retrieve user data
    mycursor.execute("SELECT password FROM login WHERE email = %s", (uname,))
    user = mycursor.fetchone()

    if uname == 'admin@gmail.com':
     return render_template('admin.html')
 
    if user:
        # Verify the hashed password
        if user[0] == pwd:
            return render_template('home.html', msg=f"{uname}")
        else:
            return render_template('index.html', msg="Invalid Password")
    else:
        return render_template('index.html', msg="Invalid Username")

if __name__=='__main__':
    app.run(debug=True, port = 4001)