import tkinter as tk
from tkinter import filedialog
import sqlite3

def copy_tables(db_path, target_table):
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 获取所有以"table_mathexercise"开头的表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name GLOB 'table_mathexercise*'")
        table_names = [table[0] for table in cursor.fetchall()]

        # 遍历所有匹配的表
        for table_name in table_names:
            print(f"Copying data from {table_name} to {target_table}")
            
            # 获取源表的列信息
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall()]
            column_names = ', '.join(columns)
            
            # 构建目标表的列名字符串
            placeholders = ', '.join(['?'] * len(columns))
            
            # 创建目标表
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {target_table} ({column_names})")
            
            # 从源表读取数据并插入到目标表
            cursor.execute(f"SELECT {column_names} FROM {table_name}")
            rows = cursor.fetchall()
            cursor.executemany(f"INSERT INTO {target_table} ({column_names}) VALUES ({placeholders})", rows)
        
        # 提交事务
        conn.commit()
        print(f"Data from all tables starting with 'table_mathexercise' has been copied to {target_table}.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # 关闭数据库连接
        conn.close()

def select_db_file():
    file_path = filedialog.askopenfilename(title="Select Database File",
                                           filetypes=[("Database files", "*.db"), ("All files", "*.*")])
    if file_path:
        db_entry.delete(0, tk.END)
        db_entry.insert(0, file_path)

def execute_operation():
    db_path = db_entry.get()
    if db_path:
        target_table = "table_mathexercise_anonymous"
        copy_tables(db_path, target_table)
    else:
        tk.messagebox.showerror("Error", "Please select a database file first.")

# 创建主窗口
root = tk.Tk()
root.title("Database Table Copier")

# 创建数据库路径输入框和按钮
db_frame = tk.Frame(root)
db_frame.pack(pady=20)

db_label = tk.Label(db_frame, text="Database File Path:")
db_label.grid(row=0, column=0, padx=10)

db_entry = tk.Entry(db_frame, width=50)
db_entry.grid(row=0, column=1, padx=10)

browse_button = tk.Button(db_frame, text="Browse", command=select_db_file)
browse_button.grid(row=0, column=2, padx=10)

# 创建执行操作按钮
execute_button = tk.Button(root, text="Execute Operation", command=execute_operation)
execute_button.pack(pady=20)

# 启动GUI事件循环
root.mainloop()