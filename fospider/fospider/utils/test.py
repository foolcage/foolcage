import datetime


def sql(the_date):
    return '''
    ALTER TABLE `message_{}` ADD COLUMN(
              state int(10) NOT NULL DEFAULT '0' COMMENT '货源状态',
              cargoTypeName varchar(50) DEFAULT NULL COMMENT '货源类型',
              intervalLoad varchar(50) DEFAULT NULL COMMENT '重量范围',
              vehicleLengthNames varchar(128) DEFAULT NULL COMMENT '车长',
              lessThanCarload varchar(64) DEFAULT NULL COMMENT '车辆载重',
              vehicleTypeName varchar(64) DEFAULT NULL COMMENT '车型',
              activity varchar(64) DEFAULT NULL COMMENT '活动',
              contactPerson varchar(32) DEFAULT NULL COMMENT '联系人姓名');
    '''.format(the_date)


base = datetime.datetime.strptime("2017-04-01", "%Y-%m-%d")
date_list = [base + datetime.timedelta(days=x) for x in range(0, 41)]

for the_date in date_list:
    print(sql(the_date.strftime("%Y-%m-%d")))
