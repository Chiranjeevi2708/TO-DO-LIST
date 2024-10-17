import sqlite3

conn = sqlite3.connect('db.sqlite3')

cursor = conn.cursor()

try:
    cursor.execute("DROP TABLE IF EXISTS todolist_app_todo")
    print("Table 'todolist_app_todo' deleted successfully.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")


conn.commit()

conn.close()
