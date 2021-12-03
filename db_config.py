import sqlite3
import json
con = sqlite3.connect('database.db')

cur = con.cursor()

jsonstring = '''{"username": "use3r7", "email": "hell3o@hello.com", "uploadedPic": "profpic2.png", "headline": "headlinejeheadline","aboutme": "aboutme je aboutme", "fullName": "asdfgrw"}'''
jsonLoad = json.loads(jsonstring)
print(jsonLoad['email'])
query = "INSERT INTO user (username, email, profilepic, headline, aboutme, fullname) VALUES ('{}','{}','{}','{}','{}','{}')".format(
    jsonLoad['username'], jsonLoad['email'], jsonLoad['uploadedPic'], jsonLoad['headline'], jsonLoad['aboutme'],
    jsonLoad['fullName'])

cur.execute(query)
con.commit()