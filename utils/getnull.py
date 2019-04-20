import json

def main():
    '''获取爬取景点中名称缺失的数据并写入文件'''
    recap = open('recapurl.json', 'w', encoding='utf-8')
    with open('../tuniu/spot.json', 'r', encoding='utf8') as f:
        for line in f:
            spot = json.loads(line)
            if spot['name'] == None:
                dic = {}
                dic['url'] = 'http://www.tuniu.com/' + spot['id'] + '/guide-0-0/'
                dic['nation'] = spot['nation']
                dic['city'] = spot['city']
                l = json.dumps(dic, ensure_ascii=False) + "\n"
                recap.write(l)
    recap.close()

if __name__ == '__main__':
    main()