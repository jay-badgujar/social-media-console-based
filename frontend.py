import ctypes
from backend import *

insta = Instagram("",0)

authuser = ""
authid = 0


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



print("\nWelcome to Instagram\n")
while(True):
    print_colorful_message("---------------------------",FOREGROUND_GREEN)
    print_colorful_message("|   Press 1 For Login     |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 2 For SignUp   |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 3 For Exit      |",FOREGROUND_GREEN)
    print_colorful_message("---------------------------",FOREGROUND_GREEN)
    choice = int(input("Your Choice - "))
    if(choice == 1):
        print("\n")
        email = input("Enter Your Email - ")
        password = input("Enter Your Password - ")
        # email = "jay@gmail.com"
        # password = 111
        a = insta.authenticateuser(email,password)
        if(a == 0):
            continue
        else:
            authid = a[0]
            authuser = a[1]
            break
    elif(choice == 2):
        print("Sign Up")
        name = input("Enter Your Name - ")
        email = input("Enter Your E-mail - ")
        password = input("Enter Your Password - ")
        a = insta.createnewuser(name,email,password)
        authid = a
        authuser = name
        break
    elif(choice == 3):
        break
    else:
        print("Please Enter Valid Choice!")

print(f"UserName - {authuser} | User Id - {authid}")

while(True):
    print_colorful_message("\n------------------------------------------",FOREGROUND_GREEN)
    print_colorful_message("|   Press 1 See Posts                    |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 2 Search Friends               |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 3 Show Followers & Following   |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 4 Chat With Friends            |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 5 Create Post                  |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 6 Update My Post               |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 7 Delete My Post               |",FOREGROUND_GREEN)
    print_colorful_message("|   Press 8 Exit                         |",FOREGROUND_GREEN)
    print_colorful_message("------------------------------------------",FOREGROUND_GREEN)
    choice = int(input("Your Choice - "))
    
    if(choice == 1):
        choice = "3"
        while(choice == "3"):
            print("\n\n---------------- All Posts ----------------\n")
            insta.seeallposts()
            postId = input("\n\nSee Particular Post - ")
            insta.seeparticularpost(postId)
            insta.seecommentsofthepost(postId)
            print_colorful_message("-------------------------------",FOREGROUND_GREEN)
            print_colorful_message("|   Press 1 Like The Post     |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 2 Write A Comment   |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 3 <- Back           |",FOREGROUND_GREEN)
            print_colorful_message("-------------------------------",FOREGROUND_GREEN)
            choice = input("Your Choice - ")
            if(choice == "1"):
                insta.likepost(postId)
            elif(choice == "2"):
                comment = input("Write a comment - ")
                insta.createComment(postId,comment)
            elif(choice == "3"):
                break
            else:
                print("Please Enter Valid Choice")

    elif(choice == 2):
        print("\n------------ Search Friends -----------")
        choice = "3"
        while(choice == "3"):
            print_colorful_message("---------------------------------------",FOREGROUND_GREEN)
            print_colorful_message("|   Press 1 For Search User By Name   |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 2 For Show List Of Users    |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 3 For <- Back               |",FOREGROUND_GREEN)
            print_colorful_message("---------------------------------------",FOREGROUND_GREEN)
            choice = input("Your Choice - ")
            if(choice == "1"):
                name = input("Enter User Name - ")
                if(insta.searchUserByName(name)):
                    print("User Found")
                    yorn = input("Like to send a friend request? Yes/No - ")
                    if(yorn == "Yes" or yorn == "yes" or yorn == "Y" or yorn == "y"):
                        insta.followingSomeone(name)
                else:
                    print("User not found")
            elif(choice == "2"):
                insta.getUsers()
                name = input("Enter User Name - ")
                if(insta.searchUserByName(name)):
                    print("User Found")
                    yorn = input("Like to send a friend request? Yes/No - ")
                    if(yorn == "Yes" or yorn == "yes" or yorn == "Y" or yorn == "y"):
                        insta.followingSomeone(name)
                else:
                    print("User not found")
            elif(choice == "3"):
                break
            else:
                print("Please Enter Valid Choice")
        
    elif(choice == 3):
        choice = "4"
        while(choice == "4"):
            print_colorful_message("-------------------------------",FOREGROUND_GREEN)
            print_colorful_message("|   Press 1 Show Followers    |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 2 Show Following    |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 3 Show My Friends   |",FOREGROUND_GREEN)
            print_colorful_message("|   Press 4  <- Back          |",FOREGROUND_GREEN)
            print_colorful_message("-------------------------------",FOREGROUND_GREEN)
            choice = input("Your Choice - ")
            
            if(choice == "1"):
                temp = insta.showFollowers()
                yorn = input("Want to follow back some one (yes/no) - ")
                if(yorn == "Yes" or yorn == "yes" or yorn == "Y" or yorn == "y"):
                        name = input("Enter Follower Name - ")
                        for i in temp:
                            if(i[7].lower()==name.lower()):
                                insta.findUser(i[1])

            elif(choice == "2"):
                insta.showFollowing()
            elif(choice == "3"):
                insta.showFriends()
            elif(choice == "4"):
                break
            else:
                print("Please Enter Valid Choice")
        
    elif(choice == 4):
        temp = insta.showFriends()
        chatpersonname = input("Enter Friend Name To Chat - ")
        print("\n")
        for i in temp:
            if(i[0].lower()==chatpersonname.lower()):
                insta.chatwithfriend(i[1])

    elif(choice == 5):
        print("---------- Create A Post ----------")
        content = input("Write A Content To Post - ")
        insta.createNewPost(content)
        
    elif(choice == 6):
        print("---------- Update A Post ----------")
        temp = insta.showMyPosts()
        postidtoupdate = input("Enter Post Id To Update - ")
        for i in temp:
            if(i[0]==int(postidtoupdate)):
                newcontent = input("Enter New Content - ")
                insta.updatePost(newcontent,i[0])
                break
        else:
            print("Wrong Post Id.")
    elif(choice == 7):
        print("---------- Delete A Post ----------")
        temp = insta.showMyPosts()
        postidtoupdate = input("Enter Post Id To Delete - ")
        for i in temp:
            if(i[0]==int(postidtoupdate)):
                insta.deletePost(i[0])
    
    elif(choice == 8):
        break
    else:
        print("Please Enter Valid Choice!")