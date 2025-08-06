# 2023-10-20
import requests
from bs4 import BeautifulSoup
import xlwt
import datetime
import os
import config


# 为热点话题下的帖子创建一个类
class Post:
    # 一条帖子应该包含：微博id/特殊标签/发帖人/发帖时间与标记/发帖来源/发帖正文/转发数/评论数/点赞数
    # 特殊标签：顶置、热门  事件与标记：如 今天 18:03 转赞人数超过100
    def __int__(self, mid, sp_label, uid, poster, time, sp_mark, origin, text, retweets_num, comments_num, likes_num):
        self.mid = mid
        self.sp_label = sp_label
        self.uid = uid
        self.poster = poster
        self.time = time
        self.origin = origin
        self.text = text
        self.retweet_num = retweets_num
        self.comments_num = comments_num
        self.likes_num = likes_num


def dateList(begin_date, end_date):
    ord_begin = datetime.date.toordinal(begin_date)
    ord_end = datetime.date.toordinal(end_date)
    date_list = []
    for date in range(int(ord_begin), int(ord_end) + 1):
        date_list.append(datetime.date.fromordinal(date))

    return date_list


headers = {
    "User-Agent": config.config['User-Agent'],
    "Cookie": config.config['json_cookie']
}


class Spider:
    def __init__(self, ques, beg_date, end_date, file_path=None):
        self.url = f"https://s.weibo.com/weibo?q={ques}&typeall=1&suball=1&timescope=custom"
        # "%3A{2023-10-29}%3A{2023-10-29}&{page=1}")
        # 初始化表格文件
        self.xls = xlwt.Workbook()
        # 确定起始日期和结束日期
        self.begin_date = beg_date
        self.end_date = end_date
        self.date_list = dateList(self.begin_date, self.end_date)
        self.file_path = f"Sina_Topic_From_{self.begin_date}_To_{self.end_date}_{ques}.xls"
        if file_path is not None:
            self.file_path = file_path

    def run(self):
        # 按日期跨度建立sheet表
        for date in self.date_list:
            print(date)
            # 初始化当前sheet表
            sheet1 = self.xls.add_sheet(sheetname=f"{date}")
            table_titles = ['微博id', '特殊标签', '发帖人id', '发帖人昵称', '发帖时间与标记', '发帖来源', '发帖正文',
                            '转发数','评论数', '点赞数']
            for i in range(len(table_titles)):
                sheet1.write(0, i, table_titles[i])

            url_for_page = self.url + f"%3A{date}%3A{date}"
            response_for_page = requests.get(url=url_for_page, headers=headers)
            soup_for_page = BeautifulSoup(response_for_page.text, 'html.parser')
            tmp_soup = soup_for_page.find('ul', attrs={"node-type": "feed_list_page_morelist"})
            try:
                page_limit = len(tmp_soup.find_all('li'))
            except:
                page_limit = 1

            row = 0
            for page in range(1, page_limit + 1):
                main_url = url_for_page + f"&page={page}"

                main_response = requests.get(url=main_url, headers=headers)
                soup = BeautifulSoup(main_response.text, 'html.parser')

                cards_list = soup.find_all('div', attrs={"action-type": "feed_list_item"})

                # 每单条帖子都将数据存入实例类中

                for card in cards_list:
                    row += 1
                    column = 0
                    # 创建实例
                    post = Post()

                    # 获取微博id
                    post.mid = card.get('mid')
                    sheet1.write(row, column, post.mid)
                    column += 1
                    # print(post.mid)

                    # 筛选特殊标签
                    title = card.find('h4', attrs={"class": "title"})
                    try:
                        sp_mark = title.find('a')
                        post.sp_mark = sp_mark.text
                    except:
                        post.sp_mark = ''
                    sheet1.write(row, column, post.sp_mark)
                    column += 1

                    # 筛选发帖人
                    name = card.find('a', class_="name")
                    post.poster = name.text
                    post.uid = name.get('href')[12:22]
                    sheet1.write(row, column, post.uid)
                    column += 1
                    sheet1.write(row, column, post.poster)
                    column += 1

                    # 筛选发帖时间与标记
                    mid = card.find('div', class_="from")
                    time = mid.find('a')
                    post.time = time.text.strip()
                    sheet1.write(row, column, post.time)
                    column += 1

                    # 筛选发帖来源
                    mid = card.find('div', attrs={"class": "from"})
                    origin = mid.find('a', attrs={"rel": "nofollow"})
                    try:
                        post.origin = origin.text
                    except:
                        post.origin = ''
                    sheet1.write(row, column, post.origin)
                    column += 1

                    # 筛选发帖正文 需要格式化处理开头空格
                    content = card.find('p', attrs={"node-type": "feed_list_content_full", "class": "txt"})
                    if content is None:
                        content = card.find('p', attrs={"node-type": "feed_list_content", "class": "txt"})
                    post.text = content.text
                    post.text = post.text.strip()
                    post.text = post.text.strip('\u200b')
                    post.text = post.text.strip('收起d')
                    sheet1.write(row, column, post.text)
                    column += 1

                    # 筛选帖子转发评论点赞数量
                    act = card.find(name='div', attrs={"class": "card-act"})
                    act_list = act.text.split('\n')
                    # 3 4 8
                    post.retweet_num = act_list[3].strip()
                    post.comments_num = act_list[4].strip()
                    post.likes_num = act_list[8].strip()
                    sheet1.write(row, column, post.retweet_num)
                    column += 1
                    sheet1.write(row, column, post.comments_num)
                    column += 1
                    sheet1.write(row, column, post.likes_num)
                    column += 1

        if os.path.exists(self.file_path) is True:
            os.remove(self.file_path)
        self.xls.save(self.file_path)
        print('话题爬取成功')
