
import streamlit as st
import pandas as pd
import sqlite3

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
    return data

def update_data(task, task_status, task_due_date, new_task, new_task_status, new_task_due_date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE taskstable SET task=?, task_status=?, task_due_date=? WHERE task=? AND task_status=? AND task_due_date=?',
              (new_task, new_task_status, new_task_due_date, task, task_status, task_due_date))
    conn.commit()
    conn.close()

def delete_data(task, task_status, task_due_date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM taskstable WHERE task=? AND task_status=? AND task_due_date=?', (task, task_status, task_due_date))
    conn.commit()
    conn.close()

# Main function for Streamlit app

def main():
    st.title("ToDo App With Streamlit")

    menu=["Create","Read","Update","Delete","About"]
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
            st.dataframe(df)
        else:
            st.write("No tasks found.")

    elif choice == "Update":
        st.subheader("Edit/Update Items")
        result = view_all_data()
        if result:
            df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
            st.dataframe(df)
            task_to_update = st.text_input("Enter the task to update")
            if st.button("Update Task"):
                new_task = st.text_area("Task To Do")
                new_task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
                new_task_due_date = st.date_input("Due Date")
                update_data(task_to_update, df[df['Task'] == task_to_update]['Status'].iloc[0],
                            df[df['Task'] == task_to_update]['Due Date'].iloc[0],
                            new_task, new_task_status, new_task_due_date)
                st.success("Task Updated Successfully")
        else:
            st.write("No tasks found.")

    elif choice == "Delete":
        st.subheader("Delete Items")
        result = view_all_data()
        if result:
            df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
            st.dataframe(df)
            task_to_delete = st.text_input("Enter the task to delete")
            if st.button("Delete Task"):
                delete_data(task_to_delete, df[df['Task'] == task_to_delete]['Status'].iloc[0],
                            df[df['Task'] == task_to_delete]['Due Date'].iloc[0])
                st.success("Task Deleted Successfully")
        else:
            st.write("No tasks found.")
 
    else:
        st.subheader("About")
        # You can provide information about your app here


if __name__ == '__main__':
    main()