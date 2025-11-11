import streamlit as st
import mysql.connector
import pandas as pd

mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kolade789@#$",
    database="day12k"
)

mycursor = mydatabase.cursor()

def register():
    st.subheader("Register New Student")
    reg_no = st.number_input("Enter Registration Number:", min_value=0)
    full_name = st.text_input("Enter Full Name:")
    gender = st.text_input("Select Gender:",["Male", "Female"])
    state = st.text_input("Enter State of Origin:")
    email = st.text_input("Enter Email Address:")

    if st.button("Register"):
        if reg_no and full_name and gender and state and email:
            query = "INSERT INTO informations(reg_no, full_name, gender, state, email) VALUES (%s, %s, %s, %s, %s)"
            values = (reg_no, full_name, gender, state, email)
            mycursor.execute(query, values)
            mydatabase.commit()
            st.success("Information successfully uploaded!")
        else:
            st.error("Please fill in all the fields before submitting.")
def search():
    st.subheader("Search Student Record")

    reg_no = st.number_input("Enter registration number to search:", min_value=0)

    result = []

    if st.button("Search"):
        query = "SELECT * FROM informations where reg_no = %s"
        mycursor.execute(query, (reg_no,))
        result = mycursor.fetchall()

        if len(result) ==0:
            st.warning("Record not fund.")
    else:
        df = pd.DataFrame(result, columns=["Reg_no","Full Name", "Gender", "State", "Email" ])
        st.table(df)

def update():
    st.subheader("Update Student Record")
    reg_no = st.number_input("Enter Registration number:", min_value=0)
    full_name = st.text_input("Enter Full Name:")
    gender = st.text_input("Enter Gender:", ["Male", "Female"])
    state = st.text_input("Enter state of Origin")
    email = st.text_input("Enter Email Address")

    if st.button("update"):
        query = """
        UPDATE informations
        SET full_name = %s, gender = %s, state = %s, email = %s
        WHERE reg_no = %s

        """
        values = ( full_name, gender, state, email, reg_no)
        mycursor.execute(query, values)
        mydatabase.commit()
        st.success("Record updated successfully")

def delete():
    st.subheader("Delete Student Record")
    reg_no = st.number_input("Enter Registration number delete:", min_value=0)
    if st.button("delete"):
        query = "DELETE FROM informations WHERE reg_no = %search"
        mycursor.execute(query, (reg_no),)
        mydatabase.commit()
        st.success("Record deleted successfully")

def display():
    st.subheader("All Registered students")
    query = "SELECT * FROM informations"
    mycursor.execute(query)
    result = mycursor.fetchall()
    if result:
        df = pd.DataFrame(result, columns=["reg.no","full name", "gender", "state", "email"] )
        st.dataframe(df)
    else:
        st.info("No record found yet")

def Logout():
    st.info("You have been logout successfully")



st.title("JAMB Student Portal")
menu = ["Register", "Search", "Update", "Delete", "Display All", "Logout"]
choice = st.sidebar.selectbox("choose an option", menu)

if choice == "Register":
    register()
elif choice == "Search":
    search()
elif choice == "Update":
    update()
elif choice == "Delete":
    delete()
elif choice == "Display All":
    display()
elif choice == "Logout":
    Logout()
