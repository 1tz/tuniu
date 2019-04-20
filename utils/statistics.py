import json
import matplotlib.pyplot as plt

def plot(length, xlabel, ylabel):
    '''画出柱状图
    :param length: 字符串长度列表
    :param xlabel: x轴标签
    :param ylabel: y轴标签
    :return: None
    '''
    x = []
    count = []
    for i in sorted(set(length)):
        x.append(i)
        count.append(length.count(i))
    plt.bar(x, count)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def show_spot_statistics():
    '''显示Spot字符类型数据统计信息
    Spot示例
    {
        "id": "g3219034",
        "name": "不丹国家邮政总局",
        "nation": "不丹",
        "city": "廷布",
        "desc": "国家邮政总局（General Postal Office）,不丹是世界上鼎鼎有名的"邮票大国"...",
        "addr": "Thimphu 0001, Bhutan",
        "open_time": "周一至周五：09:00-16:00；周六：09:00-13:00；周日歇业。",
        "traffic": {},
        "rec_play_time": null,
        "site_dist": {
            "must": {
                "g2062675": "约375米",
                "g2085065": "约401米"
            },
            "near": {
                "g2062675": "约375米",
                "g2085065": "约401米"
            }
        }
    }
    '''
    id_length = []
    name_length = []
    city_length = []
    nation_length = []
    desc_length = []
    addr_length = []
    time_length = []
    rec_time_length = []
    with open('../../result/combine.json', 'r', encoding='utf8') as f:
        for line in f:
            spot = json.loads(line)
            if spot['id'] != None:
                id_length.append(len(spot['id']))
            if spot['name'] != None:
                name_length.append(len(spot['name']))
            if spot['nation'] != None:
                nation_length.append(len(spot['nation']))
            if spot['city'] != None:
                city_length.append(len(spot['city']))
            if spot['desc'] != None:
                desc_length.append(len(spot['desc']))
            if spot['rec_play_time'] != None:
                rec_time_length.append(len(spot['rec_play_time']))
            if spot['addr'] != None:
                addr_length.append(len(spot['addr']))
            if spot['open_time'] != None:
                time_length.append(len(spot['open_time']))
    plot(id_length, 'Length of id', 'Num of spot')
    plot(name_length, 'Length of name', 'Num of spot')
    plot(city_length, 'Length of city', 'Num of spot')
    plot(nation_length, 'Length of nation', 'Num of spot')
    plot(desc_length, 'Length of description', 'Num of spot')
    plot(addr_length, 'Length of address', 'Num of spot')
    plot(time_length, 'Length of open time', 'Num of spot')
    plot(rec_time_length, 'Length of recommend time', 'Num of spot')

def show_review_statistics():
    '''显示Review字符类型数据统计信息
    Review示例
    {
        "spot_id": "g1807087",
        "spot_nation_rate": 4.0,
        "nickname": "wv-china2004",
        "spot_name": "独立海滩",
        "review_time": "2011-11-02 09:27:38",
        "rate": 4,
        "desc": "独立海滩非常的静谧，在海滩上可以看到很多建筑和高楼，这里的旅游度假区算是比较火的。",
        "upvote": 0,
        "num_reply": 0
    }
    '''
    id_length = []
    nickname_length = []
    spot_name_length = []
    desc_length = []
    with open('../../result/review.json', 'r', encoding='utf8') as f:
        for line in f:
            review = json.loads(line)
            if review['spot_id'] != None:
                id_length.append(len(review['spot_id']))
            if review['nickname'] != None:
                nickname_length.append(len(review['nickname']))
            if review['spot_name'] != None:
                spot_name_length.append(len(review['spot_name']))
            if review['desc'] != None:
                desc_length.append(len(review['desc']))
    plot(id_length, 'Length of id', 'Num of review')
    plot(nickname_length, 'Length of nickname', 'Num of review')
    plot(spot_name_length, 'Length of spot_name', 'Num of review')
    plot(desc_length, 'Length of description', 'Num of review')

def main():
    show_review_statistics()
    show_spot_statistics()

if __name__ == '__main__':
    main()