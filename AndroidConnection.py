from flask import *
from DbPackage.dbconnection import Db

app = Flask(__name__)
db = Db()

@app.route('/')
def hello():
    return "hello"


@app.route('/login',methods=["POST"])
def login():
    r = {}
    db = Db()
    email=request.form['email']
    pwd=request.form['password']
    print(email+" , "+pwd)
    q = "SELECT * FROM `login` WHERE `username`='"+email+"' AND `password`='"+pwd+"'"
    result = db.selectone(q)
    if result!=None:
        r['status'] = "success"
        r['lid'] = result['login_id']
        r['utype'] = result['usertype']
    else:
        r['status'] = "failed"
    print(jsonify({'results':r}))
    return jsonify(r)

@app.route('/StaffProfile',methods=["POST"])
def StaffProfile():
    r = {}
    db = Db()
    lid=request.form['lid']
    # lid='9'
    q="SELECT * FROM `staff` WHERE `loginid`='"+lid+"'"
    result = db.selectone(q)
    if result!=None:
        r['status'] = "success"
        r['name'] = result['staff_name']
        r['age'] = result['staff_age']
        r['address'] = result['staff_address']
        r['email'] = result['email']
        r['phone'] = result['phone_no']
        r['locality'] = result['locality']
        r['ward'] = result['ward']
        r['photo'] = result['staff_photo']
    else:
        r['status'] = "failed"
    print(jsonify({'results':r}))
    return jsonify(r)

@app.route('/ConsumerProfile',methods=["POST"])
def ConsumerProfile():
    r = {}
    db = Db()
    lid=request.form['lid']
    # lid='9'
    q="SELECT * FROM `consumer` WHERE `con_login_id`='"+lid+"'"
    result = db.selectone(q)
    if result!=None:
        r['status'] = "success"
        r['name'] = result['consumer_name']
        r['cno'] = result['consumer_no']
        r['email'] = result['email']
        r['address'] = result['address']
        r['rno'] = result['ration_no']
        r['phone'] = result['phone_no']
        r['locality'] = result['locality']
        r['ward'] = result['ward']
        r['photo'] = result['photo']
    else:
        r['status'] = "failed"
    print(jsonify({'results':r}))
    return jsonify(r)


@app.route('/view_assigned_works',methods=['POST'])
def view_assigned_works():
    db = Db()
    lid=request.form['lid']
    print(lid)
   # q = "SELECT `staff_assign`.*,`gas_request`.*,`consumer`.* FROM `consumer`,`gas_request`,`staff_assign` WHERE `consumer`.`con_login_id`=`gas_request`.`consumer_lid` AND `gas_request`.`request_id`=`staff_assign`.`request_id` AND `staff_assign`.`staff_login_id`='"+lid+"'"
    q="SELECT `staff_assign`.*,`gas_request`.*,`consumer`.* FROM `consumer`,`gas_request`,`staff_assign` WHERE `consumer`.`con_login_id`=`gas_request`.`consumer_lid` AND `gas_request`.`request_id`=`staff_assign`.`request_id` AND `staff_assign`.`staff_login_id`='"+lid+"' AND `gas_request`.`status`='Forwarded'"
    result = db.select(q)
    if (len(result) > 0):
        status = "success"
    else:
        status = "failed"
    return jsonify({'status': status, 'results': result})


@app.route('/view_request_status',methods=['POST'])
def view_request_status():
    db = Db()
    lid=request.form['lid']
    q = "SELECT * FROM `gas_request` WHERE `consumer_lid`='"+lid+"'"
    result = db.select(q)
    if (len(result) > 0):
        status = "success"
    else:
        status = "failed"
    return jsonify({'status': status, 'results': result})

@app.route('/gas_delivered',methods=['POST'])
def gas_delivered():
    db = Db()
    reqid=request.form['reqid']
    q = "UPDATE `gas_request` SET STATUS='Delivered' WHERE `request_id`='"+reqid+"'"
    result = db.update(q)
    q1 = "UPDATE `staff_assign` SET `delivery_date`=CURDATE(),`payment_status`='Paid' WHERE `request_id`='"+reqid+"'"
    result1 = db.update(q1)
    if (result1 > 0):
        status = "success"
    else:
        status = "failed"
    return jsonify({'status': status})


app.run(debug=True,threaded=True,host="0.0.0.0",port=5000)