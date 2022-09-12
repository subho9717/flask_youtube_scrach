from time import time
import requests
from pytube import YouTube,Channel
from googleapiclient.discovery import build
from pydrive.auth import GoogleAuth
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
from pydrive.drive import GoogleDrive
import os
from mysql.connector import  connect
import base64
import pymongo
import threading
import time

drive = GoogleDrive(gauth)

#google api key
api_key = 'AIzaSyByQMt4VH7I4BylDHElcxxilZVFhMwWWAc'
youtube = build('youtube', 'v3', developerKey=api_key)

box = []

#mysql connection
conn = connect(
    host="youtube-data.cgje4yzuebxp.us-east-1.rds.amazonaws.com",
    user="admin",
    password="subho987",
    database = "sys"
)
cursor = conn.cursor()

#mongo db connection
client = pymongo.MongoClient("mongodb+srv://subho9717:subho9717@ineuron.8npdrfs.mongodb.net/?retryWrites=true&w=majority")


def video_data(url_video, final_url):
    # video link
    # print(url_video,final_url)
    
    #video link 
    video_link1 = final_url

    #youtuber name extract
    video_author = YouTube(final_url).author

    #for extract the title,video like count ,comment count, thumbnail of video url from  video url
    mqldata1 =[]
    title_data = youtube.videos().list(part='snippet,contentDetails,statistics', id=url_video).execute()
    for t in title_data['items']:
        title = t["snippet"]["title"]
        title = str(title).replace("?", "_").replace("|", "_").replace("/", "_").replace("'\'", "_").replace("~", "_").replace("`", "_").replace("!", "_").replace("@", "_").replace("#", "_").replace("$", "_").replace("%", "_").replace("^", "_").replace("&", "_").replace("*", "_").replace("(", "_").replace(")", "_").replace("-", "_").replace("+", "_").replace("=", "_").replace(":", "_").replace(";", "_").replace('"""', "_").replace("'", "_").replace(",", "_").replace("<", "_").replace(">", "_")
        likeCount = t['statistics']['likeCount']
        commentCount = t['statistics']['commentCount']
        thumbnails = t["snippet"]['thumbnails']['high']['url']
        mqldata1.append([title,likeCount,commentCount,thumbnails])
        # print(thumbnails)

    data = youtube.commentThreads().list(part='snippet', videoId=url_video, maxResults='100',
                                         textFormat="plainText").execute()

    #for extract commenter name and comments
    for i in data["items"]:
        name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        box.append([name, comment])

    while ("nextPageToken" in data):

        data = youtube.commentThreads().list(part='snippet', videoId=url_video, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]

            box.append([name, comment])

    

    #upload youtubername,video title, commenter name,comments,thumbnaiand,video url data in mongodb 
    def mongo(thumbnails,title,mqldata1):

        ##########################################Image
        imglink = thumbnails
        image = requests.get(imglink).content
        img_title = str(title).replace("?", "_").replace("|", "_").replace("/", "_").replace("'\'", "_").replace("~", "_").replace("`", "_").replace("!", "_").replace("@", "_").replace("#", "_").replace("$", "_").replace("%", "_").replace("^", "_").replace("&", "_").replace("*", "_").replace("(", "_").replace(")", "_").replace("-", "_").replace("+", "_").replace("=", "_").replace(":", "_").replace(";", "_").replace('"""', "_").replace("'", "_").replace(",", "_").replace("<", "_").replace(">", "_")
        imgtitleg ='media/images/'+ img_title + '.jpg'
        
        with open(imgtitleg, "wb") as file:
            file.write(image)

        dir = r"media/images"
        all_files = os.listdir(dir)
        for f in all_files:
            path = os.path.join(dir, f)
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                # print(encoded_string)
                for i in box:
                    for j in mqldata1:
                        data = {'Author': video_author,
                                'title':j[0].replace(" ", "_").replace("?", "_").replace("|", "_").replace("/", "_").replace("'\'", "_").replace("~", "_").replace("`", "_").replace("!", "_").replace("@", "_").replace("#", "_").replace("$", "_").replace("%", "_").replace("^", "_").replace("&", "_").replace("*", "_").replace("(", "_").replace(")", "_").replace("-", "_").replace("+", "_").replace("=", "_").replace(":", "_").replace(";", "_").replace('"""', "_").replace("'", "_").replace(",", "_").replace("<", "_").replace(">", "_"),
                                'Commenter_Name': i[0],
                                'Comment': i[1],
                                'thumbnail':encoded_string,
                                'Video_watch_url': url_video
                                }
                        db = client['YouTube_Video_Data']
                        coll = db['YouTubers_table']
                        coll.insert_one(data)

    #upload video in google drive

    def video1(final_url):

        ######################################################
        videofolder = '1qDl8vUE3qy0yBhxTIz1ztfNQ3KDsWVB4'
        youtube_1 = YouTube(final_url)
        videos_1 = youtube_1.streams.all()
        vid = list(enumerate(videos_1))
        strm = 0
        videos_1[strm].download("media/video/")
        dir = r"media/video"
        all_files = os.listdir(dir)

        for f in all_files:
            path = os.path.join(dir, f)
            vfname = str(f).replace(" ", "_").replace("?", "_").replace("|", "_").replace("/", "_").replace("'\'", "_").replace("~", "_").replace("`", "_").replace("!", "_").replace("@", "_").replace("#", "_").replace("$", "_").replace("%", "_").replace("^", "_").replace("&", "_").replace("*", "_").replace("(", "_").replace(")", "_").replace("-", "_").replace("+", "_").replace("=", "_").replace(":", "_").replace(";", "_").replace('"""', "_").replace("'", "_").replace(",", "_").replace("<", "_").replace(">", "_")
            file6 = drive.CreateFile({
                'title':vfname,
                'parents': [{'id': videofolder}]
            })
            # file6.SetContentFile(path)
            # file6.Upload()

        print('successfully')
    
    #insert YouTubers_Name ,Video_Link ,Video_Likes , Number_Of_Comments ,Title_Of_Video ,Thumbnail_Of_Video_Link and Video_watch_url to mysql database
    def mysql(mqldata1,thumbnails,url_video):
        for i in mqldata1:
            
            sqlq1 = "INSERT INTO YouTubers_Table(YouTubers_Name ,Video_Link ,Video_Likes , Number_Of_Comments ,Title_Of_Video ,Thumbnail_Of_Video_Link,Video_watch_url) values (%s,%s,%s,%s,%s,%s,%s)"
            val = (video_author, video_link1, i[1], i[2], i[0], thumbnails, url_video)

            cursor.execute(sqlq1, val)
            conn.commit()
        
    print(final_url)
    t1 = threading.Thread(target=mongo,args=(thumbnails,title,mqldata1))
    t2 = threading.Thread(target=mysql,args=(mqldata1,thumbnails,url_video))
    # t3 = threading.Thread(target=video1,args=(final_url,))

    t1.start()
    # t3.start()
    t2.start()

    t1.join()
    # t3.join()
    t2.join()

#delete from google drive data
def gdive_delete():
    videofolder = '1qDl8vUE3qy0yBhxTIz1ztfNQ3KDsWVB4'
    folder = "\'" + videofolder + "\'" + " in parents and trashed=false" 
    file_list = drive.ListFile({'q': folder}).GetList()
    for file1 in file_list:
        file = drive.CreateFile({'id':file1['id']})
        file.Delete()


# main function
def get_all_video_url(video_url,videounum):

    try:
        print(videounum)
        t=time.time()
        # print(video_url)
        
        # print('ok')
        #delete table of mongo for new table 
        db = client['YouTube_Video_Data']
        col = db['YouTubers_table']
        col.drop()


        #id from flask app
        c = Channel(video_url)

        count = 0

        #function for delete all video in google drive
        gdive_delete()
        for r in c:

            #delete all images from local folder after upload in mongo
            dir = r"./media/images"
            all_files = os.listdir(dir)
            for f in all_files:
                path = os.path.join(dir, f)
                os.remove(path)

            #delete all images from local folder after upload in google drive
            dir = r"./media/video"
            all_files = os.listdir(dir)
            for f in all_files:
                path = os.path.join(dir, f)
                os.remove(path)

            #chanel all videos link
            final_url = str(r)
            #extract video id from channel video link
            url_video = str(r)[-11:]

            # function for extract video data
            data = video_data(url_video, final_url)

            #cont for one by one video data extract
            if count == int(videounum)-1:
                break

            count += 1

            print('completed')
        
        #for chrck the time for video rxtract
        dura = time.time()-t
        print('done : ',time.strftime("%H:%M:%S", time.gmtime(dura)))

            # return data
    except Exception as e:
        pass
        print(e)

# get_all_video_url('https://www.youtube.com/c/HiteshChoudharydotcom/videos',1)