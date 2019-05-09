import pymssql
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import sqlite3
import time
import logging

# 参考 https://www.cnblogs.com/baiyangcao/p/pymssql_basic.html

class ReceiveDeliverySyncMessage:
    def __init__(self):
        '''
        初始化日志组件
        '''
        logging.basicConfig(filename="log-ReceiveDeliverySyncMessage.log",
                            level=logging.DEBUG,
                            format='%(levelname)s %(asctime)s %(message)s', # 记录格式
                            datefmt='%Y-%m-%d %H:%M:%S',  # 时间格式
                            )
        '''
        初始化数据库连接
        '''
        self.ssbConn = pymssql.connect('202.75.218.213', 'sa', 'OCTmami2013', 'SSB')
        self.ssb = self.ssbConn.cursor()
        # 正式数据库
        # self.octerpConn = pymssql.connect('202.75.218.213', 'sa', 'OCTmami2013', 'OCTERP2010')
        # 测试数据库
        self.octerpConn = pymssql.connect('202.91.241.219', 'sa', 'OCTmami2013', 'BSERP3_20170513')
        self.octerp2010 = self.octerpConn.cursor()

        # 存储要保存的数据
        # self.deliveryList = []
        self.deliveryitemList = []

        # sqlite 存放临时数据
        self.sqliteConn = sqlite3.connect('temp.db')

        # 设置返回数据是字典格式
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.sqliteConn.row_factory = dict_factory

        self.sqlite = self.sqliteConn.cursor()

        # 查询临时表是否存在，存在则删除
        self.sqlite.execute("SELECT * FROM sqlite_master WHERE type='table' and tbl_name = 'temp_delivery'")
        row = self.sqlite.fetchone()
        if row:
            self.sqlite.execute('DROP TABLE temp_delivery;')
            self.sqlite.execute('DROP TABLE temp_delivery_item;')
            self.sqliteConn.commit()
        # 创建临时表
        self.sqlite.execute('''CREATE TABLE `temp_delivery` (
            ID INTEGER PRIMARY KEY  AUTOINCREMENT ,
            `DeliveryNo`  varchar(50) ,
            `OrderNo`  varchar(50) ,
            `DeliveryType`  varchar(50) ,
            `DeliveryStatus`  int ,
            `ShopNo`  varchar(50) ,
            `ShopName`  varchar(50) ,
            `ShopType`  int ,
            `ShopPlatform`  varchar(50) ,
            `CustmerNo`  varchar(50) ,
            `CustmerName`  varchar(50) ,
            `CustmerMemo`  text ,
            `ReceiveName`  varchar(50) ,
            `ReceiveProvince`  varchar(50) ,
            `ReceiveCity`  varchar(50) ,
            `ReceiveDistrict`  varchar(50) ,
            `ReceiveAddress`  text ,
            `ReceiveMobile`  varchar(50) ,
            `ReceivePhone`  varchar(50) ,
            `ReceiveZip`  varchar(50) ,
            `ShipTypeCode`  varchar(50) ,
            `ShipTypeName`  varchar(50) ,
            `TrackingNo`  varchar(50) ,
            `GoodsCount`  decimal(18,4) ,
            `GoodsWeight`  decimal(18,4) ,
            `GoodsAmount`  decimal(18,4) ,
            `FreightAmount`  decimal(18,4) ,
            `DiscountAmount`  decimal(18,4) ,
            `ReceivableAmount`  decimal(18,4) ,
            `Remark`  text ,
            `ModifyTime`  datetime ,
            `CreateTime`  datetime 
        );''')
        self.sqlite.execute('''CREATE TABLE `temp_delivery_item` (
            ID INTEGER PRIMARY KEY  AUTOINCREMENT ,
            `DeliveryItemNo`  varchar(50) ,
            `DeliveryNo`  varchar(50) ,
            `ProductNo`  varchar(50) ,
            `ProductType`  int ,
            `ProductName`  text ,
            `GoodsNo`  varchar(50) ,
            `GoodsType`  varchar(50) ,
            `SpecValue`  varchar(50) ,
            `SpecName`  varchar(50) ,
            `SpecValue1`  varchar(50) ,
            `SpecName1`  varchar(50) ,
            `SpecValue2`  varchar(50) ,
            `SpecName2`  varchar(50) ,
            `CostPrice`  decimal(18,4) ,
            `CurrentPrice`  decimal(18,4) ,
            `MarketPrice`  decimal(18,4) ,
            `Quantity`  decimal(18,4) ,
            `Unit`  varchar(50) ,
            `Weight`  decimal(18,4) ,
            `DiscountAmount`  decimal(18,4) ,
            `TotalAmount`  decimal(18,4) 
        );''')
        self.sqliteConn.commit()

    def run(self):
        ssbId = 0
        # 获取xml数据,解析存储
        for xml, id in self.getXmlDataList():
            ssbId = id
            # 解析xml, 排除需要剔除的数据
            self.parseXml(xml)
        # 事务写入
        try:
            # # 写入渠道调拨单
            # self.createQddbd()
            #
            # # 写入零售销货单
            # self.createLsxhd()
            #
            # # 写入批发销货通知单
            # self.createFsend()
            #
            # # 库存操作
            # self.createSpkcb()

            # 记录历史单号
            self.createHistory()
            print(ssbId)
            # 提交
            # self.octerpConn.commit()
            logging.info('处理成功 %s' % ssbId)
        except Exception as e:
            self.octerpConn.rollback()
            # 文件日志
            logging.exception(e)
            # 数据库日志
            msg = ''
            # self.createLog(ssbId, msg)
            # self.octerp2010.commit()
            # 异常处理
            print(e)

    def getXmlDataList(self):
        '''
        查询需要的xml数据
        :return:
        '''
        # self.ssb.execute("select MessageBody as body from SSBMessageIn where UpdateTime is Null and Status = 'O' and MessageType="Delivery"")
        # self.ssb.execute('select MessageBody as body from SSBMessageIn where InTime = %s', "2019-04-08 01:00:03.000")
        self.ssb.execute('select ID, MessageBody as body from SSBMessageIn where Id = %s and MessageType= %s',
                         ("10084565", "Delivery"))
        while True:
            row = self.ssb.fetchone()
            # 如果为空值则不返回了
            if not row:
                break
            # 返回xml数据
            yield (row[1], row[0])

    def parseXml(self, xml):
        '''
        解析xml数据
        :param xml:
        :return:
        '''
        # 从字符串中解析 xml
        root = ET.fromstring(xml)
        # findall 查询所有的 Delivery 标签
        DeliveryList = root.findall("Body/Delivery")
        # print(DeliveryList)
        # 执行事务
        try:
            for delivery in DeliveryList:
                # 过滤数据
                dvu = self.checkDeliveryCanUse(delivery)
                # 如果这条数据不符合条件直接跳过
                if not dvu:
                    continue

                item = {}
                # 获取属性
                item['DeliveryNo'] = delivery.get('DeliveryNo')
                item['OrderNo'] = delivery.get('OrderNo')
                item['DeliveryType'] = delivery.get('DeliveryType')
                item['DeliveryStatus'] = delivery.get('DeliveryStatus')
                item['ShopNo'] = delivery.get('ShopNo')
                item['ShopName'] = delivery.get('ShopName')
                item['ShopType'] = delivery.get('ShopType')
                item['ShopPlatform'] = delivery.get('ShopPlatform')
                item['CustmerNo'] = delivery.get('CustmerNo')
                item['CustmerName'] = delivery.get('CustmerName')
                item['CustmerMemo'] = delivery.get('CustmerMemo')
                item['ReceiveName'] = delivery.get('ReceiveName')
                item['ReceiveProvince'] = delivery.get('ReceiveProvince')
                item['ReceiveCity'] = delivery.get('ReceiveCity')
                item['ReceiveDistrict'] = delivery.get('ReceiveDistrict')
                item['ReceiveAddress'] = delivery.get('ReceiveAddress')
                item['ReceiveMobile'] = delivery.get('ReceiveMobile')
                item['ReceivePhone'] = delivery.get('ReceivePhone')
                item['ReceiveZip'] = delivery.get('ReceiveZip')
                item['ShipTypeCode'] = delivery.get('ShipTypeCode')
                item['ShipTypeName'] = delivery.get('ShipTypeName')
                item['TrackingNo'] = delivery.get('TrackingNo')
                item['GoodsCount'] = delivery.get('GoodsCount')
                item['GoodsWeight'] = delivery.get('GoodsWeight')
                item['GoodsAmount'] = delivery.get('GoodsAmount')
                item['FreightAmount'] = delivery.get('FreightAmount')
                item['DiscountAmount'] = delivery.get('DiscountAmount')
                item['ReceivableAmount'] = delivery.get('ReceivableAmount')
                item['Remark'] = delivery.get('Remark')
                item['ModifyTime'] = delivery.get('ModifyTime')
                item['CreateTime'] = delivery.get('CreateTime')
                # 保存数据
                # self.deliveryList.append(item)
                self.insert(item, 'temp_delivery', self.sqlite)
                # 获取详情数据
                deliveryItemList = delivery.findall("DeliveryItem")
                for deliveryItem in deliveryItemList:
                    # 过滤数据
                    dicv = self.checkDeliveryItemCanUse(deliveryItem)
                    if not dicv:
                        continue

                    dItem = {}
                    dItem['DeliveryItemNo'] = deliveryItem.get('DeliveryItemNo')
                    dItem['DeliveryNo'] = deliveryItem.get('DeliveryNo')
                    dItem['ProductNo'] = deliveryItem.get('ProductNo')
                    dItem['ProductType'] = deliveryItem.get('ProductType')
                    dItem['ProductName'] = deliveryItem.get('ProductName')
                    dItem['GoodsNo'] = deliveryItem.get('GoodsNo')
                    dItem['GoodsType'] = deliveryItem.get('GoodsType')
                    dItem['SpecValue'] = deliveryItem.get('SpecValue')
                    dItem['SpecName'] = deliveryItem.get('SpecName')

                    # 拆分规格属性信息
                    dItem['SpecValue1'] = ''
                    dItem['SpecName1'] = ''
                    dItem['SpecValue2'] = ''
                    dItem['SpecName2'] = ''
                    # 分割 赋值
                    if dItem['SpecValue'] and '|' in dItem['SpecValue']:
                        specV = dItem['SpecValue'].split('|')
                        dItem['SpecValue1'] = specV[0]
                        dItem['SpecName1'] = ''
                        dItem['SpecValue2'] = specV[1]
                        dItem['SpecName2'] = ''

                    dItem['CostPrice'] = deliveryItem.get('CostPrice')
                    dItem['CurrentPrice'] = deliveryItem.get('CurrentPrice')
                    dItem['MarketPrice'] = deliveryItem.get('MarketPrice')
                    dItem['Quantity'] = deliveryItem.get('Quantity')
                    dItem['Unit'] = deliveryItem.get('Unit')
                    dItem['Weight'] = deliveryItem.get('Weight')
                    dItem['DiscountAmount'] = deliveryItem.get('DiscountAmount')
                    dItem['TotalAmount'] = deliveryItem.get('TotalAmount')
                    # 添加到临时表
                    # self.deliveryitemList.append(dItem)
                    self.insert(dItem, 'temp_delivery_item', self.sqlite)
            self.sqliteConn.commit()
        except Exception as e:
            print(e)
            self.sqliteConn.rollback()
            return False

        return True

    def checkDeliveryCanUse(self, delivery):
        '''
        过滤 Delivery 数据
        :param delivery:
        :return:
        '''
        ShopNo = delivery.get('ShopNo')
        DeliveryNo = delivery.get('DeliveryNo')
        can = True
        # 增加非直营电商店铺的判断，未来按照客户做批发销货单
        # 判断前四位
        if ShopNo[:4] == 'sysc' or ShopNo[:4] == 'xxtm' or ShopNo[:4] == 'sycs':
            can = False

        # 排除历史数据
        self.octerp2010.execute('SELECT DeliveryNo FROM API_ReceiveDeliveryHistory where DeliveryNo = %s', DeliveryNo)
        row = self.octerp2010.fetchone()
        # if row:
        #     can = False

        return can

    def checkDeliveryItemCanUse(self, deliveryItem):
        '''
        过滤 DeliveryItem 数据
        :param deliveryItem:
        :return:
        '''
        GoodsNo = deliveryItem.get('GoodsNo')
        # 排除的数据
        excludeGoodsNo = ['F4415308', 'F4415309', 'F4415310', 'F4415311']
        can = True
        if GoodsNo in excludeGoodsNo:
            can = False

        return can

    def createQddbd(self):
        '''
        创建渠道调拨单和明细单
        :return: 返回店铺对应的 主键id
        '''
        # 保存店铺对应的 主键id
        # shopNo_newid = {}
        row = self.sqlite.execute(
            'select ShopNo, DeliveryType, MAX(CreateTime) CreateTime, SUM(GoodsCount) GoodsCount, SUM(GoodsAmount) GoodsAmount from temp_delivery group by ShopNo, DeliveryType')
        qddbdList = row.fetchall()
        for qddbdInfo in qddbdList:
            # 如果不是自营的跳过
            if qddbdInfo['ShopNo'][:3] != '021':
                continue
            # 创建退货单id
            sql = "SELECT CONVERT(DATE, GETDATE()) NowTime, CONVERT(DATE, '" + qddbdInfo['CreateTime'] + "'), '" + \
                  qddbdInfo[
                      'ShopNo'] + "' + '_d' + RIGHT('0000000000' + CAST(( RIGHT(ISNULL(MAX([DJBH]), '0000000000'), 10) + 1 ) AS VARCHAR(20)), 10) as newid FROM LSXHD WHERE  DJBH LIKE '" + \
                  qddbdInfo['ShopNo'] + "_d%'"
            self.octerp2010.execute(sql)
            row = self.octerp2010.fetchone()
            NowTime = row[0]
            CreateTime = row[1]
            # shopNo_newid[qddbdInfo['ShopNo']] = row[2]
            newid = qddbdInfo['DeliveryType'] + "_" + row[2][3:]
            # print(qddbdInfo)

            qddbdDict = {
                'DJBH': newid,
                'RQ': CreateTime,
                'DJXZ': '0',
                'FPLX': '0',
                'DM1': qddbdInfo['ShopNo'],
                'DM1_1': '000',
                'DM2': qddbdInfo['DeliveryType'],
                'DM2_1': '000',
                'DM4': '888',
                'DM4_1': '001',
                'QDDM': '020',
                'QYDM': '000',
                'YGDM': '000',
                'SL': qddbdInfo['GoodsCount'],
                'JE': qddbdInfo['GoodsAmount'],
                'BZJE': qddbdInfo['GoodsAmount'],
                'YS': 1,
                'YSRQ': CreateTime,
                'SH': '1',
                'SHRQ': CreateTime,
                'ZDR': '系统管理员',
                'YSR': '系统管理员',
                'SHR': '系统管理员',
                'RQ_4': NowTime,
                'BZ': '电商系统自动生成的单据',
                'BYZD1': '3',
                'BYZD12': 1,
                '[DAYS]': 0,
                'CJ': 0,
                'TJ': 0,
                'XC': 0,
                'JZ': 0,
                'JS': 0,
                'SP': 0,
                'LL': 1,
                'LLR': 0,
                'ZS': 0
            }
            # 写入渠道调拨单
            # self.sqlserverInsert(qddbdDict, 'QDDBD', self.octerp2010)
            row = self.sqlite.execute(
                'select MAX(GoodsNo) GoodsNo, MAX(SpecValue1) SpecValue1, MAX(SpecValue2) SpecValue2, SUM(Quantity) Quantity, MAX(MarketPrice) MarketPrice, MAX(MarketPrice) MarketPrice, MAX(MarketPrice) MarketPrice, SUM(MarketPrice * Quantity) TotalSum from temp_delivery_item where DeliveryNo  IN ( SELECT DeliveryNo FROM temp_delivery WHERE ShopNo = :ShopNo and DeliveryType= :DeliveryType ) GROUP BY ProductNo',
                {'ShopNo': qddbdInfo['ShopNo'], 'DeliveryType': qddbdInfo['DeliveryType']})
            qddbdItemList = row.fetchall()
            index = 1
            for qddbdItemInfo in qddbdItemList:
                qddbdItemDict = {
                    'DJBH': newid,
                    'MIBH': index,
                    'SPDM': qddbdItemInfo['GoodsNo'],
                    'GG1DM': qddbdItemInfo['SpecValue1'],
                    'GG2DM': qddbdItemInfo['SpecValue2'],
                    'SL': qddbdItemInfo['Quantity'],
                    'CKJ': qddbdItemInfo['MarketPrice'],
                    'ZK': 1,
                    'DJ': qddbdItemInfo['MarketPrice'],
                    'DJ_1': qddbdItemInfo['MarketPrice'],
                    'DJ_2': 1,
                    'JE': qddbdItemInfo['TotalSum'],
                }
                # 写入渠道调拨明细单
                # self.sqlserverInsert(qddbdItemDict, 'QDDBDMX', self.octerp2010)
                index += 1
        # return shopNo_newid

    def createLsxhd(self):
        '''
        零售销货单
        明细可能会出现 除零 的异常
        :return:
        '''
        row = self.sqlite.execute(
            'select ShopNo, MAX(CreateTime) CreateTime, SUM(ReceivableAmount) ReceivableAmount, SUM(GoodsCount) GoodsCount, SUM(GoodsAmount) GoodsAmount from temp_delivery group by ShopNo')
        lsxhdList = row.fetchall()
        for lsxhdInfo in lsxhdList:
            # 如果不是自营的跳过
            if lsxhdInfo['ShopNo'][:3] != '021':
                continue
            # 创建零售销货单id
            sql = "SELECT CONVERT(DATE, GETDATE()) NowTime, CONVERT(DATE, '" + lsxhdInfo['CreateTime'] + "'), '" + \
                  lsxhdInfo[
                      'ShopNo'] + "' + '_d' + RIGHT('0000000000' + CAST(( RIGHT(ISNULL(MAX([DJBH]), '0000000000'), 10) + 1 ) AS VARCHAR(20)), 10) as newid FROM LSXHD WHERE  DJBH LIKE '" + \
                  lsxhdInfo['ShopNo'] + "_d%'"
            self.octerp2010.execute(sql)
            row = self.octerp2010.fetchone()
            NowTime = row[0]
            CreateTime = row[1]
            newid = row[2]

            lsxhdDict = {
                'DJBH': newid,
                'RQ': CreateTime,
                'DJXZ': '1',
                'FPLX': '1',
                'DM1': lsxhdInfo['ShopNo'],
                'DM1_1': '000',
                'DM2': lsxhdInfo['ShopNo'],
                'DM2_1': '000',
                'DM4': '000',
                'QDDM': '020',
                'YGDM': '000',
                'SL': lsxhdInfo['GoodsCount'],
                'JE': lsxhdInfo['GoodsAmount'],
                'JE_1': lsxhdInfo['ReceivableAmount'],
                'YS': 1,
                'YSRQ': CreateTime,
                'SH': '1',
                'SHRQ': CreateTime,
                'ZDR': '系统管理员',
                'YSR': '系统管理员',
                'SHR': '系统管理员',
                'RQ_4': NowTime,
                'BZ': '电商系统自动生成的单据',
                'BYZD1': '3',
                'BYZD12': 1,
                'BYZD13': 0,
                'HBHL': 1
            }

            # 写入零售销货单
            # self.sqlserverInsert(lsxhdDict, 'LSXHD', self.octerp2010)
            row = self.sqlite.execute(
                'select MAX(ID) ID, MAX(GoodsNo) GoodsNo, MAX(SpecValue1) SpecValue1, MAX(SpecValue2) SpecValue2, SUM(Quantity) Quantity, AVG(MarketPrice) MarketPrice, SUM(MarketPrice * Quantity) TotalSum from temp_delivery_item where DeliveryNo  IN ( SELECT DeliveryNo FROM temp_delivery WHERE ShopNo = :ShopNo) GROUP BY ProductNo',
                {'ShopNo': lsxhdInfo['ShopNo']})
            lsxhdItemList = row.fetchall()
            for lsxhdItemInfo in lsxhdItemList:
                lsxhdItemDict = {
                    'DJBH': newid,
                    'MIBH': lsxhdItemInfo['ID'],
                    'SPDM': lsxhdItemInfo['GoodsNo'],
                    'GG1DM': lsxhdItemInfo['SpecValue1'],
                    'GG2DM': lsxhdItemInfo['SpecValue2'],
                    'SL': lsxhdItemInfo['Quantity'],
                    'CKJ': lsxhdItemInfo['MarketPrice'],
                    'ZK': lsxhdItemInfo['TotalSum'] / lsxhdItemInfo['Quantity'] / lsxhdItemInfo['MarketPrice'],
                    'DJ': lsxhdItemInfo['TotalSum'] / lsxhdItemInfo['Quantity'],
                    'DJ_1': lsxhdItemInfo['MarketPrice'],
                    'DJ_2': lsxhdItemInfo['MarketPrice'],
                    'JE': lsxhdItemInfo['TotalSum'],
                    'BYZD9': lsxhdItemInfo['TotalSum']
                }
                # 写入零售销货明细单
                # self.sqlserverInsert(lsxhdItemDict, 'LSXHDMX', self.octerp2010)

    def createFsend(self):
        '''
        批发销货通知单
        明细可能会出现 除零 的异常
        :return:
        '''
        row = self.sqlite.execute(
            'select ShopNo, MAX(CreateTime) CreateTime, SUM(ReceivableAmount) ReceivableAmount, SUM(GoodsCount) GoodsCount, SUM(GoodsAmount) GoodsAmount from temp_delivery group by ShopNo')
        fsendList = row.fetchall()
        for fsendInfo in fsendList:
            # 如果是自营的跳过
            if fsendInfo['ShopNo'][:3] == '021':
                continue
            # 创建批发销货通知单id
            sql = "SELECT CONVERT(DATE, GETDATE()) NowTime, CONVERT(DATE, '" + fsendInfo['CreateTime'] + "'), '" + \
                  fsendInfo[
                      'ShopNo'] + "' + '_p' + RIGHT('0000000000' + CAST(( RIGHT(ISNULL(MAX([DJBH]), '0000000000'), 10) + 1 ) AS VARCHAR(20)), 10) as newid FROM FSEND WHERE  DJBH LIKE '" + \
                  fsendInfo['ShopNo'] + "_p%'"
            self.octerp2010.execute(sql)
            row = self.octerp2010.fetchone()
            NowTime = row[0]
            CreateTime = row[1]
            newid = row[2]
            shopNo = fsendInfo['ShopNo'][:-2]
            fsendDict = {
                'DJBH': newid,
                'RQ': CreateTime,
                'DJXZ': '0',
                'FPLX': '0',
                'DM1': shopNo,
                'DM1_1': '000',
                'DM2': '20',
                'DM2_1': '000',
                'DM3': shopNo,
                'DM3_1': '000',
                'DM4': '888',
                'DM4_1': '001',
                'QDDM': '000',
                'YGDM': '000',
                'SL': fsendInfo['GoodsCount'],
                'JE': fsendInfo['ReceivableAmount'],
                'JE_1': fsendInfo['ReceivableAmount'],
                'YS': '0',
                'YSRQ': '',
                'JZ': '0',
                'JZRQ': '',
                'ZDR': '系统管理员',
                'YSR': '',
                'SHR': '',
                'RQ_4': NowTime,
                'BZ': '电商系统自动生成的单据',
                'BYZD1': '3',
                'BYZD12': 1,
            }

            # 写入批发销货通知单
            # self.sqlserverInsert(fsendDict, 'FSEND', self.octerp2010)
            row = self.sqlite.execute(
                'select MAX(ID) ID, MAX(GoodsNo) GoodsNo, MAX(SpecValue1) SpecValue1, MAX(SpecValue2) SpecValue2, SUM(Quantity) Quantity, AVG(MarketPrice) MarketPrice, SUM(MarketPrice * Quantity) TotalSum from temp_delivery_item where DeliveryNo  IN ( SELECT DeliveryNo FROM temp_delivery WHERE ShopNo = :ShopNo) GROUP BY ProductNo',
                {'ShopNo': fsendInfo['ShopNo']})
            fsendItemList = row.fetchall()
            for fsendItemInfo in fsendItemList:
                fsendItemDict = {
                    'DJBH': newid,
                    'MIBH': fsendItemInfo['ID'],
                    'SPDM': fsendItemInfo['GoodsNo'],
                    'GG1DM': fsendItemInfo['SpecValue1'],
                    'GG2DM': fsendItemInfo['SpecValue2'],
                    'SL': fsendItemInfo['Quantity'],
                    'CKJ': fsendItemInfo['MarketPrice'],
                    'ZK': fsendItemInfo['TotalSum'] / fsendItemInfo['Quantity'] / fsendItemInfo['MarketPrice'],
                    'DJ': fsendItemInfo['TotalSum'] / fsendItemInfo['Quantity'],
                    'DJ_1': fsendItemInfo['MarketPrice'],
                    'DJ_2': 1,
                    'JE': fsendItemInfo['TotalSum']
                }
                # 写入批发销货通知单明细
                # self.sqlserverInsert(fsendItemDict, 'FSENDMX', self.octerp2010)

    def createSpkcb(self):
        '''
        库存操作
        :return:
        '''
        '''
        初始化库存记录
        '''
        row = self.sqlite.execute(
            'select ShopNo, MAX(CreateTime) CreateTime, SUM(ReceivableAmount) ReceivableAmount, SUM(GoodsCount) GoodsCount, SUM(GoodsAmount) GoodsAmount from temp_delivery group by ShopNo')
        spkcbList = row.fetchall()
        for spkcbInfo in spkcbList:
            shopNo = spkcbList['ShopNo']
            row = self.sqlite.execute(
                'select GoodsNo, SpecValue1, SpecValue2 from temp_deliveryitem where DeliveryNo in (select DeliveryNo from temp_delivery where shop_no= ? group by GoodsNo, SpecValue1, SpecValue2', shopNo)
            spkcbItemList = row.fetchall()
            for item in spkcbItemList:
                row = self.octerp2010.execute("SELECT * from SPKCB where SPDB = %s AND GG1DM = %s AND GG2DM = %s AND CKDM = '20' AND KWDM = '000'", (item['GoodsNo'], item['SpecValue1'], item['SpecValue2']))
                temp = row.fetchall()
                if temp:
                    continue
                itemDict = {
                    'SPDM': item['GoodsNo'],
                    'GG1DM':item['SpecValue1'],
                    'GG2DM':item['SpecValue2'],
                    'CKDM':'20',
                    'KWDM':'000',
                    'SL':0,
                    'SL1':0,
                    'SL2':0,
                    'SL3':0,
                    'SL4':0,
                    'SL5':0,
                    'SL6':0,
                    'SL7':0,
                    'SL8':0,
                    'SL9':0,
                    'SL10':0,
                    'YDSL':0
                }
                # 初始化库存记录
                # self.sqlserverInsert(itemDict, 'SPKCB', self.octerp2010)

    def createHistory(self):
        '''
        记录历史单号
        :return:
        '''
        row = self.sqlite.execute(
            'select DeliveryNo, OrderNo from temp_delivery')
        historyList = row.fetchall()
        print(historyList)
        # 写入
        # self.sqlserverInsertAll(historyList, 'API_ReceiveDeliveryHistory', self.octerp2010)

    def createLog(self, id, msg, name = 'ReceiveDeliverySyncMessage'):
        '''
        记录错误日志
        :return:
        '''
        # 发送微信通知

        # 记录数据库日志
        item = {
            'Procedure' : name,
            'RowNumber' : id,
            'ErrorInfo' : msg
        }
        self.sqlserverInsert(item, 'API_JobEventLog', self.octerp2010)

    def sqlserverInsert(self, in_dict, table, cursor):
        '''
        sqlserver 写入操作
        把字典写入到表中
        :param in_dict: 要写入的字典
        :param table: 表名
        :param cursor: 指针
        :return:
        '''
        ls = [(k, in_dict[k]) for k in in_dict if in_dict[k]]
        sql = 'INSERT %s (' % table + ','.join([i[0] for i in ls]) + \
              ') VALUES (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        # print(sql)
        row = cursor.execute(sql)
        return row

    def sqlserverInsertAll(self, in_list, table, cursor):
        '''
        sqlserver 写入操作
        把字典列表写入到表中
        :param in_dict: 要写入的字典组成的列表
        :param table: 表名
        :param cursor: 指针
        :return:
        '''
        in_dict = in_list[0]
        ls = [(k, in_dict[k]) for k in in_dict]
        sql = 'INSERT %s (' % table + ','.join([i[0] for i in ls]) + \
              ') VALUES '
        values = ''
        for item in in_list:
            temp = [(k, in_dict[k]) for k in in_dict]
            values += '(' + ', '.join([' % r' % i[1] for i in temp]) + '),'
        sql += values[:-1] + ';'
        row = cursor.execute(sql)
        return row

    def insert(self, in_dict, table, cursor):
        '''
        把字典写入到表中 for sqlite
        :key 会自动对应到字典中的key
        :param in_dict: 字典
        :param table: 表名
        :param cursor: 指针
        :return:
        '''
        keyList = in_dict.keys()
        keyListFlags = [':' + key for key in keyList]
        keyStr = ','.join(keyList)
        keyStrFlags = ','.join(keyListFlags)
        sql = 'insert into %s (%s) values (%s)' % (table, keyStr, keyStrFlags)
        row = cursor.execute(sql, in_dict)
        return row

    def __del__(self):
        '''
        销毁时关闭指针
        :return:
        '''
        self.ssbConn.close()
        self.octerpConn.close()
        self.sqliteConn.close()


if __name__ == '__main__':
    obj = ReceiveDeliverySyncMessage()
    obj.run()
