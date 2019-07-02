# 引入Python内置的http操作库
from urllib import request
# 引入re正则表达式包
import re

# 爬虫框架可以使用BeautifulSoup，Scrapy
class Spider:
    # 需要爬取的网页地址
    url = 'https://www.huya.com/g/lol'
    root_pattern = '<span class="txt">([\s\S]*?</span>[\s]*<span class="num">[\s\S]*?</span>[\s]*)</span>'
    name_pattern = '<i class="nick" title="[\s\S]*?">([\s\S]*?)</i>'
    num_pattern = '<span class="num">[\s]*<i class="num-icon"></i>[\s]*<i class="js-num">([\s\S]*?)</i></span>'


    # 定义私有方法（获取网页内容）
    def __fetch__content(self):
        # request.urlopen用以发送http请求
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    # 定义私有方法（分析网页内容）
    def __analysis(self, htmls):

        # 根据正则获取爬取页面的需要数据
        root_html = re.findall(Spider.root_pattern, htmls)

        anchors = []
        for x in root_html:
            root_name = re.findall(Spider.name_pattern, x)
            root_num = re.findall(Spider.num_pattern, x)
            anchor = {'name': root_name, 'num': root_num}
            anchors.append(anchor)

        return anchors

    # 精简爬取得数据
    def __refine(self, anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'num': anchor['num'][0]
        }
        return map(l, anchors)

    # 排序
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['num'])
        number = float(r[0])
        if '万' in anchor['num']:
            number *= 10000
        return number

    # 展示数据
    def __show(self, anchors):
        # for anchor in anchors:
        #     print(anchor['name'] + '-------' + anchor['num'])
        for rank in range(0, len(anchors)):
            print('rank: ' + str(rank + 1) + '---' + anchors[rank]['name'] + '---' + anchors[rank]['num'])

    def go(self):
        hails = self.__fetch__content()
        anchors = self.__analysis(hails)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
