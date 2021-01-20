from flask import Flask, render_template, request
import requests
import mysql.connector

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getvalue():
    fr = request.form['from']
    to = request.form['to']
    dod = request.form['dod']
    adults = request.form['noa']
    children = request.form['noc']
    infants = request.form['noi']
    response = requests.get(
        "http://developer.goibibo.com/api/search/?app_id=1a7d2727&app_key=a7e093b62d62716c630ffe3017553829&format=json&source={FROM}&destination={TO}&dateofdeparture={DOD}&seatingclass={sc}&adults={ADULTS}&children={CHILDREN}&infants={INFANTS}&counter=100".format(
            FROM=fr, TO=to, DOD=dod, sc='E', ADULTS=adults, CHILDREN=children, INFANTS=infants))

    for q in response.json()['data']['onwardflights']:

        airname = q['airline']
        arrdate = ""
        for d in range(0, 9):
            arrdate += q['arrdate'][d]
        arrterm = q['arrterminal']
        arrtime = q['arrtime']
        depterm = q['depterminal']
        deptime = q['deptime']
        dur = q['duration']
        tbf = "₹" + str(q['fare']['totalfare'])
        fc = q['flightcode']
        fn = q['flightno']
        sa = q['seatsavailable']
        rs = q['warnings']

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="*******************",
            database='dp'
        )

        mycursor = mydb.cursor()
        sql = "insert into flights values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val = ("'" + airname + "'", "'" + arrdate + "'","'" + arrterm+ "'", "'" + arrtime + "'", "'" + depterm + "'",
               "'" + deptime + "'", "'" + dur + "'", "'" + tbf + "'", "'" + fc + "'", "'" + fn + "'","'" + sa+ "'",
               "'" + rs + "'")

        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('results.html', an=airname, ad=arrdate, atime=arrtime, aterm=arrterm, dterm=depterm,
                               dtime=deptime, dur=dur, tbf=tbf, fc=fc, fn=fn, sa=sa, rs=rs)


if __name__ == "__main__":
    app.run()
    