from email.message import Message
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pytube import YouTube
from mysql.connector import connect
from youtube_scrap import get_all_video_url
import pymongo
import threading

app = Flask(__name__)

conn = connect(
    host="youtube-data.cgje4yzuebxp.us-east-1.rds.amazonaws.com",
    user="admin",
    password="subho987",
    database="sys"
)
cursor = conn.cursor()

client = pymongo.MongoClient(
    "mongodb+srv://subho9717:subho9717@ineuron.8npdrfs.mongodb.net/?retryWrites=true&w=majority")


@app.route('/', methods=['POST', 'GET'])
def index():  # put app's code here

    #mysql data fetch
    cursor.execute("select * from YouTubers_Table")
    fnl_data = [r for r in cursor.fetchall()]

    return render_template('index.html', data=fnl_data)


@app.route('/video_url', methods=["POST", "GET"])
def youtube():  # put app's code here
    if request.method == "POST":
        videourl = request.form['videourl']
        videounum = request.form['videounum']
        print(videourl,videounum)

        # delete all data from mysql
        cursor.execute("truncate YouTubers_Table")
        conn.commit()

        #mysql data fetch
        data = get_all_video_url(videourl, videounum)
        cursor.execute("select * from YouTubers_Table where Video_watch_url = '%s'" % data)
        fnl_data = [r for r in cursor.fetchall()]

        return redirect(url_for('index', data=fnl_data))
        # return jsonify({'data': videourl})
        # return url_for('index')

        # return render_template("index.html",data=fnl_data)

    return render_template("index.html")


@app.route('/video_comment', methods=["POST", "GET"])
def comment():  # put app's code here

    #fetch data from mongodb
    comm = request.form['comment']
    if comm:
        db = client['YouTube_Video_Data']
        coll = db['YouTubers_table']
        data = coll.find({"Video_watch_url": comm})
        fnldata = []
        for r in data:
            fnldata.append([r['Commenter_Name'], r['Comment']])

        return render_template("index.html", cdata=fnldata)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
