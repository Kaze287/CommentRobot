from SpiderForTopic import Spider
from EmotionAnalysis import EmotionAnalysis
from GenerateAIReply import GenerateAIReply
from DataFilter import DataFilter
import datetime
from BulkSend import BulkSend

if __name__ == '__main__':
    # 确定话题关键词 爬取帖子的开始和结束时间 文件保存路径
    question = '谭竹'
    begin_date = datetime.date(2024, 5, 6)
    end_date = datetime.date(2024, 5, 6)
    file_path = f"Sina_Topic_From_{begin_date}_To_{end_date}_{question}.xls"

    # 爬取热点话题
    new_spider = Spider(ques=question, beg_date=begin_date, end_date=end_date, file_path=file_path)
    new_spider.run()
    print('爬取目标话题完成')

    # 获取情感分析
    new_analyse_task = EmotionAnalysis(exl_path=file_path)
    new_analyse_task.analyse()
    print('获取情感分析完成')

    # 筛选负面情感较强的帖子并生成AI回复存储在数据表内
    new_gen_task = GenerateAIReply(exl_path=file_path, confidence_thr=0.95, negative_prob_thr=0.95)
    new_gen_task.save_AI_reply()
    print('生成AI回复完成')

    # 检阅数据表选出需要发送的评论
    new_filter = DataFilter(exl_path=file_path)
    datalist = new_filter.filter()
    print('筛选数据完成')

    # 发送评论
    new_send = BulkSend(datalist)
    new_send.run()
    new_send.print_success_rate()
    print('发送回复完成')
