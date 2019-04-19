import json
import matplotlib.pyplot as plt

def plot(length, xlabel, ylabel):
    x = []
    count = []
    for i in sorted(set(length)):
        x.append(i)
        count.append(length.count(i))
    plt.bar(x, count)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def main():
    # Spot中字符串类型的属性有：id / name / nation / city / desc / open_time / rec_play_time / 
    # {"id": "g2085065", "name": "Clock Tower Square", "nation": "不丹", "city": "廷布", "desc": null, "addr": null, "open_time": null, "traffic": {}, "rec_play_time": null, "site_dist": {"must": {}, "near": {}}}
    # {"id": "g4395430", "name": "都楚拉隘口", "nation": "不丹", "city": "廷布", "desc": "都楚拉隘口（Dochula Pass）是从Thimpu到Punakha在不丹境内积雪覆盖的喜马拉雅山上的山口，海拔约 3150 公尺，此处有第四世王的皇后发愿为国王及国家祈福而建的 108 座佛塔群Bhutanese Stupas，称为凯旋佛塔（Druk Wangyal Chorten）。", "addr": "Dochula,Bhutan", "open_time": "\r\n                            ", "traffic": {}, "rec_play_time": null, "site_dist": {"must": {"g2096355": "约187米", "g36732": "约9.8公里"}, "near": {"g2096355": "约187米", "g36732": "约9.8公里"}}}
    # {"id": "g2092545", "name": "Dechencholing Palace", "nation": "不丹", "city": "廷布", "desc": null, "addr": null, "open_time": null, "traffic": {}, "rec_play_time": null, "site_dist": {"must": {}, "near": {}}}
    # {"id": "g3219034", "name": "不丹国家邮政总局", "nation": "不丹", "city": "廷布", "desc": "国家邮政总局（General Postal Office）,不丹是世界上鼎鼎有名的\"邮票大国\"，以至于国家邮政总局都成为不丹的必游景点之一。1962年人类*枚会唱歌的唱片邮票就诞生在不丹。至今，不丹在邮票设计、印制和材质的多样性上，一直处于*地位，并多次在国际邮展上获奖。\n不丹的邮票内容非常丰富多彩，除了表现本国宗教、民俗、动植物、王室庆典等题材之外，还发行国际球星、欧洲名画、各国风光等题材的邮品。发行富有国际竞争力的特种邮票以成为不丹赚取外汇的主要途径之一。目前，不丹仍然保持着使用特殊材料印刷邮票*多的世界纪录。\n在这里你可以尝试个人头像邮票，或购买世界上*的CD邮票，还可以做3D邮票。不丹的国际邮政编码为999090，但并未采用。在实际操作中，从中国大陆邮寄到不丹的国际邮件，需要用不丹当地使用的语言来写清详细城市和地址。可以不用填写不丹邮政编码，也一样可以递送到不丹。", "addr": "Thimphu 0001, Bhutan", "open_time": "周一至周五：09:00-16:00；周六：09:00-13:00；周日歇业。", "traffic": {}, "rec_play_time": null, "site_dist": {"must": {"g2062675": "约375米", "g2085065": "约401米"}, "near": {"g2062675": "约375米", "g2085065": "约401米"}}}
    # {"id": "g3219024", "name": "不丹传统医药研究所", "nation": "不丹", "city": "廷布", "desc": "不丹传统医药研究所位于不丹国家图书馆和传统艺术中心上方的小山顶。它建于1967年，当时的国王下令给不丹卫生部，下令建立一座传统医药所来保存不丹传统文化。\n1979年搬迁到廷布的现址，改名为国家土着医院（National Indigenous Hospital），1988年更名为国家传统医学研究所（Institute of Traditional Medicine Services ），简称ITMS，然后于1998年升级为传统医学服务研究所（Institute of Traditional Medical Services），简称ITMS。它于1968年6月22日对公众开放，提供传统医药服务，培训医生，并对传统医学草本植物展开研究。 ", "addr": "Sherzhong Lam, Thimphu, Bhutan", "open_time": "周一至周五：09;00-15:00；周六 ：09:00-13:00。", "traffic": {}, "rec_play_time": null, "site_dist": {"must": {"g2106814": "约356米", "g2106376": "约358米"}, "near": {"g2106814": "约356米", "g2106376": "约358米"}}}
    # id VARCHAR(10)
    # name VARCHAR
    # nation VARCHAR
    # city VARCHAR
    # description TEXT
    # open_time VARCHAR
    # rec_play_time VARCHAR
    # addr VARCHAR
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

    # Review中字符串类型的属性有：spot_id / nickname / spot_name / desc
    # {"spot_id": "g1807087", "spot_nation_rate": 4.0, "nickname": "wv-china2004", "spot_name": "独立海滩", "review_time": "2011-11-02 09:27:38", "rate": 4, "desc": "独立海滩非常的静谧，在海滩上可以看到很多建筑和高楼，这里的旅游度假区算是比较火的。", "upvote": 0, "num_reply": 0}
    # {"spot_id": "g26689", "spot_nation_rate": 4.0, "nickname": "阿米*圣1991", "spot_name": "胜利海滩", "review_time": "2011-11-02 08:47:25", "rate": 4, "desc": "很多人在这里捕鱼，会有淡淡的腥味，不过这里的景色真是让人赏心悦目。", "upvote": 0, "num_reply": 0}
    # {"spot_id": "g26690", "spot_nation_rate": 4.0, "nickname": "ES一边炒菜一边1988", "spot_name": "索卡海滩", "review_time": "2011-11-02 06:14:47", "rate": 4, "desc": "周围有一家五星级的酒店，而且这里是被他承包了，管理的非常好，风景也很优美。", "upvote": 0, "num_reply": 0}
    # {"spot_id": "g26689", "spot_nation_rate": 4.0, "nickname": "圣徒卡卡1990", "spot_name": "胜利海滩", "review_time": "2011-07-27 09:35:44", "rate": 4, "desc": "这里是观看日落的好地方，美丽的晚霞伴着和煦的微风，一切都很生机盎然。", "upvote": 98, "num_reply": 0}
    # {"spot_id": "g26689", "spot_nation_rate": 4.0, "nickname": "周宏翔2009", "spot_name": "胜利海滩", "review_time": "2011-06-13 00:43:29", "rate": 4, "desc": "那里的游客很少，还有几个外国人在哪里晒太阳，而且还有几个小孩子在那里玩水。", "upvote": 0, "num_reply": 0}
    # spot_id VARCHAR(10)
    # spot_nation_rate FLOAT
    # nickname VARCHAR(20)
    # spot_name VARCHAR(30)
    # review_time DATETIME
    # rate TINYINT
    # desc TEXT
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
    

if __name__ == '__main__':
    main()