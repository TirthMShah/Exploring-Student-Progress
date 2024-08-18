import numpy as np
import matplotlib.pyplot as plt
import psycopg2

def connection(): # For connection
    conn=psycopg2.connect(host="localhost",port="5432",user="postgres",password="tirth",database="ESP")
    cur=conn.cursor()
    return conn,cur

def details_of_students(): # To fetch Student Data
    while True:
        try:
            num_of_stu=int(input("\nEnter the number of Student you want to add:"))
            break
        except:
            print("Enter The Valid Number")
    detail={}
    while len(detail)!=num_of_stu:
        conn,cur=connection()
        names=input("Enter the name of student:")
        names=names.upper()
        cur.execute(f"SELECT python,fsd,ps,de FROM student_data where student_name='{names}';")    
        data=cur.fetchall()
        try:
            marks=[data[0][0],data[0][1],data[0][2],data[0][3]]
            if num_of_stu==1:
                bar_graph_ind(names)
                return
        except Exception as e:
            print("\nNo student of this name.\nPlease verify the Name of the Student")
            print("Re-enter the name of the Student")
            continue
        detail[names]=marks
        conn.close()
    bar_graph(detail)

def bar_graph_ind(names): # For individual bar graph of student of all semester
    conn,cur=connection()
    cur.execute(f"SELECT python,fsd,ps,de FROM student_data where student_name='{names}';")    
    data_sem3=cur.fetchall()
    cur.execute(f"SELECT ds_total,dbms_total,java_total,maths_total,fee_total FROM student_sem2 where student_name='{names}';")  
    data_sem2=cur.fetchall()
    cur.execute(f"SELECT maths,physics,java,se,iot,com_workshop FROM student_sem1 where student_name='{names}';")  
    data_sem1=cur.fetchall()
    conn.close()
    mark_3=[data_sem3[0][0],data_sem3[0][1],data_sem3[0][2],data_sem3[0][3]]
    mark_2=[data_sem2[0][0],data_sem2[0][1],data_sem2[0][2],data_sem2[0][3],data_sem2[0][4]]
    mark_1=[data_sem1[0][0],data_sem1[0][1],data_sem1[0][2],data_sem1[0][3],data_sem1[0][4],data_sem1[0][5]]

    x3=["PYTHON","FSD","PS","DE"]
    x2=["DS","DBMS","JAVA","MATHS-II","FEE"]
    x1=["MATHS-I","PHYSICS","JAVA","SE","IOT","CW"]
    index3 = np.arange(len(x3))
    index2 = np.arange(len(x2))
    index1 = np.arange(len(x1))

    plt.subplot(1,3,1)
    plt.bar(index3,mark_3,label=names)
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title('Scores by Student in Sem-3')
    plt.xticks(index3,x3)

    plt.subplot(1,3,2)
    plt.bar(index2,mark_2,label=names)
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title('Scores by Student in Sem-2')
    plt.xticks(index2,x2)
    
    plt.subplot(1,3,3)
    plt.bar(index1,mark_1,label=names)
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title('Scores by Student in Sem-1')
    plt.xticks(index1,x1)


    plt.suptitle("Student Marks")
    plt.show()

def bar_graph(detail):   # For bar graph
    fig, ax = plt.subplots(figsize=(5,4)) 
    x=["PYTHON","FSD","PS","DE"]
    index = np.arange(len(x))
    bar_width = 0.15

    for i,name in enumerate(detail.keys()):
        plt.bar(index + i * bar_width, detail[name], bar_width, label=name)
    
    for i, name in enumerate(detail.keys()):
        for j, value in enumerate(detail[name]):
            plt.text(index[j] + i * bar_width, value + 1, str(value), ha='center', va='bottom')

    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title('Scores by Student and Subject')
    plt.xticks(index + 1.5 * bar_width, x)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1))
    plt.show()

def bar_graph_stu(detail,subject): # For individual subjects FSD/PYTHON
    x=[subject.upper()]
    index = np.arange(len(x))
    bar_width = 0.15
    for i,name in enumerate(detail.keys()):
        plt.bar(index + i * bar_width,detail[name], bar_width, label=name)
    
    for i, name in enumerate(detail.keys()):
        for j, value in enumerate(detail[name]):
            plt.text(index[j] + i * bar_width, value + 1, str(value), ha='center', va='bottom')

    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title('Scores by Student and Subject')
    plt.xticks(index + 1.5 * bar_width, x)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1))
    plt.show()

def valid_num_of_stu(num):  # Valided number of student
    if num<=0:
        return False 
    return True

def check_branch(branch):  # To valided branch
    conn,cur=connection()
    cur.execute(f"SELECT branch from student_data")
    data=cur.fetchall()
    conn.close()
    for i in data:
        if branch in i:
            return True
    else:
        return False

def top_branch(name,num):  # To fetch Branch Data
    conn,cur=connection()
    num=str(num)
    cur.execute(f"SELECT python,fsd,ps,de,student_name from student_data where branch='{name}' LIMIT '{num}'")
    data=cur.fetchall()
    conn.commit()
    conn.close()
    details={}
    for i in data:
        marks=[i[0],i[1],i[2],i[3]]
        details[i[4]]=marks
    bar_graph(details)
 
def select_branch():  # To select Branch 
    print("1.CE.\n2.CSE\n3.IT\n4.Other\n5.Exit")
    choice=valid_input()

    if choice==1:
        num_stu=select_student()
        while not valid_num_of_stu(num_stu):
            print("Enter Valid Number of Students")
            num_stu=select_student()
        top_branch("CE",num_stu)
        select_branch()
    
    elif choice==2:
        num_stu=select_student()
        if not valid_num_of_stu(num_stu):
            print("Enter Valid Number of Students")
            return
        top_branch("CSE",num_stu)
        select_branch()

    elif choice==3:
        num_stu=select_student()
        if not valid_num_of_stu(num_stu):
            print("Enter Valid Number of Students")
            return
        top_branch("IT",num_stu)
        select_branch()

    elif choice==4:
        while True:
            branch=input("Enter Branch of your Choice:")
            if check_branch(branch.upper()):
                num_stu=select_student()       
                if not valid_num_of_stu(num_stu):
                    print("Enter Valid Number of Students")
                    return
                else:
                    top_branch(branch.upper(),num_stu)
                    break
            else:
                print("Enter Valid Type of Branch")
    elif choice==5:
        print("Exited")
    else:
        print("Enter The Valid Choice")
        select_branch()

def top_depart(name,num): #To fetch Deptartment Data
    conn,cur=connection()
    num=str(num)
    cur.execute(f"SELECT python,fsd,ps,de,student_name from student_data where department='{name}' LIMIT '{num}'")
    data=cur.fetchall()
    conn.commit()
    conn.close()
    d={}
    for i in data:
        marks=[i[0],i[1],i[2],i[3]]
        d[i[4]]=marks
    bar_graph(d)

def select_depart(): # To select Branch 
    print("1.CE/IT-1.\n2.CE/IT-2\n3.CE/IT-3\n4.Exit")
    choice=valid_input()

    if choice==1:
        num_stu=select_student()
        if not valid_num_of_stu(num_stu):
            print("Enter Valid Number of Students")
            return
        top_depart("CE/IT-1",num_stu)
        select_depart()

    elif choice==2:
        num_stu=select_student()
        if not valid_num_of_stu(num_stu):
            print("Enter Valid Number of Students")
            return
        top_depart("CE/IT-2",num_stu)
        select_depart()

    elif choice==3:
        num_stu=select_student()
        if not valid_num_of_stu(num_stu):
            print("Enter Valid Number of Students")
            return
        top_depart("CE/IT-3",num_stu)
        select_depart()

    elif choice==4:
        print("Exited\n")
        return
    else:
        print("Enter The Valid Choice")
        select_depart()

def select_student(): # To select Number of Student 
    print("\nSelect Number Of Student")
    print("1.3.\n2.5\n3.7\n4.Other")
    choice=valid_input()
    if choice==1:
        return 3
    elif choice==2:
        return 5
    elif choice==3:
        return 7
    elif choice==4:
        choice=valid_input()
        return choice
    else:
        print("Enter The Valid Choice")
        select_student()

def top_subject(subject): # To fetch per subject data 
    num_stu=select_student()
    if not valid_num_of_stu(num_stu):
        print("Enter Valid Number of Students")
        return
    conn,cur=connection()
    num_stu=str(num_stu)
    data=""

    if subject=="python":
        cur.execute(f"SELECT python,student_name from student_data order by python desc LIMIT '{num_stu}'")
        data=cur.fetchall()
    elif subject=="Fsd":
        cur.execute(f"SELECT fsd,student_name from student_data order by fsd desc LIMIT '{num_stu}'")
        data=cur.fetchall()

    conn.commit()
    conn.close()
    detail={}
    for i in data:
        marks=[i[0]]
        detail[i[1]]=marks
    bar_graph_stu(detail,subject)

def valid_input(): # To valided user input
    while True:
        try:
            choice=int(input("Enter Your Choice:"))
            break
        except:
            print("\nEnter Valid Input\n")
    return choice

def via_SPI(): # To fetch marks and calculate SPI
    sem_1=[6,4,6,4,2,2]
    sem_2=[6,6,6,6,3]
    sem_3=[5,6,5,5]
    while True:
        try:
            num_of_stu=int(input("\nEnter the number of Student you want to add:"))
            break
        except:
            print("Enter The Valid Number")
    detail={}
    while len(detail)!=num_of_stu:
        conn,cur=connection()
        names=input("Enter the name of student:")
        names=names.upper()
        cur.execute(f"SELECT python,fsd,ps,de FROM student_data where student_name='{names}';")  
        data_sem3=cur.fetchall()
        cur.execute(f"SELECT ds_total,dbms_total,java_total,maths_total,fee_total FROM student_sem2 where student_name='{names}';")  
        data_sem2=cur.fetchall()
        cur.execute(f"SELECT maths,physics,java,se,iot,com_workshop FROM student_sem1 where student_name='{names}';")  
        data_sem1=cur.fetchall()
        try:
            spi3=(data_sem3[0][0]*sem_3[0]+data_sem3[0][1]*sem_3[1]+data_sem3[0][2]*sem_3[2]+data_sem3[0][3]*sem_3[3])/(sum(sem_3)*10)
            spi2=(data_sem2[0][0]*sem_2[0]+data_sem2[0][1]*sem_2[1]+data_sem2[0][2]*sem_2[2]+data_sem2[0][3]*sem_2[3]+data_sem2[0][4]*sem_2[4])/(sum(sem_2)*10)
            spi1=(data_sem1[0][0]*sem_1[0]+data_sem1[0][1]*sem_1[1]+data_sem1[0][2]*sem_1[2]+data_sem1[0][3]*sem_1[3]+data_sem1[0][4]*sem_1[4]+data_sem1[0][5]*sem_1[5])/(sum(sem_1)*10)
            SPI=[spi1,spi2,spi3]
        except:
            print("\nNo student of this name.\nPlease verify the Name of the Student")
            print("Re-enter the name of the Student")
            continue
        detail[names]=SPI
        conn.close()
    line_graph(detail)

def line_graph(details): # To show Line Graph
    x=np.array([1,2,3])
    for student, spi_values in details.items():
        plt.plot(x, spi_values, marker='o',label=student)
    plt.xlabel("SPI")
    plt.xticks(x)
    plt.ylabel("Semester")
    plt.grid(True)
    plt.legend()
    plt.show()

def search(): # To Select Type
    print("1.Search within the Students.\n2.Top Students of Departments\n3.Top Students of Branch\n4.Top Students of Python\n5.Top Students of FSD\n6.Compare Student via SPI\n7.Exit")
    choice=valid_input()
    if choice==1:
        details_of_students()
        search()
    elif choice==2:
        select_depart()
        search()
    elif choice==3:
        select_branch()
        search()
    elif choice==4:
        top_subject("python")
        search()
    elif choice==5:
        top_subject("Fsd")
        search()
    elif choice==6:
        via_SPI()
        search()
    elif choice==7:
        print("Thank You!")
        return
    elif choice>6 and choice<1:
        print("Enter The valid choice")
        search()

def Main(): #Main Method
    search()
Main()