"""
将电子书分章节写入文档 将书名，作者，路径存入总的书表中 将章节和路径存入特定的书表中
需要一个bookmanager库
# create database bookmanager default charset=utf8;
和一个books表
# create table books (id int(8) primary key auto_increament,bookname varchar(32),
# author varchar(32) not null,bookpath varchar(128) not null)default charset=utf8;
使用 在linux终端运行文件 后面加 书名 作者 路径（绝对或相对路径）
例：python3 insert_books 雪中悍刀行 烽火戏诸侯 file.txt
"""


import sys
import os
import re
import pymysql

book_name = sys.argv[1]
book_author = sys.argv[2]
book_path = os.path.abspath(sys.argv[3])



try:
    conn = pymysql.connect("localhost", "root", "123456", "bookmanager",use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    sql = """insert into books (bookname,author,bookpath) values('%s','%s','%s')
    """%(book_name,book_author,book_path)
    result = cursor.execute(sql)
    print(result)
    conn.commit()


except Exception as e:
    print(e)
    conn.rollback()


try:
    f = open("%s" % book_path)
except IOError:
    print("路径错误或文件已存在")
else:
    sql01 = "select id from books where bookpath = '%s'" % book_path
    cursor.execute(sql01)
    book_id = cursor.fetchall()[0][0]
    pattern = r"^第.{1,6}章.*"
    os.mkdir("%s" % book_name)
    value = f.readlines()
    b = open("%s/写在前面.txt"%book_name, "w",encoding="utf-8")
    for i in value:
        path = re.findall(pattern, i)
        if len(path) != 0:
            b.close()
            new_path = "%s/%s.txt"%(book_name,path[0])
            print(new_path)
            b = open(new_path, "w",encoding="utf-8")
            sql03 = "insert into booksection (book_id,section_name,section_path) values(%d,'%s','%s');" % (book_id,path[0],os.path.abspath(new_path))
            result = cursor.execute(sql03)
            conn.commit()
        b.write(i)

cursor.close()
conn.close()




