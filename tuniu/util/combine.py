import json

def main():
    f_combine = open('combine.json', 'w', encoding='utf-8')
    with open('../recap.json', 'r', encoding='utf-8') as f_recap:
        for line in f_recap:
            f_combine.write(line)
    with open('../spot.json', 'r', encoding='utf8') as f_spot:
        for line in f_spot:
            spot = json.loads(line)
            if spot['name'] != None:
                f_combine.write(line)
    f_combine.close()

if __name__ == '__main__':
    main()