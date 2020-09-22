
import sqlite3 
  
connection = sqlite3.connect("library.db") 
cursor = connection.cursor() 
  
# SQL piece of code Executed 
# SQL piece of code Executed 
cursor.executescript(""" 
    CREATE TABLE people( 
        firstname, 
        lastname, 
        age 
    ); 
   
    CREATE TABLE book( 
        title, 
        author, 
        published 
    ); 
   
    INSERT INTO 
    book(title, author, published) 
    VALUES ( 
        'Dan Clarke''s GFG Detective Agency', 
        'Sean Simpsons', 
        1987 
    ); 
    """) 
  
sql = """ 
SELECT COUNT(*) FROM book;"""
  
cursor.execute(sql) 
  
# The output in fetched and returned 
# as a List by fetchall() 
result = cursor.fetchall() 
print(result) 
  
sql = """ 
SELECT * FROM book;"""
  
cursor.execute(sql) 
  
result = cursor.fetchall() 
print(result) 
  
# Changes saved into database 
connection.commit() 
  
# Connection closed(broken)  
# with DataBase 
connection.close() 
