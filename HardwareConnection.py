from flask import *
from flask import request
import pymysql
val=" "
try:
    con=pymysql.connect(host='localhost',user='root',password='',port=3306,database='lpg')
    cmd=con.cursor()
    print("connected")
except Exception as e:
    print(str(e))
app=Flask(__name__)
@app.route('/test',methods = ['POST', 'GET'])
def test():
    global val
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, database='lpg')
    cmd = con.cursor()
    b = request.get_data()
    c=b.decode("utf-8")
    print(c)
    if c=="A":
        val="LOW"
        cmd.execute("select * from gas_request where consumer_lid=5 and status='requested'")
        rq=cmd.fetchone()
        if rq==None:
            cmd.execute("insert into gas_request values(null,5,curdate(),curtime(),'requested')")
            con.commit()
    elif c=="B":
        val="GOOD"
    cmd.execute("select * from readings where id=1 ")
    res = cmd.fetchone()
    print(res)

    if res==None:
        cmd.execute("insert into readings values(null,'"+str(val)+"')")
        con.commit()
    else:
        cmd.execute("update readings set cylinder_status='"+str(val)+"' where id="+str(res[0])+"")
        con.commit()

    return 'ok'
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)