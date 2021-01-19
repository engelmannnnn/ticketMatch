from saveTicket import saveTicket
import xlwt
import time


class findTicket:
    def __init__(self):
        self.start_add = ""
        self.mid_add = ""
        self.end_add = ""
        self.start_date = 0
        self.total_price = 0
        self.gap_time = 2 * 60 * 60  # 两段航班的间隔时间 秒
        self.max_time = 12 * 60 * 60  # 两段航班最大间隔时间 秒
        self.travel1 = []  # 第一段旅程列表，航班用字典存储
        self.travel2 = []  # 第二段
        self.db = saveTicket()  # 数据库对象
        self.matchInfo = []

    # 匹配第一段与第二段机票
    def match(self):
        # 清空匹配缓存
        self.db.delMatchInfo()
        self.matchInfo = []
        # 获取第一段机票
        travel1 = self.db.matchInfo(self.start_add, self.mid_add)
        self.travel1 = self.parseList(travel1)

        # 获取第二段机票
        travel2 = self.db.matchInfo(self.mid_add, self.end_add)
        self.travel2 = self.parseList(travel2)

        # 校验两段航程是否都有票
        for i in range(len(self.travel1)):
            for j in range(len(self.travel2)):
                # 筛选航班
                if self.travel1[i]["start_date"] == self.start_date:
                    if (self.travel2[j]["start_stamp"] - self.travel1[i]["end_stamp"]) > self.gap_time and (
                            self.travel2[j]["start_stamp"] - self.travel1[i]["end_stamp"]) < self.max_time:
                        aid1 = self.travel1[i]["aid"]  # 第一段航班aid
                        aid2 = self.travel2[j]["aid"]  # 第二段
                        # 获取已存储的航班列表
                        isSaved = self.db.searchMatchInfo(aid1, aid2)
                        if len(isSaved) == 0:
                            self.db.insertMatchInfo(aid1, aid2)

    # 获取匹配行程
    def getMatchInfo(self):
        # 获取缓存的行程单
        matchAir = self.db.getMatchInfo()
        for airLine in matchAir:
            # ((1, '深圳', '北京', 20210110, 1950, 1610279426, 20210110, 2255, 1610290526, 689, 1609930218, 1609930218), ((8, '北京', '朝阳', 20210113, 625, 1610490326, 20210113, 735, 1610494526, 564, 1609930218, 1609930218),))
            self.matchInfo.append(
                (self.db.searchInfo("aid", airLine[0])[0], self.db.searchInfo("aid", airLine[1])[0])
            )
        rows = ('aid', '开始城市', '中转城市', '起飞时间', '降落时间', '价格', 'aid', '中转城市', '降落城市', '起飞时间', '降落时间', '价格', '总价格', '间隔时间(小时)')
        workBook = xlwt.Workbook()
        workSheet = workBook.add_sheet('航班情况', cell_overwrite_ok=True)
        # 录入表格头
        for i in range(len(rows)):
            workSheet.write(0, i, rows[i])
        # 录入航班信息
        for i in range(len(self.matchInfo)):
            if len(self.matchInfo[i][0]) == 12:
                # aid
                workSheet.write(i + 1, 0, self.matchInfo[i][0][0])
                # 开始城市
                workSheet.write(i + 1, 1, self.matchInfo[i][0][1])
                # 中转城市
                workSheet.write(i + 1, 2, self.matchInfo[i][0][2])
                # 起飞时间
                timeStamp = self.matchInfo[i][0][5]
                timeArray = time.localtime(timeStamp)
                inputTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                workSheet.write(i + 1, 3, inputTime1)
                # 降落时间
                timeStamp = self.matchInfo[i][0][8]
                timeArray = time.localtime(timeStamp)
                inputTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                workSheet.write(i + 1, 4, inputTime2)
                # 价格
                workSheet.write(i + 1, 5, self.matchInfo[i][0][9])

                # aid
                workSheet.write(i + 1, 6, self.matchInfo[i][1][0])
                # 中转城市
                workSheet.write(i + 1, 7, self.matchInfo[i][1][1])
                # 降落城市
                workSheet.write(i + 1, 8, self.matchInfo[i][1][2])
                # 起飞时间
                timeStamp = self.matchInfo[i][1][5]
                timeArray = time.localtime(timeStamp)
                inputTime3 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                workSheet.write(i + 1, 9, inputTime3)
                # 降落时间
                timeStamp = self.matchInfo[i][1][8]
                timeArray = time.localtime(timeStamp)
                inputTime4 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                workSheet.write(i + 1, 10, inputTime4)
                # 价格
                workSheet.write(i + 1, 11, self.matchInfo[i][1][9])

                # 总价格
                workSheet.write(i + 1, 12, self.matchInfo[i][0][9] + self.matchInfo[i][1][9])
                # 时间差
                timeStamp = self.matchInfo[i][1][5] - self.matchInfo[i][0][8]
                inputTime5 = timeStamp / 60 / 60  # 换成hour
                workSheet.write(i + 1, 13, '%.2f' % inputTime5)

                # 打印显示
                print('aid:', self.matchInfo[i][0][0],
                      '开始城市:', self.matchInfo[i][0][1],
                      '中转城市:', self.matchInfo[i][0][2],
                      '起飞时间:', inputTime1,
                      '降落时间:', inputTime2,
                      '价格:', self.matchInfo[i][0][9],
                      '| |',
                      'aid:', self.matchInfo[i][1][0],
                      '中转城市:', self.matchInfo[i][1][1],
                      '降落城市:', self.matchInfo[i][1][2],
                      '起飞时间:', inputTime3,
                      '降落时间:', inputTime4,
                      '价格:', self.matchInfo[i][1][9],
                      '总价格:', self.matchInfo[i][0][9] + self.matchInfo[i][1][9],
                      '间隔时间(小时):', '%.2f' % inputTime5)

        workBook.save('airLine.xls')
        print("表格已导出..")

    # 解析数据库
    def parseList(self, tuple):
        length = len(tuple)
        list = []
        for i in range(length):
            if len(tuple[i]) == 12:
                line = {}
                line["aid"] = tuple[i][0]
                line["start_add"] = tuple[i][1]
                line["end_add"] = tuple[i][2]
                line["start_date"] = tuple[i][3]
                line["start_time"] = tuple[i][4]
                line["start_stamp"] = tuple[i][5]
                line["end_date"] = tuple[i][6]
                line["end_time"] = tuple[i][7]
                line["end_stamp"] = tuple[i][8]
                line["price"] = tuple[i][9]
                line["ctime"] = tuple[i][10]
                line["utime"] = tuple[i][11]
                list.append(line)
            elif len(tuple[i]) == 3:
                line = {}
                line["start_aid"] = tuple[i][0]
                line["end_aid"] = tuple[i][1]
                line["ctime"] = tuple[i][2]
            else:
                print("数据库解析错误!!!")
                return 0
        return list

    def test(self):
        self.start_add = "深圳"
        self.mid_add = "北京"
        self.end_add = "朝阳"
        self.match()
        self.getMatchInfo()
        for i in self.matchInfo:
            print(i)


if __name__ == "__main__":
    test = findTicket()
    test.test()
