# -*- coding: utf-8 -*-
#!/usr/bin/python3
import json
import pymysql


def insert_review():
    '''向数据库中插入评论信息'''
    # 连接数据库
    db = pymysql.connect("ip", "user", "passwd", "tuniu", charset='utf8')
    cursor = db.cursor()

    # 删除表
    sql = """DROP TABLE IF EXISTS tuniu.REVIEW"""
    cursor.execute(sql)

    # 创建表
    sql = """CREATE TABLE REVIEW (
             SpotID VARCHAR(10),
             SpotNationRate DECIMAL(2,1),
             NickName VARCHAR(20),
             SpotName VARCHAR(30),
             ReviewTime DATETIME,
             Rate INT(1),
             Description TEXT,
             Upvote INT(3),
             NumReply INT(3))
             """
    cursor.execute(sql)
    
    # 每1000条执行一次SQL语句，而不是每条执行一次。这样效率更高
    sql = '''INSERT INTO tuniu.REVIEW(SpotID, SpotNationRate, \
             NickName, SpotName, ReviewTime, Rate, Description, Upvote, NumReply) \
             VALUES '''
    with open('../result/review.json', 'r', encoding='utf8') as f_review:
        values = ''
        for i, line in enumerate(f_review):
            review = json.loads(line)
            values += '''('{}', {}, '{}', '{}', '{}', {}, '{}', {}, {})'''.format(
                review['spot_id'],
                review['spot_nation_rate'],
                review['nickname'].strip().replace("'","''"),
                review['spot_name'].replace("'","''"),
                review['review_time'],
                review['rate'],
                review['desc'].strip().replace("'","''"),
                review['upvote'],
                review['num_reply'])
            if i % 1000 != 0:
                values += ', '
            else:
                try:
                    cursor.execute(sql + values)
                    db.commit()
                except:
                    db.rollback()
                values = ''
                print(i)
        values = values[:-2]
        cursor.execute(sql + values)
        db.commit()
    db.close()

def insert_spot():
    '''向数据库中插入景点信息'''
    # 连接数据库
    db = pymysql.connect("ip", "user", "passwd", "tuniu", charset='utf8')
    cursor = db.cursor()

    # 删除表
    sql = """DROP TABLE IF EXISTS tuniu.SPOT"""
    cursor.execute(sql)

    # 创建表
    sql = """CREATE TABLE SPOT (
             ID VARCHAR(10),
             Name VARCHAR(100),
             Nation VARCHAR(10),
             City VARCHAR(12),
             Description TEXT,
             Address VARCHAR(200),
             OpeningTimes TEXT,
             RecPlayTime VARCHAR(10),
             PRIMARY KEY (ID)
             )"""
    cursor.execute(sql)

    sql = '''INSERT INTO tuniu.SPOT(ID, \
             Name, Nation, City, Description, Address, \
             OpeningTimes, RecPlayTime) \
             VALUES '''
    
    # 每1000条执行一次SQL语句，而不是每条执行一次，会导致速度慢
    with open('../result/combine.json', 'r', encoding='utf8') as f_spot:
        values = ''
        for i, line in enumerate(f_spot):
            spot = json.loads(line)
            values += '''('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(
                str(spot['id']),
                str(spot['name']).replace("\\","").replace("'","''"),
                str(spot['nation']),
                str(spot['city']),
                str(spot['desc']).strip().replace("\\","").replace("'","''"),
                str(spot['addr']).strip().replace("\\","").replace("'","''"),
                str(spot['open_time']).strip().replace("\\","").replace("'","''"),
                str(spot['rec_play_time'])).replace("\\","").strip()
            if i % 1000 != 0:
                values += ', '
            else:
                try:
                    cursor.execute(sql + values)
                    db.commit()
                except:
                    print(sql + values)
                    db.rollback()
                values = ''
                print(i)
        values = values[:-2]
        cursor.execute(sql + values)
        db.commit()
    db.close()

def main():
    insert_review()
    insert_spot()

if __name__ == '__main__':
    main()