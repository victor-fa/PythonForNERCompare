# coding=utf-8
import csv
import codecs
import json
import sys
import urllib2
import thread
import time

# 内容 开始
fromFile = 'text.txt'   # 需要解析的文件名【必选】
toFile = 'test.csv'     # 的csv文件【必选】
keyWord = '我想听一首歌，叫***'    # 关键词【必选，替换关键词默认为三个'*'，即'***'】
# 内容 结束

reload(sys)
sys.setdefaultencoding('utf8')  # 指定
datas = [['song', u'语句', 'NER', u'比对']]     # 初始化数据
url='http://aliyun-sh11.chewrobot.com:58200/predict'    # NER 请求地址
header_dict = {"Content-Type": "application/json"}      # 请求头
lineNumber = 0
finishCount = 0

# 直接获取所有行数
fCount = open('./file/' + fromFile, 'r')
count = fCount.read()
lineNumber = len(count.splitlines())
fCount.close()

# 读text.txt
f = open('./file/' + fromFile, 'r')
line = f.readline()
line = line[:-1]

while line:
    try:
        tempData = []
        if line.strip() == "":
            continue
        str = line.decode('gbk')
        str = str.replace("'", '"')
        strJson = json.loads(str)
        if not strJson.has_key('title'):
            print('error')
            continue
        result = strJson["title"]

        execKeyWord = keyWord.replace('***', result)

        textmod = {"sentence": execKeyWord}
        textmod = json.dumps(textmod)
        req = urllib2.Request(url = url, data = textmod, headers = header_dict)
        res = urllib2.urlopen(req)
        res = res.read()
        res = json.loads(res)

        if res["chunks"]:
            nerResult = res["chunks"][0]['chunks']
        else:
            nerResult = '[]'

        # 组装数组
        tempData.append(result)
        tempData.append(execKeyWord)
        tempData.append(nerResult)    # NER结果
        tempData.append(result == nerResult)
        datas.append(tempData)

        finishCount += 1
        # 打印出目前执行效果
        print('完成情况： ' + '%d' % finishCount + '/' + '%d' % lineNumber + '  ' + nerResult)

        line = f.readline()
        line = line[:-1]  # 去掉换行符
    except OSError as err:
        print("OS error: {0}".format(err))
    except (ValueError) as Argument:
        print("Could not convert data to an integer.", Argument)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

f.close()

# 写入csv内容
fcsv = codecs.open('./file/' + toFile, 'wb', "utf8")
fcsv.write(codecs.BOM_UTF8) # 防止乱码
writer = csv.writer(fcsv)
writer.writerows(datas)
fcsv.close()

def main():
    # 读取csv内容
    with open('./file/' + toFile, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row
    pass

# main()