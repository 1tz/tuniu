import os
import json
import shutil

def main():
    '''合并两次爬取的结果'''
    if not os.path.exists('../result'):
        os.mkdir('../result')
    f_combine = open('../result/combine.json', 'w', encoding='utf-8')
    with open('../tuniu/recap.json', 'r', encoding='utf-8') as f_recap:
        for line in f_recap:
            f_combine.write(line)
    with open('../tuniu/spot.json', 'r', encoding='utf8') as f_spot:
        for line in f_spot:
            spot = json.loads(line)
            if spot['name'] != None:
                f_combine.write(line)
    f_combine.close()
    # 将review复制到result中
    shutil.copyfile('../tuniu/review.json','../result/review.json')

if __name__ == '__main__':
    main()