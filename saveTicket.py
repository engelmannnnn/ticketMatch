import pymysql
import time


class saveTicket:
    def __init__(self):
        self.start_add = ""
        self.end_add = ""
        self.start_date = ""
        self.start_time = ""
        self.end_date = ""
        self.end_time = ""
        self.price = 0

        # 连接db
        self.db = pymysql.connect("127.0.0.1", "root", "676996", "localDB")
        # 建立游标
        self.cursor = self.db.cursor()

    # 写入数据
    def insertInfo(self):
        ctime = int(time.time())
        # '2013-10-10 23:40:00'
        startTime = str(self.start_date)[0:4] + '-' + str(self.start_date)[4:6] + '-' + str(self.start_date)[6:8] + ' ' + str(self.start_time)[:-2] + ':' + str(self.start_time)[
                                                                                                                                                            -2:] + ':00'
        # print(start_time)
        startTimeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        startTimeStamp = int(time.mktime(startTimeArray))
        # print(timeStamp)

        endTime = str(self.end_date)[0:4] + '-' + str(self.end_date)[4:6] + '-' + str(self.end_date)[6:8] + ' ' + str(self.end_time)[:-2] + ':' + str(self.end_time)[-2:] + ':00'
        endTimeArray = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        endTimeStamp = int(time.mktime(endTimeArray))

        sql = '''INSERT INTO `airPrice`(start_add, end_add, start_date, start_time, start_stamp, end_date, end_time, end_stamp, price, ctime, utime)
        VALUES ('{}','{}',{},{},{},{},{},{},{},{},{})'''.format(self.start_add, self.end_add, self.start_date, self.start_time, startTimeStamp, self.end_date, self.end_time,
                                                                endTimeStamp, self.price, ctime, ctime)

        # print(sql)
        try:
            # 尝试执行sql
            self.cursor.execute(sql)
            self.db.commit()
            print(self.searchInfo("ctime", ctime)[0])
            print("数据存储成功..")
        except:
            self.db.rollback()
            print("！！数据库错误！！")

        # self.db.close()

    # 删除数据
    def delInfo(self, aid):
        sql = '''DELETE FROM airPrice WHERE aid = {}'''.format(aid)

        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("删除成功..")
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 更新数据
    def updateInfo(self, aid, item, data):
        utime = int(time.time())
        sql = '''UPDATE airPrice SET {} = '{}', utime = {} WHERE aid = '{}'
         '''.format(item, data, utime, aid)
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("航班信息更新成功..")
            print(self.searchInfo("aid", aid))
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 查询数据
    def searchInfo(self, item, data):
        sql = '''SELECT * FROM airPrice WHERE {} = '{}'
        '''.format(item, data)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 精确查询
    def matchInfo(self, add1, add2):
        sql = '''SELECT * FROM airPrice WHERE start_add = '{}' AND end_add = '{}'
         '''.format(add1, add2)
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 获取匹配信息
    def getMatchInfo(self):
        sql = '''SELECT * FROM airMatch'''
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
            print("！！数据库错误！！")

    # 展示所有航班记录
    def getAllInfo(self):
        sql = '''SELECT * FROM airPrice'''
        try:
            self.cursor.execute(sql)
            airlines = self.cursor.fetchall()
            return airlines
        except:
            self.db.rollback()
            print("！！数据库错误！！")

    # 记录匹配航班
    def insertMatchInfo(self, aid1, aid2):
        ctime = int(time.time())
        sql = '''INSERT INTO `airMatch`(start_aid, end_aid, ctime) VALUES ({},{},{})
        '''.format(aid1, aid2, ctime)
        # print(sql)
        try:
            # 尝试执行sql
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 清空airMatch
    def delMatchInfo(self):
        a = '''DELETE FROM airMatch'''
        try:
            # 尝试执行sql
            self.cursor.execute(a)
            self.db.commit()
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 查询匹配航班
    def searchMatchInfo(self, aid1, aid2):
        sql = '''SELECT * FROM airMatch WHERE start_aid = {} AND end_aid = {}
        '''.format(aid1, aid2)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
            print("！！数据库错误！！")
        # self.db.close()

    # 去除重复航班信息
    def delSameInfo(self):
        info = self.getAllInfo()
        length = len(info)
        count = 0
        for i in range(0, length - 1):
            for j in range(i + 1, length):
                # 起飞,降落地点,起飞时间,降落时间,价格相同
                if info[i][1] == info[j][1] and info[i][2] == info[j][2] and info[i][5] == info[j][5] and info[i][8] == info[j][8] and info[i][9] == info[j][9]:
                    sameAid = info[j][0]
                    print("已删除:")
                    print(info[j])
                    self.delInfo(sameAid)
                    count += 1
        if count == 0:
            print("没有重复的航班信息..")

    # 添加,删除或展示备注信息 type = add, delete,show
    def controlNote(self, type, data):
        if type == "add":
            id = data[0]
            note = data[1]
            sql = '''INSERT INTO `airNote`(id,note) values ({},'{}')'''.format(id, note)
            # print(sql)
            try:
                self.cursor.execute(sql)
                self.db.commit()
                print("添加备注成功..")
            except:
                self.db.rollback()
                print("！！数据库错误！！")
        if type == "delete":
            id = data
            sql = '''DELETE FROM `airNote` WHERE id = {}'''.format(id)
            try:
                self.cursor.execute(sql)
                self.db.commit()
                print("添加删除成功..")
            except:
                self.db.rollback()
        if type == "show":
            sql = '''SELECT * FROM airNote'''
            try:
                self.cursor.execute(sql)
                notes = self.cursor.fetchall()
                if len(notes) > 0:
                    for note in notes:
                        print(str(note[0])+".",note[1])
            except:
                self.db.rollback()
                print("！！数据库错误！！")

    def test(self):
        self.start_add = "深圳"
        self.end_add = "天津"
        self.start_date = "20200105"
        self.start_time = "930"
        self.end_date = "20200106"
        self.end_time = "1525"
        self.price = 997
        # self.delMatchInfo()
        # self.insertInfo()
        # self.delInfo(6)
        # self.updateInfo(8,"end_add","日本")
        # a = self.searchInfo("start_add","深圳")
        # a = self.matchInfo("深圳","日本")
        # print(a)
        # self.delSameInfo()
        self.controlNote("delete",1)

if __name__ == "__main__":
    a = saveTicket()
    a.test()
