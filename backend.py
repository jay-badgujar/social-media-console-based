import mysql.connector
from datetime import datetime
import ctypes
# Define color codes
STD_OUTPUT_HANDLE = -11
FOREGROUND_RED = 0x0004
FOREGROUND_GREEN = 0x0002
FOREGROUND_BLUE = 0x0001
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
FOREGROUND_WHITE = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE

def set_text_color(color):
    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE), color)

def print_colorful_message(message, color):
    set_text_color(color)
    print(message)
    set_text_color(FOREGROUND_WHITE)


class Instagram:
    def __init__(self,authuser,authid):
        self.con = mysql.connector.connect(host="localhost", user="root", password="", database="socialmedia")
        self.mycursor = self.con.cursor()

    def authenticateuser(self,email,password):
        query="SELECT id,name FROM usertable WHERE email = (%s) AND password = (%s)"
        val = (email,password)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchone()
        if(rs == None):
            print("Invalid Credentials")
            return 0
        else:
            self.authid = rs[0]
            self.authuser = rs[1]
            print("User Authenticated Successfully")

            query="SELECT lastlogindate FROM lastlogin WHERE userid = (%s)"
            val = (self.authid,)
            self.mycursor.execute(query,val)
            rs = self.mycursor.fetchone()

            current_date = datetime.now()
            formatted_date = current_date.strftime("%d-%m-%Y")

            if(rs == None):
                print("First Time Login")
                query="INSERT INTO lastlogin(lastlogindate) VALUES(%s)"
                val=(formatted_date,)
                self.mycursor.execute(query,val)
            else:
                print(f"Last Login On - {rs[0]}")
                query="UPDATE lastlogin SET lastlogindate=%s WHERE userid=%s"
                val=(formatted_date,self.authid)
                self.mycursor.execute(query,val)
            self.con.commit()
            return (self.authid,self.authuser)
        
    def createnewuser(self,name,email,password):
        query="INSERT INTO usertable(name,email,password) VALUES(%s,%s,%s)"
        val=(name,email,password)
        self.mycursor.execute(query,val)
        self.con.commit()
        query="SELECT id FROM usertable WHERE name = (%s) AND email = (%s) AND password = (%s)"
        val = (name,email,password)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchone()
        return rs[0]

    def seeallposts(self):
        query="SELECT createdby,id,content FROM posts"
        self.mycursor.execute(query)
        rs = self.mycursor.fetchall()
        for i in rs:
            print_colorful_message(f'Post Id - {i[1]}  |  Created by - {i[0]}\n',FOREGROUND_YELLOW)
            print_colorful_message(f"content - {i[2]}",FOREGROUND_YELLOW)
            print_colorful_message("-------------------------------------------------",FOREGROUND_YELLOW)
    
    def seeparticularpost(self,postId):
        query="SELECT createdby,createdbyid,content,likes,comments FROM posts WHERE id = (%s)"
        val = (postId,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        print_colorful_message("\n-------------------------------------------------",FOREGROUND_BLUE)
        for i in rs:
            print_colorful_message(f'Post Id - {i[1]}  |  Created by - {i[0]}\n',FOREGROUND_BLUE)
            print_colorful_message(f"content - {i[2]}\n",FOREGROUND_BLUE)
            print_colorful_message(f'Likes - {i[3]}  |  Comments - {i[4]}\n',FOREGROUND_BLUE)
            print_colorful_message("-------------------------------------------------",FOREGROUND_BLUE)

    def seecommentsofthepost(self,postId):
        query="SELECT createdby,comment FROM commentsofposts WHERE postid = (%s)"
        val = (postId,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        for i in rs:
            print(f'Comment By - {i[0]}  |  Comment - {i[1]}\n')
            print("-------------------------------------------------")

    def likepost(self,postid):
        query="UPDATE posts SET likes = likes + 1 WHERE id = (%s)"
        val=(postid,)
        self.mycursor.execute(query,val)
        if self.mycursor.rowcount > 0:
            print("Liked Successfully")
        self.con.commit()

    def createComment(self,postid,comment):
        query="INSERT INTO commentsofposts(postid,createdby,createdbyid,comment) VALUES(%s,%s,%s,%s)"
        val=(postid,self.authuser,self.authid,comment)
        self.mycursor.execute(query,val)
        if self.mycursor.rowcount > 0:
            print("Comment created successfully.")
        self.con.commit()

        query="UPDATE posts SET comments = comments + 1 WHERE id = (%s)"
        val=(postid,)
        self.mycursor.execute(query,val)
        self.con.commit()

    def searchUserByName(self,name):
        query="SELECT * FROM usertable WHERE name = (%s)"
        val = (name,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchone()
        if(rs == None):
            return False
        else:
            return True

    def followingSomeone(self,name):
        query="SELECT id FROM usertable WHERE name = (%s)"
        val = (name,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchone()

        toid = rs[0]
        status = "following"

        query="INSERT INTO friendlist(fromid,toid,status) VALUES(%s,%s,%s)"
        val=(self.authid,toid,status)
        self.mycursor.execute(query,val)
        if self.mycursor.rowcount > 0:
            print(f"Now you are following {name}.")
        self.con.commit()

    def getUsers(self):
        query="SELECT * FROM usertable"
        self.mycursor.execute(query)
        rs = self.mycursor.fetchall()
        count = 0
        for i in rs:
            count = count + 1
            print_colorful_message(f"{count}. {i[1]}",FOREGROUND_BLUE)

    def showFollowers(self):
        query="SELECT * FROM friendlist JOIN usertable ON friendlist.fromid = usertable.id WHERE friendlist.toid = (%s)"
        val = (self.authid,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        print("\n")
        for i in rs:
            print_colorful_message(f"name - {i[7]} status - {i[3]}",FOREGROUND_BLUE)
        print("\n")
        return rs
    
    def findUser(self,fromid):
        query="UPDATE friendlist SET status = (%s) WHERE fromid = (%s) AND toid = (%s)"
        val=("friend",fromid,self.authid)
        self.mycursor.execute(query,val)
        self.con.commit()

    def showFollowing(self):
        query="SELECT * FROM friendlist JOIN usertable ON friendlist.fromid = usertable.id WHERE friendlist.toid = (%s)"
        val = (self.authid,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        print("\n")
        for i in rs:
            print_colorful_message(f"name - {i[7]}",FOREGROUND_BLUE)

    def showFriends(self):
        query = "SELECT DISTINCT usertable.name,usertable.id FROM friendlist JOIN usertable ON (friendlist.fromid = usertable.id OR friendlist.toid = usertable.id) WHERE (friendlist.fromid = (%s) OR friendlist.toid = (%s)) AND friendlist.status = (%s) GROUP BY usertable.name HAVING COUNT(*) = 1"
        val = (self.authid,self.authid,"friend")
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        count = 0
        print("\n")
        for i in rs:
            count += 1
            print_colorful_message(f"{count}. {i[0]}",FOREGROUND_BLUE)
        print("\n")
        return rs
    
    def chatwithfriend(self,id):
        query = "SELECT * FROM chats WHERE (cfromid = (%s) AND ctoid = (%s)) OR (cfromid = (%s) AND ctoid = (%s))"
        val = (id,self.authid,self.authid,id)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if(i[1]==self.authid):
                print_colorful_message(f"{' '*20}{i[4].date()}",FOREGROUND_YELLOW)
                print_colorful_message(f"{' '*35}{i[3]}({i[4].time()})",FOREGROUND_GREEN)
            else:
                print_colorful_message(f"{' '*20}{i[4].date()}",FOREGROUND_YELLOW)
                print_colorful_message(f"{i[3]}({i[4].time()})",FOREGROUND_RED)
        
        while(True):
            message = input("Enter Message To Send (exit)- ")
            if(message.lower() == 'Exit'.lower()):
                break
            else:
                query="INSERT INTO chats(cfromid,ctoid,chat) VALUES(%s,%s,%s)"
                val=(self.authid,id,message)
                self.mycursor.execute(query,val)
                self.con.commit()
        
    def createNewPost(self,content):
        query="INSERT INTO posts(createdby,createdbyid,content,likes,comments) VALUES(%s,%s,%s,%s,%s)"
        val=(self.authuser,self.authid,content,0,0)
        self.mycursor.execute(query,val)
        self.con.commit()

    def showMyPosts(self):
        query="SELECT * FROM posts WHERE createdbyid = (%s)"
        val = (self.authid,)
        self.mycursor.execute(query,val)
        rs = self.mycursor.fetchall()
        for i in rs:
            print(f"{i[0]}. - {i[5]}")
        return rs

    def updatePost(self,content,id):
        query="UPDATE posts SET content = (%s) WHERE id = (%s)"
        val=(content,id)
        self.mycursor.execute(query,val)
        self.con.commit()

    def deletePost(self,id):
        query="DELETE FROM posts WHERE id = (%s)"
        val=(id,)
        self.mycursor.execute(query,val)
        self.con.commit()

        query="DELETE FROM commentsofposts WHERE postid = (%s)"
        val=(id,)
        self.mycursor.execute(query,val)
        self.con.commit()