from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db

app = Flask(__name__)

dsn_hostname = "815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid = "tbc72932"
dsn_pwd = "4LioOqzrIBnfCt6c"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "30367"
dsn_security = "SSL"
dsn = ("DRIVER={0};"
"DATABASE={1};"
"HOSTNAME={2};"
"PORT={3};"
"UID={4};"
"PWD={5};"
"SECURITY={6};").format(dsn_driver,dsn_database,dsn_hostname,dsn_port,dsn_uid,dsn_pwd,dsn_security)
print(dsn)
try:
  conn = ibm_db.pconnect(dsn,"","")
  print("success")
except:
  print(ibm_db.conn_errormsg())

@app.route("/" , methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    sql_stmt = "insert into USER values(?,?,?,?)"
    stmt = ibm_db.prepare(conn, sql_stmt)
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    number = request.form['number']
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, email)
    ibm_db.bind_param(stmt, 3, password)
    ibm_db.bind_param(stmt, 4, number)
    try:
      ibm_db.execute(stmt)
      return redirect('/')
    except:
      print(ibm_db.stmt_errormsg())

  return render_template('index.html')


@app.route("/login",methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "select COUNT(*) from user where username='"+username+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        row = ibm_db.fetch_tuple(stmt5)
        if(row[0] ==1 ):
            return redirect("/shop/")
    return render_template("index.html")


@app.route("/shop/" , methods=['GET', 'POST'])
def shop():
  sql = "SELECT * FROM job"
  job_name = []
  job_location = []
  job_role = []
  job_number = []
  job_salary = []
  job_image = []
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_assoc(stmt)
  while dictionary != False:
    job_name.append(dictionary["NAME"])
    job_location.append(dictionary["LOCATION"])
    job_role.append(dictionary["ROLE"])
    job_number.append(dictionary["NUMBER"])
    job_salary.append(dictionary["SALARY"])
    job_image.append(dictionary["IMAGE"])
    dictionary = ibm_db.fetch_assoc(stmt)
  return render_template('shop.html', len = len(job_name), job_name = job_name, job_location = job_location, job_role = job_role, job_number = job_number, job_salary = job_salary, job_image = job_image)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')