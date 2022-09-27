import mysql.connector as mysql 

db = mysql.connect(host = "localhost", user = "root", password = "", database="school")  #password is blank by default _ database= <nameofyours> 
command_handler = db.cursor(buffered=True)  #for work with sql queries 

def student_session(username):
    while 1:
        print('1. View status'); print('2. Logout')
        
        user_option = input(str('Option : '))
        
        if user_option == '1':
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == '2':
            break 
        else:
            print("Please type a valid option.")

def teacher_session():
    while 1:
        print(''); print('Admin Menu'); print('')
        print('1. Mark student register'); print('2. View students'); print('3. Log out')
        
        user_option = input(str('Option : '))
        if user_option == '1':
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student' ")
            records = command_handler.fetchall()
            date = input(str('Date : DD/MM/YYYY : '))
            for record in records:
                record= str(record).replace("'", "")
                record= str(record).replace(",", "")
                record= str(record).replace("(", "")
                record= str(record).replace(")", "")
                #Present | Absent | Late
                status = input(str("Status for " + str(record) + " P|A|L : "))
                query_values = (str(record),date,status)
                command_handler.execute("INSERT INTO  attendance (username, date, status) VALUES(%s,%s,%s)", query_values)
                db.commit()  # saving the changes
                print(record + " Marked as " + status)
        elif user_option == '2':
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == '3':
            break 
        else:
            print("Please type a valid option.")
                   
        
def admin_session():
    while 1:
        print(''); print('Admin Menu'); print('')
        print('1. Register new Student'); print('2, Register new teacher'); print('3. Delete Student')
        print('4. Delete teacher'); print('5. Logout')
        
        user_option = input(str('Option : '))
        
        if user_option == '1':
            username = input(str('username : '))
            password = input(str('password : '))
            query_values = (username, password)
            command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s,%s,'student')", query_values)
            db.commit()  # saving the changes
            print(username+' has been registered as a student successfully.')
            
        elif user_option == '2':
            username = input(str('username : '))
            password = input(str('password : '))
            query_values = (username, password)
            command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s,%s,'teacher')", query_values)
            db.commit()  # saving the changes
            print(username+' has been registered as a teacher successfully.')
            
        elif user_option == '3':
            username = input(str('username : '))
            query_values = (username, 'student')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_values)
            db.commit()  # saving the changes
            if command_handler.rowcount < 1:
                print('Student not found')
            else:
                print(username+' has been deleted as a student successfully.')
                
        elif user_option == '4':
            username = input(str('username : '))
            query_values = (username, 'teacher')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_values)
            db.commit()  # saving the changes
            if command_handler.rowcount < 1:
                print('Teacher not found')
            else:
                print(username+' has been deleted as a teacher successfully.')
        
        elif user_option == '5':
            break
        else:
            print('Please type a valid option.')
            
def auth_student():
    username = input(str('username : ')) 
    password = input(str('password : '))
    query_values = (username, password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = 'student'", query_values)
    if command_handler.rowcount <= 0:
        print("Login failed")
    else:
        student_session(username)
            
def auth_teacher():
    username = input(str('username : '))          
    password = input(str('password : '))  
    query_values = (username, password)       
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher' ", query_values)
    if command_handler.rowcount <= 0:
        print('Login failed')
    else:
        teacher_session()
    

def auth_admin():
    print('')
    print('Admin Login')
    print('')
    username = input(str('Username : '))
    password = input(str('Password : '))
    if username == 'admin':
        if password == 'pass':
            admin_session()
        else:
            print('incorrect password')
    else:
        print('incorrect username')
    
def main():
    while 1:
        print('Welcome to the school system.')
        print('-----------------------------')
        print('1. Login as student');print('2. Login as teaacher');print('3. Login as admin')
        
        user_option = input(str("Option : "))
        
        if user_option == '1':
            auth_student()
        elif user_option == '2':
            auth_teacher()
        elif user_option == '3':
            auth_admin()
        else:
            print('Please type a valid option.')
            
main()   