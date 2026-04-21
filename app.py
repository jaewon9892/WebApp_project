import streamlit as st
import mysql.connector
from mysql.connector import Error
import pymysql

#MySQL과 연결을 한다.
def get_db_connection():
    # st.secrets를 통해 보안 정보를 가져온다
    db_config = st.secrets["mysql"]

    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

# Task를 저장하는 함수
def add_task(task):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO todos(task) VALUES (%s)"
        cursor.execute(query, (task,))
        connection.commit()
        cursor.close()
    except Error as e:
        st.error(f"Error adding task: {e}")

# Task를 불러오는 함수
def get_task():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todos WHERE completed=FALSE ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        cursor.close()
        connection.close()
        return tasks
    except Error as e:
        st.error(f"Error: {e}")
        return []

# 작업을 완료하는 부분
def mark_task_completed(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE todos SET completed=TRUE WHERE id=%s"
        cursor.execute(query, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        st.error(f"Error: {e}")

connection = get_db_connection()

# User Interface
st.header("Welcome to Super Todo App", divider="rainbow")

# 새로운 todo를 입력하는 부분
new_task = st.text_input("New task")

if st.button("Add Task") and new_task:
    add_task(new_task)
    st.success(f"Task '{new_task}' added successfully!")

# task를 완료하는 부분
task_id = st.text_input("task id")

if st.button("Complete") and task_id:
    mark_task_completed(task_id)
    st.success(f"Task '{task_id}' updated!")

tasks = get_task()

st.write(tasks)
