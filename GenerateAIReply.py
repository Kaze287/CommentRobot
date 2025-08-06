from ZhipuApi import ZhipuAIReply
import xlrd
import xlwt
from tqdm import tqdm, trange
import os


def exl_write_by_row(table, wt_list, wt_row):
    for cnt in range(len(wt_list)):
        table.write(wt_row, cnt, wt_list[cnt])


class GenerateAIReply:
    def __init__(self, exl_path, save_path=None, confidence_thr=0.85, negative_prob_thr=0.8):
        self.rd_exl_path = exl_path
        self.rd_exl_file = xlrd.open_workbook_xls(self.rd_exl_path)
        if save_path is None:
            self.wt_exl_path = exl_path
        else:
            self.wt_exl_path = save_path
        self.wt_exl_file = xlwt.Workbook()
        self.table_head = None
        self.confidence_thr = confidence_thr
        self.negative_prob_thr = negative_prob_thr
        self.AI_reply = None

    def save_AI_reply(self):
        for table in tqdm(self.rd_exl_file.sheets(), desc='逐页获取数据中'):
            # 创建表格副本
            new_table = self.wt_exl_file.add_sheet(table.name)
            self.table_head = table.row_values(0) + ['AI回复']
            exl_write_by_row(new_table, self.table_head, 0)

            text_col_index = self.table_head.index('发帖正文')
            confi_col_index = self.table_head.index('confidence')
            neg_prob_col_index = self.table_head.index('negative_prob')

            for row_cnt in tqdm(range(1, table.nrows), desc='逐行生成AI回复中', position=0, leave=True):
                confidence = table.cell(row_cnt, confi_col_index).value
                neg_prob = table.cell(row_cnt, neg_prob_col_index).value
                text = table.cell(row_cnt, text_col_index).value
                if confidence > self.confidence_thr and neg_prob > self.negative_prob_thr:
                    self.AI_reply = ZhipuAIReply(text).GetReply().content
                else:
                    self.AI_reply = '#内容消极信息含量较低，不生成回复#'
                data_list = table.row_values(row_cnt)
                data_list.append(self.AI_reply)
                exl_write_by_row(new_table, data_list, row_cnt)

        self.rd_exl_file.release_resources()
        if os.path.exists(self.wt_exl_path):
            os.remove(self.wt_exl_path)
        self.wt_exl_file.save(self.wt_exl_path)


if __name__ == '__main__':
    new_task = GenerateAIReply(exl_path='', save_path='')
    new_task.save_AI_reply()
    """
    Row Processing: 100%|██████████| 432/432 [18:00<00:00,  2.50s/it]
    Table Processing: 100%|██████████| 1/1 [18:00<00:00, 1080.76s/it]
    """

