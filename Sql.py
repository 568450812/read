from Database import *


class MenberManage:
    def __init__(self):
        self.mysql = MysqlHelper()
        self.mysql.open_mysql()  # 连接数据库

    def __del__(self):
        self.mysql.close_mysql()  # 关闭数据库

    def do_read(self):  # 阅读
        pass

    def do_query_by_bookName(self,bookname):  # 根据书名查找
        value = "select * from books where bookname = '%s'"%bookname
        result = self.mysql.select(value)
        if not result:
            return False
        else:
            return result # 多个元组套元组

    def do_query_by_author(self, author):  # 根据作者查找
        value = "select * from books where author = '%s'" % author
        result = self.mysql.select(value)
        if not result:
            return False
        else:
            return result  # 多个元组套元组

    def do_find_path(self,id):
        value = "select bookpath from books where id = %d"%id
        result = self.mysql.select(value)
        if not result:
            return False
        else:
            return result[0][0]

    def do_find_bysection(self,section,table):
        value = "select path from %s where section = %s"%(table,section)
        result = self.mysql.select(value)
        if not result:
            return False
        else:
            return result[0][0]


    def do_find_id(self,bookname,author):
        value = """select id from books where bookname = '%s',author = '%s'
        """%(bookname,author)
        result = self.mysql.select(value)
        if not result:
            return False
        else:
            return result[0][0]

    def do_find_section(self,bookname,author):
        value = self.do_find_id(bookname,author)
        value = "B" + str(value)
        data = "select * from %s "%value
        result = self.mysql.select(data)
        if not result:
            return False
        else:
            return result



    # 根据编号查询密码
    def select_passwd(self, id, passwd):

        value = "select passwd from members where id = '%s'" % id
        result = self.mysql.select(value)
        try:
            if passwd in result[0]:
                return True
            else:
                return False
        except Exception:
            print("输入信息有误")

    # 新用户注册
    def add_member(self, id, passwd):
        value = "insert into members values('%s','%s')" % (id, passwd)
        result = self.mysql.update(value)
        if result:
            return True
        else:
            return False

