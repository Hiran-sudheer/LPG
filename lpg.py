from flask import *
from DbPackage.dbconnection import Db

app = Flask(__name__)
db = Db()

@app.route('/')
def main():
   return render_template("login.html")

@app.route('/login',methods=['get','post'])
def login():
    uname=request.form['username']
    pswd=request.form['password']
    qrylog="SELECT * FROM login where username='"+uname+"' and password='"+pswd+"' and usertype='admin'"
    res=db.selectone(qrylog)
    if res==None:
        return "<script>alert('Invalid user or password');window.location='/'</script>"
    else:
       return redirect(url_for('home'))

@app.route('/adminhome')
def home():
   return render_template("admin_home.html")


@app.route('/add_consumer')
def add_consumer():
    q="SELECT DISTINCT(`locality`) FROM `staff`"
    result=db.select(q)
    return render_template("add_consumer.html",data=result)

@app.route('/consumer',methods=['get','post'])
def consumer():
    consumernumber=request.form['connum1']
    consumername=request.form['conname1']
    rationno=request.form['ration1']
    email=request.form['email1']
    address=request.form['address1']
    phone=request.form['phone1']
    f = request.files['photo1']
    locality=request.form['locality1']
    ward=request.form['ward1']
    pwd=request.form['pwd']

    qry="insert into login values(null,'"+email+"','"+pwd+"','consumer')"
    lid=db.insert(qry)

    ext = str.split(f.filename, '.')
    ext1 = ext[len(ext) - 1]

    photo = str(lid) + "." + ext1
    path = "E:\\p\\project\\lpg\\static\\consumerpics\\" + photo
    f.save(path)

    qry1="insert into consumer values(null,'"+consumernumber+"','"+consumername+"','"+str(lid)+"','"+rationno+"','"+email+"','"+address+"','"+phone+"','"+photo+"','"+locality+"','"+ward+"')"
    db.insert(qry1)
    return "<script>alert('Registration successful');window.location='/add_consumer'</script>"

@app.route('/add_staff')
def add_staff():
    return render_template("add_staff.html")

@app.route('/staff',methods=['get','post'])
def staff():
    staffname=request.form['staffname1']
    staffage=request.form['staffage1']
    staffaddress=request.form['staffaddress1']
    phonenumber=request.form['staffphone1']
    email=request.form['staffemail1']
    f = request.files['staffphoto1']
    locality=request.form['loc']
    ward=request.form['ward']
    pwd = request.form['pwd']
    qry = "insert into login values(null,'"+email+"','"+pwd+"','staff')"
    lid = db.insert(qry)

    ext = str.split(f.filename, '.')
    ext1 = ext[len(ext) - 1]

    photo = str(lid) + "." + ext1
    path = "E:\\p\\project\\lpg\\static\\staffpics\\" + photo
    f.save(path)

    qry2 = "insert into staff values(null,'"+str(lid)+"','"+staffname+"','"+staffage+"','"+staffaddress+"','"+phonenumber+"','"+email+"','"+photo+"','"+locality+"','"+ward+"')"
    db.insert(qry2)
    return "<script>alert('Registration successful');window.location='/'</script>"
    #return render_template('add_staff.html')

@app.route('/view_consumer')
def view_consumer():
    qryviewcon = "SELECT * FROM consumer"
    e = db.select(qryviewcon)
    return render_template("view_consumer.html",a=e)

@app.route('/edit_consumer/<id>')
def edit_consumer(id):
    e="select * from consumer where consumer_id='"+str(id)+"'"
    r=db.selectone(e)
    return render_template("edit_consumer.html",z=r)

@app.route('/update_consumer',methods=['get','post'])
def update_consumer():
    id=request.form['id']
    consumernumber = request.form['connum1']
    consumername = request.form['conname1']
    rationno = request.form['ration1']
    email = request.form['email1']
    address = request.form['address1']
    phone = request.form['phone1']
    f = request.files['photo1']
    locality = request.form['locality1']
    ward = request.form['ward1']

    if request.files['photo1'].filename =="":
        p="UPDATE `consumer` SET`consumer_no`='"+consumernumber+"',`consumer_name`='"+consumername+"',`ration_no`='"+rationno+"',`email`='"+email+"',`address`='"+address+"',`phone_no`='"+phone+"',`locality`='"+locality+"',`ward`='"+ward+"' where consumer_id='"+str(id)+"'"
    else:
        ext = str.split(f.filename, '.')
        ext1 = ext[len(ext) - 1]

        photo = str(id) + "." + ext1
        path = "E:\\p\\project\\lpg\\static\\staffpics\\" + photo
        f.save(path)
        p="UPDATE `consumer` SET`consumer_no`='" + consumernumber + "',`consumer_name`='" + consumername + "',`ration_no`='" + rationno + "',`email`='" + email + "',`address`='" + address + "',`phone_no`='" + phone + "',`photo`='" + photo + "',`locality`='" + locality + "',`ward`='" + ward + "' where consumer_id='" + str(id) + "'"

    j=db.update(p)
    return redirect(url_for('view_consumer'))

@app.route('/delete_consumer/<id>')
def delete_consumer(id):
    o="delete from consumer where consumer_id='"+str(id)+"'"
    db.delete(o)
    return redirect(url_for('view_consumer'))






@app.route('/view_staff')
def view_staff():
    qryviewstaff="SELECT * FROM staff"
    f=db.select(qryviewstaff)
    return render_template("view_staff.html",b=f)

@app.route('/edit_staff/<id>')
def edit_staff(id):
    s="select * from staff where staff_id='"+str(id)+"'"
    w=db.selectone(s)
    return render_template("edit_staff.html",y=w)

@app.route ('/update_staff',methods=['get','post'])
def update_staff():
    id=request.form['id']
    staffname = request.form['staffname1']
    staffage = request.form['staffage1']
    staffaddress = request.form['staffaddress1']
    phonenumber = request.form['staffphone1']
    email = request.form['staffemail1']
    f = request.files['staffphoto1']
    locality = request.form['loc']
    ward = request.form['ward']

    if request.files['photo1'].filename =="":
        d = "UPDATE `staff` SET `staff_name`='" + staffname + "',`staff_age`='" + staffage + "',`staff_address`='" + staffaddress + "',`phone_no`='" + phonenumber + "',`email`='" + email + "',`locality`='" + locality + "',`ward`='" + ward + "' where staff_id='" + str(id) + "'"
    else:
        ext = str.split(f.filename, '.')
        ext1 = ext[len(ext) - 1]

        photo = str(id) + "." + ext1
        path = "E:\\p\\project\\lpg\\static\\staffpics\\" + photo
        f.save(path)
        d = "UPDATE `staff` SET `staff_name`='" + staffname + "',`staff_age`='" + staffage + "',`staff_address`='" + staffaddress + "',`phone_no`='" + phonenumber + "',`email`='" + email + "',`staff_photo`='" + photo + "',`locality`='" + locality + "',`ward`='" + ward + "' where staff_id='" + str(id) + "'"

    j=db.update(d)
    return redirect(url_for('view_staff'))

@app.route('/delete_staff/<id>')
def delete_staff(id):
    g="delete from staff where staff_id='"+str(id)+"'"
    db.delete(g)
    return redirect(url_for('view_staff'))

@app.route('/view_request')
def view_request():
    qry="SELECT `gas_request`.*,`consumer`.* FROM `gas_request` inner join `consumer` on `gas_request`.`consumer_lid`=`consumer`.`con_login_id` where gas_request.status='requested'"
    #qry="select * from gas_request where status='requested'"
    w=db.select(qry)
    print(w)
    return render_template("view_request.html",t=w)

@app.route('/forward/<id>')
def forward(id):
    g="UPDATE gas_request SET STATUS='Forwarded' WHERE request_id='"+str(id)+"'"
    result=db.update(g)
    q1="SELECT staff.* FROM staff,consumer,gas_request WHERE `consumer`.`locality`=`staff`.`locality` AND `consumer`.`ward`=`staff`.`ward` AND `consumer`.`con_login_id`=`gas_request`.`consumer_lid` AND `gas_request`.`request_id`='"+id+"'"
    result1=db.selectone(q1)
    stafflid=result1['loginid']
    q2="INSERT INTO `staff_assign` (`request_id`,`staff_login_id`,`assign_date`) VALUES ('"+id+"','"+str(stafflid)+"',CURDATE())"
    res=db.insert(q2)
    if res>0:
        return redirect(url_for('view_request'))
    else:
        return "ERROR"



@app.route('/view_forwarded_request')
def view_forwarded_request():
    qry = "SELECT `gas_request`.*,`consumer`.*,`staff`.*,`staff_assign`.* FROM `gas_request`,`consumer`,`staff`,`staff_assign` WHERE `gas_request`.`consumer_lid`=`consumer`.`con_login_id` AND gas_request.status='forwarded' AND `gas_request`.`request_id`=`staff_assign`.`request_id` AND `staff_assign`.`staff_login_id`=`staff`.`loginid` ORDER BY consumer.locality"
    w=db.select(qry)
    print(w)
    return render_template("RequestFocus.html",res=w)


@app.route('/viewward/<locality>')
def viewward(locality):
    qry = "SELECT ward FROM `staff` WHERE `locality`='"+locality+"'"
    w=db.select(qry)
    print(w)
    return render_template("viewWard.html",res1=w)



if __name__ == '__main__':
    app.run()
