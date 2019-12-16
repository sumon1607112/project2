#!/usr/bin/env python
# coding: utf-8

# In[2]:


import speech_recognition as sr
import mysql.connector
import re 
from gtts import gTTS
import os



#database connection

mydb = mysql.connector.connect(
  host="localhost",
  user="rifat",
  passwd="rifat",
  database="hospital",
  auth_plugin='mysql_native_password'
)
  
def validating_name(name): 
    #print(name)
  
    # RegexObject = re.compile( Regular expression, flag ) 
    # Compiles a regular expression pattern into a regular expression object 
    regex_name1 = re.compile(r'(doctor|Doctor|Dr|dr) ([a-z]+)*',  
              re.IGNORECASE) 
    regex_name2 = re.compile(r'([0-9]+)([:]?)([0-9]*) ([a|p|A|P])',  
              re.IGNORECASE)
    regex_name3 = re.compile(r'([0-9]+) (JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|januay|february|march|april|may|june|july|august|september|october|november|december)*',  
              re.IGNORECASE)
    # RegexObject is matched wi                                 th the desired  
    # string using search function 
    # In case a match is found, search() returns 
    # MatchObject Instance 
    # If match is not found, it return None 
    res1 = regex_name1.findall(name) 
    res2 = regex_name2.findall(name)
    res3 = regex_name3.findall(name)
    print(res1)
    print(res2)
    print(res3)
    lis1=[]
    lis2=[]
    lis3=[]
    # If match is found, the string is valid 
    if res1:
        lis1.append(res1)
        #print(lis)
        print(lis1[0][0][1])
        n=lis1[0][0][1]
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * from doctorlist WHERE name = '%s'" % (n))
        myresult = mycursor.fetchall()
        #print(myresult)
        #print(myresult[0][0])
        doctor_id=myresult[0][0]
        
        
        #print(myresult[0][2])
        doctor_stime=myresult[0][2]
        #print(myresult[0][3])
        doctor_etime=myresult[0][3]
        #print(myresult[0][4])
        doctor_limit=myresult[0][4]
        
        
                        
        mydb.commit()
        
    
    
    if res2:
        lis2.append(res2)
        #print(lis)
        #print(lis2[0][0][0])
        #print(lis2[0][0][3])
        user_time=int(lis2[0][0][0])
        user_a_p=lis2[0][0][3]
        #user_time=int(user_time)
        print (user_a_p)
        if user_a_p =="p":
            user_time=user_time+12
            print(user_time)

    
    if res3:
        lis3.append(res3)
        #print(lis)
        #print(lis3[0][1][1])
        user_date=lis3[0][1][0]
        #print(lis3[0][1][0])
        user_month=lis3[0][1][1]
      
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * from patien_list WHERE d_id = '%s'" % (doctor_id))
    myresult = mycursor.fetchall()
    print(myresult)
    var=int(len(myresult))
    print(var)
    if var==0:
        print("0k1")
        u_limit=int(int(doctor_limit)-1)
        sql = "INSERT INTO patien_list (d_id,date,month,slot) VALUES (%s,%s,%s,%s)"
        
        value = (doctor_id,user_date,user_month,u_limit)

        mycursor.execute(sql, value)
        
        print(mycursor.rowcount, "record inserted.")
        
    else:
      mycursor.execute("SELECT * from patien_list WHERE date = '%s' AND month='%s' AND d_id='%s' " % (user_date,user_month,doctor_id))
      myresult = mycursor.fetchall()
      print("iin")
      print(myresult)
      
      var2=int(len(myresult))
      print(var2)
       
      if var2==0:
          lim=int(0)
      else:
        lim=myresult[0][4]
      
      
      if  var2!=0 and lim>0:
        print("ok2")
        lim=lim-1
        mycursor.execute ("UPDATE patien_list SET slot=%s WHERE d_id='%s'  AND date='%s' AND month='%s' " % (lim,doctor_id,user_date,user_month))
        #mycursor.execute(sql, value)   
        print(mycursor.rowcount, "record updated.")        
      else:
        print("fucked up")
        u_limit=int(int(doctor_limit)-1)
        sql = "INSERT INTO patien_list (d_id,date,month,slot) VALUES (%s,%s,%s,%s)"
        
        value = (doctor_id,user_date,user_month,u_limit)

        mycursor.execute(sql, value)
        
        print(mycursor.rowcount, "record inserted.")
        
        
                        
    mydb.commit()    


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak Anything :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        file = open("newfile.txt", "w+")
        file.write(text)
        file.close()
        print("You said : {}".format(text))
        
        file=open("newfile.txt","r+")
        content=file.read()
        validating_name(content)
        
    except:
        #print("Sorry could not recognize what you said")
        myText = "Firoz abbu abbu abbu abbu abbu abbu"

        language = 'en'

        output = gTTS(text=myText, lang=language, slow=False)

        output.save("output.mp3")

        os.system("start output.mp3")

