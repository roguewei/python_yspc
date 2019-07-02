from urllib import request
import re


class SpiderLol:
    root_url = 'http://yctanlu.com/'

    root_pattern = '<span class="item-title">([\s\S]*?)</span>'
    css_pattern = '<link rel="stylesheet" type="text/css" href="css/(\w+.css?)">'
    js_pattern = '<script type="text/javascript" src="http://yctanlu.com/js/([\s\S]*?.js)"></script>'
    img_pattern = '<img (alt="[\w\W]+?")? src="(http://yctanlu.com/upload/\w+/\d*?.(png|jpg))">'
    html_pattern = '<a href="(http://yctanlu.com/\w+?)"[\s\S]*?>[\w\W]+?</a>'

    def __get__content(self, url, encoding):
        r = request.urlopen(url)
        htmls = r.read()
        htmls = str(htmls, encoding=encoding)
        return htmls

    def __analysis(self, htmls, pattern):
        root_html = re.findall(pattern, htmls)
        return root_html

    def __writetofile(self, filename, contents, encoding):
        f1 = open('files/' + filename, 'w', encoding=encoding)
        f1.write(contents)
        f1.close()

    def __writeimg(self, fileurls, encoding):
        a = []
        for fileurl in fileurls:
            a.append(fileurl[1]+'\n')
        imgurl = ''.join(a)
        f1 = open('files/imgfile.txt', 'w', encoding=encoding)
        f1.write(imgurl)
        f1.close()

    def action(self, url, encoding):
        htmls = self.__get__content(url, encoding)
        # 写入主HTML页面
        self.__writetofile('index.html', htmls, 'utf-8')
        # 抽取css文件
        css_htmls = self.__analysis(htmls, self.css_pattern)
        for filename in css_htmls:
            filecontent = self.__get__content(self.root_url + 'css/' + filename, 'utf-8')
            self.__writetofile(filename, filecontent, encoding='utf-8')

        # 抽取js文件
        js_htmls = self.__analysis(htmls, self.js_pattern)
        for filename in js_htmls:
            filecontent = self.__get__content(self.root_url + 'js/' + filename, 'utf-8')
            self.__writetofile(filename, filecontent, encoding='utf-8')

        # 抽取图片文件
        img_htmls = self.__analysis(htmls, self.img_pattern)
        self.__writeimg(img_htmls, 'utf-8')

        html_htmls = self.__analysis(htmls, self.html_pattern)
        # for html in html_htmls:
        #     pass


spiderlol = SpiderLol()
spiderlol.action(spiderlol.root_url, 'utf-8')
# spiderlol.action()
