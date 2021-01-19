from saveTicket import saveTicket
from findTicket import findTicket


class APP:
    def __init__(self):
        self.saveTicket = saveTicket()
        self.findTicket = findTicket()

    # 录入航班信息
    def inputAir(self):
        print("请输入航班信息:(起飞城市,降落城市,起飞日期,起飞时间,降落日期,降落时间,机票价格)")
        isContinue = False
        while not isContinue:
            self.saveTicket.start_add = input("起飞城市:")
            self.saveTicket.end_add = input("降落城市:")
            self.saveTicket.start_date = int(input("起飞日期:"))
            self.saveTicket.start_time = int(input("起飞时间:"))
            self.saveTicket.end_date = int(input("降落日期:"))
            self.saveTicket.end_time = int(input("降落时间:"))
            self.saveTicket.price = int(input("机票价格:"))

            isSave = input("确认保存?(Yes/No) default:Yes")
            if isSave == "yes" or isSave == "Yes" or isSave == "YES":
                isSave = False
            if not isSave:
                self.saveTicket.insertInfo()

            isContinue = input("是否继续录入?(Yse/No) default:Yes")
            if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
                isContinue = False

    # 删除航班信息
    def deleteAir(self):
        print("请输入要删除的航班aid:")
        isContinue = False
        while not isContinue:
            aid = input("aid:")
            self.saveTicket.delInfo(aid)
            isContinue = input("是否继续删除?(Yse/No) default:Yes")
            if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
                isContinue = False

    # 筛选和导出航班信息
    def matchAir(self):
        isContinue = False
        while not isContinue:
            self.findTicket.start_add = input("起飞城市:")
            self.findTicket.end_add = input("降落城市:")
            self.findTicket.mid_add = input("中转城市:")
            self.findTicket.start_date = input("出行日期:(20210209)")
            self.findTicket.gap_time = input("航班间隔时间:(default: 2 hour)")
            if self.findTicket.gap_time == '':
                self.findTicket.gap_time = 2 * 60 * 60
            else:
                self.findTicket.gap_time = int(self.findTicket.gap_time)
            if self.findTicket.start_date == '':
                self.findTicket.start_date = 20210209
            else:
                self.findTicket.start_date = int(self.findTicket.start_date)

            # 执行匹配函数
            self.findTicket.match()

            # 导出表格
            self.findTicket.getMatchInfo()

            isContinue = input("是否继续匹配?(Yse/No) default:Yes")
            if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
                isContinue = False

    # 更新航班信息
    def updateAir(self):
        isContinue = False
        while not isContinue:
            aid = input("请输入需要修改的航班aid:")
            price = input("请输入调整后的机票价格:")
            self.saveTicket.updateInfo(aid, "price", price)

            isContinue = input("是否继续更新?(Yse/No) default:Yes")
            if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
                isContinue = False

    # 展示所有航班信息
    def showAir(self):
        airlines = self.saveTicket.getAllInfo()
        for a in airlines:
            print(a)

    # 去除重复信息
    def delSameAir(self):
        self.saveTicket.delSameInfo()

    # 自定义查询航班信息
    def searchAir(self):
        isContinue = False
        while not isContinue:

            item = input("请输入要查找的字段:(start_add, end_add, start_date, start_time, start_stamp, end_date, end_time, end_stamp, price, ctime, utime)")
            if item == "start_date" or item == "start_time" or item == "start_stamp" or item == "end_date" or item == "end_time" or item == "end_stamp" or item == "price":
                data = int(input("请输入要查询的信息:"))
            else:
                data = input("请输入要查询的信息:")
            info = self.saveTicket.searchInfo(item, data)
            for i in info:
                print(i)
            isContinue = input("是否继续查找?(Yse/No) default:Yes")
            if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
                isContinue = False

    # 管理备注信息
    def addAirNote(self):
        isContinue = False
        while not isContinue:
            print('''
            1. 添加备注信息
            2. 删除备注信息
            3. 查看备注信息
            4. 退出
            ''')
            button1 = input("功能选择:")
            if button1 == "1":
                id = input("请输入备注id:")
                data = input("请输入备注信息:\n")
                self.saveTicket.controlNote("add",[int(id),data])
            if button1 == "2":
                id = input("请输入要删除的备注id:")
                self.saveTicket.controlNote("delete",int(id))
            if button1 == "3":
                self.saveTicket.controlNote("show","")
            elif button1 == "4":
                return 0
            isContinue = input("是否继续添加或删除信息?(Yse/No) default:Yes")
            if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
                isContinue = False

if __name__ == "__main__":
    app = APP()
    isContinue = False
    while not isContinue:
        print('''
        +-----------------+
        | 中 转 航 班 查 询 | 
        +-----------------+
        
        1. 录入航班信息
        2. 更新航班信息
        3. 查看所有航班信息
        4. 删除航班信息
        5. 去除重复航班信息
        6. 自定义查询航班信息
        7. 管理备注信息
        8. 检索和匹配航班信息
        9. 退出''')
        print("备注信息:")
        app.saveTicket.controlNote("show",'')
        print(" ")

        button = input("功能选择:")
        if button == '1':
            app.inputAir()
        elif button == '2':
            app.updateAir()
        elif button == '3':
            app.showAir()
        elif button == '4':
            app.deleteAir()
        elif button == '5':
            app.delSameAir()
        elif button == '6':
            app.searchAir()
        elif button == "7":
            app.addAirNote()
        elif button == '8':
            app.matchAir()
        elif button == '9':
            quit()
        else:
            print("输入无效..")
        isContinue = input("是否继续?(Yse/No) default:Yes")
        if isContinue == "yes" or isContinue == "Yes" or isContinue == "YES":
            isContinue = False
