from aip import AipNlp
import xlrd
import xlwt
import time
from tqdm import tqdm, trange
import os
import config

# 我的 APPID AK SK #
APP_ID = config.config['APP_ID']
API_Key = config.config['API_Key']
Secret_Key = config.config['Secret_Key']

# 储存客户端
client = AipNlp(APP_ID, API_Key, Secret_Key)

result_key_list = ['confidence', 'negative_prob', 'positive_prob', 'sentiment']


def exl_write_by_row(table, wt_list, wt_row):
    for cnt in range(len(wt_list)):
        table.write(wt_row, cnt, wt_list[cnt])


class EmotionAnalysis:
    def __init__(self, exl_path, save_path=None):
        self.client = AipNlp(APP_ID, API_Key, Secret_Key)
        self.rd_exl_path = exl_path
        self.rd_exl_file = xlrd.open_workbook_xls(self.rd_exl_path)
        if save_path is None:
            self.wt_exl_path = exl_path
        else:
            self.wt_exl_path = save_path
        self.wt_exl_file = xlwt.Workbook()
        self.table_head = None

    def upload_text(self, text):
        time.sleep(0.5)
        result = self.client.sentimentClassify(text)
        if 'error_msg' in result:
            print('该文本分析出错, 原因: ' + result['error_msg'])
            return 'error'
        else:
            # print(result['items'][0])
            return result['items'][0]

    def analyse(self):
        for table in tqdm(self.rd_exl_file.sheets(), desc='逐页情感分析中', position=0, leave=True):
            # 创建表格副本
            new_table = self.wt_exl_file.add_sheet(table.name)
            self.table_head = table.row_values(0) + result_key_list
            exl_write_by_row(new_table, self.table_head, 0)

            text_col_index = self.table_head.index('发帖正文')
            for row_cnt in tqdm(range(1, table.nrows), desc='逐行情感分析中', position=0, leave=True):
                text = table.cell(row_cnt, text_col_index).value
                result_dict = self.upload_text(text)
                # 合并源数据与分析结果
                data_list = table.row_values(row_cnt)
                if result_dict != 'error':
                    for key in result_dict.keys():
                        data_list.append(result_dict[key])
                exl_write_by_row(new_table, data_list, row_cnt)

        self.rd_exl_file.release_resources()
        if os.path.exists(self.wt_exl_path):
            os.remove(self.wt_exl_path)
        self.wt_exl_file.save(self.wt_exl_path)


if __name__ == '__main__':
    new_task = EmotionAnalysis(exl_path="")
    new_task.analyse()
