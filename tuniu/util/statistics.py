import json
import matplotlib.pyplot as plt

def plot(length, xlabel, ylabel):
    x = []
    count = []
    for i in sorted(set(length)):
        x.append(i)
        count.append(length.count(i))
    plt.plot(x, count)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def main():
    desc_length = []
    addr_length = []
    with open('./combine.json', 'r', encoding='utf8') as f:
        for line in f:
            spot = json.loads(line)
            if spot['desc'] != None:
                desc_length.append(len(spot['desc']))
            if spot['addr'] != None:
                addr_length.append(len(spot['addr']))
    plot(desc_length, 'Length of description', 'Num of spot')
    plot(addr_length, 'Length of address', 'Num of spot')

if __name__ == '__main__':
    main()