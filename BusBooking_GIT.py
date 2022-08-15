#!/usr/bin/env python
# coding: utf-8

# In[1]:


def dbconnect(h, u, p):
    import mysql.connector as ms
    try:
        con = ms.connect(host=h, user=u, passwd=p)
        print("Connected")
        return con
    except:
        print("Connection failed..")
        return False


# In[2]:


def init(dbname, conn):
    cur = conn.cursor()
    cur.execute("show databases;")
    result = cur.fetchall()
    for row in result:
        if row[0] == dbname:
            print("database found")
            cur.execute('use {}'.format(dbname))
            cur.close()
            break
    else:
        print('Database not found')
        print("Creating database and tables:")
        sql = 'create database {}'.format(dbname)
        cur.execute(sql)
        sql = 'use {}'.format(dbname)
        cur.execute(sql)
        sql = 'create table buses(bus_id INT PRIMARY KEY AUTO_INCREMENT, b_from varchar(30),b_to varchar(30),s_time time,j_time time,a_time time,fare int)'
        cur.execute(sql)
        sql = 'create table users(user_id INT PRIMARY KEY AUTO_INCREMENT,name varchar(30),email varchar(30) UNIQUE,password varchar(30))'
        cur.execute(sql)
        sql = 'insert into users values(1,"admin","admin","admin")'
        cur.execute(sql)
        sql = 'create table bookings(book_id INT PRIMARY KEY AUTO_INCREMENT,u_id int,bus_id int,j_date date,seat int)'
        cur.execute(sql)
        sql = 'create table stats(bus_id int,j_date date,avl int)'
        cur.execute(sql)
        print("Database created sucessfully..")
        cur.close()


# In[3]:


def signin(conn):
    print("\nLogin to your account...")
    cur = conn.cursor()
    email = input("Enter Email :")
    passwd = input("Enter password : ")
    sql = 'select * from users where email="{}" and password = "{}"'.format(email,passwd)
    cur.execute(sql)
    res = cur.fetchone()
    n = cur.rowcount
    if n==-1:
        cur.close()
        print("!!!!Email or password wrong!!!!")
        return 0,0
    else:
        print("Login Sucessfull")
        uid, uname = res[0], res[1]
        print("welcome")
        cur.close()
        return uid, uname
        
        
    


# In[4]:


def register(conn):
    cur = conn.cursor()
    name = input("Enter Name : ")
    email = input("Enter Email :")
    passwd = input("Enter password : ")
    sql = 'insert into users(name , email , password) values ("{}","{}","{}")'.format(name, email , passwd)
    try:
        cur.execute(sql)
        print("User registration sucessfull")
        cur.close()
        return True
    except:
        cur.close()
        print("EOOR while creating.email already exists")
        return False
    


# In[5]:


def admin(conn):
    menu = """
    1.view Booking for a Bus
    2.Create a new Bus route
    3.Delete a bus route
    4.View bookings for a date
    5.view bus routes
    6.sign out
    """
    while True:
        print(menu)
        ch = int(input("Enter your choice:"))
        if ch==1:
            cur = conn.cursor()
            b_id=int(input('Enter bus id :'))
            sql = 'select u.u_id, name, email, bus_id, j_date, seat from bookings b, users u where b.u_id = u.u_id and b.bus_id={}'.format(b_id)
            cur.execute(sql)
            res = cur.fetchall()
            print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format('UID','passenger Name','email','BUSID','Date','seat'))
            if len(res)==0:
                print("No Bookings Found...")
            else:
                for row in res:
                    print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format(row[0], row[1], row[2], row[3], str(row[4]), row[5]))
            cur.close()
            pass
        elif ch==2:
            cur = conn.cursor()
            From_bus = input('From :')
            to_bus = input('To :')
            s = input("start Time (hh:mm) :")
            j = input("Journey Time (hh:mm) :")
            a = input("ArrivalTime(hh:mm) :")
            fare = int(input("Enter fare :"))
            sql = 'insert into buses(b_from, b_to, s_time, j_time, a_time, fare) values("{}","{}","{}","{}","{}",{})'.format(From_bus, to_bus, s, j, a, fare)
            cur.execute(sql)
            print("Route Added")
            cur.close()
            pass
        elif ch==3:
            cur= conn.cursor()
            b_id = int(input('Enter bus id :'))
            sql = 'delete from buses where bus_id={}'.format(b_id)
            cur.execute(sql)
            print("Route Delete")
            cur.close()
        elif ch==4:
            cur = conn.cursor()
            j_date=input('Enter Date (YYYY-MM-DD) :')
            sql = 'select u.u_id name, email, bus_id,j_date, seat from bookings b, users u where b.u_id = u.u_id and b.J_date={}'.format(d)
            cur.execute(sql)
            res = cur.fetchall()
            print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format('UID','passenger Name','email','BUSID','Date','seat'))
            if len(res)==0:
                print("No Bookings Found...")
            else:
                for row in res:
                    print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
            cur.close()
            pass
        elif ch==5:
            cur = conn.cursor()
            sql = 'select * from buses'
            cur.execute(sql)
            res = cur.fetchall()
            print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format('BID','From','TO','Start Time','Journey Time','Arrival Time','Fare'))
            if len(res)==0:
                print("No Bookings Found...")
            else:
                for row in res:
                    print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format(row[0], row[1], row[2], str(row[3]), str(row[4]), str(row[5]),row[6]))
            cur.close()
        elif ch==6:
            print("\nSigned out..")
            break
        else:
            print("Invalid Option")
    
    


# In[6]:


def user(uid,uname,conn):
    menu = '''
    
    1.Book a Ticket
    2.View Your Bookings
    3.Cancle your ticket
    4.sign out
    '''
    
    while True:
        print(menu)
        ch = int(input("Enter your choice"))
        if ch == 1:
            cur = conn.cursor()
            f = input("From :")
            t = input("To :")
            sql = 'select * from buses where b_from="{}" and b_to="{}"'.format(f,t)
            cur.execute(sql)
            res = cur.fetchall()
            if cur.rowcount==0:
                print("Sorry No buses Found On this Route")
            else:
                d = input("Date (YYYY-MM-DD) :")
                print("BUSES FOUND:")
                res = cur.fetchall()
                print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format('BID','From','TO','Start Time','Journey Time','Arrival Time','Fare'))
                for row in res:
                    print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format(row[0], row[1], row[2], str(row[3]), str(row[4]), str(row[5]),row[6]))
            u_b_id = int(input("Enter bus id to book ticket : "))
            sql = 'select * from stats where bus_id={} and j_date="{}"'.format(u_b_id, d)
            cur.execute(sql)
            res = cur.fetchone()
            if cur.rowcount==-1:
                input("Press enter to pay the fare...")
                sql = 'insert into bookings(u_id, bus_id, j_date, seat) values({},{},"{}",1)'.format(uid, u_b_id, d)
                cur.execute(sql)
                sql = 'insert into stats values({},"{}",39)'.format(u_b_id, d)
                cur.execute(sql)
                print("Ticket Booked.Seat No is 1, Go to Bookings for Details.")
            else:
                if res[2]==0:
                    print("Sorry! BUS FULL...")
                else:
                    seat = 40-res[2]+1
                    sql = 'insert into bookings(u_id, bus_id, j_date, seat) values({},{},"{}",{})'.format(uid, u_b_id, d, seat)
                    cur.execute(sql)
                    sql = 'update stats set avl=avl-1 where bus_id={} and j_date="{}"'.format(u_b_id, d)
                    cur.execute(sql)
                    print("Ticket Booked. seat Number is ",seat,"Go to bookings for more details")
            cur.close()
        elif ch==2:
            pass
        elif ch == 3:
            pass
        elif ch == 4:
                print("\nSign out...")
                break
        else:
            print("Invalid Option")


# In[7]:


def main():
    h= input("Enter host name:")
    u = input("Enter username:")
    p = input("Enter Password:")
    if h=='':
        h='localhost'
    if u== '':
        u= 'root'
    conn = dbconnect(h,u,p)
    db = input("Enter the database name:")
    if db== '':
        db= 'busbook'
    init(db,conn)
    
    menu = """
    1.Sign in
    2.Register
    3.Exit
    """
    uid=0
    print(menu)
    ch = int(input("Enter your choice :"))
    if ch==1:
        uid,uname = signin(conn)
    elif ch==2:
        if register(conn):
            uid,uname = signin(conn)
        else:
            pass
    elif ch==3:
        print("Exiting...")
        pass
    else:
        print("Invalid Option")
    
    if uid == 1:
        admin(conn)
    elif uid==0:
        pass
    else:
        user(uid, uname, conn)
    
    #commit to the database
    conn.commit()
    conn.close()

