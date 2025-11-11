import streamlit as st
import mysql.connector
import pandas as pd

# -------------------------
# Connect to MySQL Database
# -------------------------
# Use Streamlit secrets for security
# Create a .streamlit/secrets.toml file with:
# [mysql]
# host = "localhost"
# user = "root"
# password = "kolade789@#$"
# database = "day12k"

mydatabase = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)

mycursor = mydatabase.cursor()

# -------------------------
# Register New Student
# -------------------------
def register():
    st.subheader("Register New Student")
    reg_no = st.number_input("Enter Registration Number:", min_value=0, step=1)
    full_name = st.text_input("Enter Full Name:")
    gender = st.selectbox("Select Gender:", ["Male", "Female"])
    state = st.text_input("Enter State of Origin:")
    email = st.text_input("Enter Email Address:")

    if st.button("Register"):
        if reg_no and full_name and gender and state and email:
            query = "INSERT INTO informations(reg_no, full_name, gender, state, email) VALUES (%s, %s, %s, %s, %s)"
            values = (reg_no, full_name, gender, state, email)
            try:
                mycursor.execute(query, values)
                mydatabase.commit()
                st.success("Information successfully uploaded!")
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please fill in all the fields before submitting.")

# -------------------------
# Search Student Record
# -------------------------
def search():
    st.subheader("Search Student Record")
    reg_no = st.number_input("Enter registration number to search:", min_value=0, step=1)

    if st.button("Search"):
        query = "SELECT * FROM informations WHERE reg_no = %s"
        mycursor.execute(query, (reg_no,))
        result = mycursor.fetchall()

        if not result:
            st.warning("Record not found.")
        else:
            df = pd.DataFrame(result, columns=["Reg_no", "Full Name", "Gender", "State", "Email"])
            st.table(df)

# -------------------------
# Update Student Record
# -------------------------
def update():
    st.subheader("Update Student Record")
    reg_no = st.number_input("Enter Registration Number to Update:", min_value=0, step=1)
    full_name = st.text_input("Full Name:")
    gender = st.selectbox("Gender:", ["Male", "Female"])
    state = st.text_input("State of Origin:")
    email = st.text_input("Email Address:")

    if st.button("Update"):
        query = """
        UPDATE informations
        SET full_name = %s, gender = %s, state = %s, email = %s
        WHERE reg_no = %s
        """
        values = (full_name, gender, state, email, reg_no)
        try:
            mycursor.execute(query, values)
            mydatabase.commit()
            st.success("Record updated successfully")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

# -------------------------
# Delete Student Record
# -------------------------
def delete():
    st.subheader("Delete Student Record")
    reg_no = st.number_input("Enter Registration Number to Delete:", min_value=0, step=1)
    if st.button("Delete"):
        query = "DELETE FROM informations WHERE reg_no = %s"
        try:
            mycursor.execute(query, (reg_no,))
            mydatabase.commit()
            st.success("Record deleted successfully")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

# -------------------------
# Display All Students
# -------------------------
def display():
    st.subheader("All Registered Students")
    query = "SELECT * FROM informations"
    mycursor.execute(query)
    result = mycursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["Reg_no", "Full Name", "Gender", "State", "Email"])
        st.dataframe(df)
    else:
        st.info("No record found yet.")

# -------------------------
# Logout
# -------------------------
def logout():
    st.info("You have been logged out successfully")

# -------------------------
# Streamlit Sidebar Menu
# -------------------------
st.title("JAMB Student Portal")
menu = ["Register", "Search", "Update", "Delete", "Display All", "Logout"]
choice = st.sidebar.selectbox("Choose an option", menu)

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
    logout()
