import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Define functions to interact with the database

def create_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT, task_status TEXT, task_due_date DATE)')
    conn.commit()
    conn.close()

def add_data(task, task_status, task_due_date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO taskstable(task, task_status, task_due_date) VALUES (?, ?, ?)', (task, task_status, task_due_date))
    conn.commit()
    conn.close()

def view_all_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM taskstable')
    data = c.fetchall()
    conn.close()
    return [row for row in data if row[0]]

def update_data(task, new_task_status, new_task_due_date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE taskstable SET task_status=?, task_due_date=? WHERE task=?', (new_task_status, new_task_due_date, task))
    conn.commit()
    conn.close()

def delete_data(task):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM taskstable WHERE task=?', (task,))
    conn.commit()
    conn.close()

def view_unique_tasks():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT task FROM taskstable WHERE task IS NOT NULL AND task != ""')
    data = c.fetchall()
    conn.close()
    return data

# Main function for Streamlit app

def main():
    st.title("ToDo App With Streamlit")

    menu=["Create","Read","Update","Delete"]
    choice=st.sidebar.selectbox("Menu",menu)
     
    if choice == "Create":
        st.subheader("Add Items")

        # Layout
        col1,col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")
    
        with col2:
            task_status = st.selectbox("Status",["ToDo","Doing","Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success("Successfully Added Data: {}".format(task))


    elif choice == "Read":
        st.subheader("View Items")
        result = view_all_data()
        if result:
            df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
            with st.expander("View All Data"):
                st.dataframe(df)
            
            with st.expander("Task Status"):
                task_df = df['Status'].value_counts().to_frame()
                task_df = task_df.reset_index()
                st.dataframe(task_df)

                p1 = px.pie(task_df, names='Status', values='count')
                st.plotly_chart(p1)

        else:
            st.write("No tasks found.")

    elif choice == "Update":
        st.subheader("Edit/Update Items")
        result = view_all_data()
        if result:
            df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
            with st.expander("Current Data"):
                st.dataframe(df)

            list_of_tasks = [i[0] for i in view_unique_tasks()]
            selected_task = st.selectbox("Task To Edit", list_of_tasks)

            new_task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            new_task_due_date = st.date_input("Due Date")

            if st.button("Update Task"):
                update_data(selected_task, new_task_status, new_task_due_date)
                st.success("Task Updated Successfully")

        else:
            st.write("No tasks found.")

    elif choice == "Delete":
        st.subheader("Delete Items")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)
        
        list_of_tasks = [i[0] for i in view_unique_tasks()]
        selected_task = st.selectbox("Task To Delete", list_of_tasks)
        st.warning("Do you want to delete {}".format(selected_task))
        if st.button("Delete Task"):
            delete_data(selected_task)
            st.success("Task has been successfully deleted")

        
   

if __name__ == '__main__':
    main()
