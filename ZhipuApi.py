from zhipuai import ZhipuAI
import config


api_key = config.config['api_key']


class ZhipuAIReply:
    def __init__(self, text):
        self.text = text
        self.client = ZhipuAI(api_key=api_key)
        self.reply = None

    def GetReply(self, prompt=None):
        content = "作为一名网络舆论回复专家，请为接下来提供的帖子生成一段评论，要能够安抚人心，实现平息舆论的目的，字数要限制在100字以内，并且言简意赅"
        if prompt is not None:
            content = prompt
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": content},
                {"role": "assistant", "content": "当然可以。请您提供那段恶意言论，我会根据内容生成一段旨在安抚人心、平息舆论的回复。"},
                {"role": "user", "content": '不要提到自己的身份，只需要生成回复即可。回复要从普通网民视角出发，以网友的口吻回复,风格要接近一般网络评论'},
                {"role": "assistant", "content": "好的，我不会提到自己的身份。我会从普通网民角度出发，以网友的语气生成回复。"},
                {"role": "user", "content": '句首和句尾不要使用引号。'},
                {"role": "user", "content": self.text},
            ],
            # stream=True,
        )
        self.reply = response.choices[0].message
        return response.choices[0].message


if __name__ == '__main__':
    text = '#谭竹 一只小布#一只小布为谭竹胖猫事件揭发了更多真相，原来谭竹不仅坑害胖猫，同时也在对女生下手，发展Pua对象敛财。这让人想到诱骗老手都美竹，也是在网络上对单亲妈妈骗💰，号称报警也不怕。谭竹、都美竹等捞女如此恶劣，却打着女性的旗号敛财，是妇女权益进步最大的绊脚石，简直给兢兢业业认真工作的女性群体蒙羞，希望这两人得到法律的严惩。 '
    test = ZhipuAIReply(text=text)
    reply = test.GetReply()
    print(test.reply.content)
    """
    CompletionMessage(content='哎，看到这样的消息真是让人心情沉重。我觉得吧，不管事情真相如何，我们都不能因为个别人的行为就否定了一个群体。网络上总是会有一些负面新闻，但咱们不能让这些极端案例影响了我们对大多数人的判断。法律是公正的，如果真的有人做了违法的事，自然会有法律来严惩。我们作为网民，还是应该保持冷静，不要被情绪带了节奏。\n\n至于那些真正在努力工作、认真生活的女性，她们才是我们应该关注的焦点。咱们不能因为少数人的行为，就给整个群体贴上标签。让我们一起期待正义的到来，同时也要传播正能量，支持那些真正值得尊敬的人们。别让一时的愤怒和偏见，遮住了我们看待这个世界的眼睛。加油，小伙伴们！🌟', role='assistant', tool_calls=None)
    """
"""
同步调用示例，调用后即可一次性获得最终结果
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
    ],
)
print(response.choices[0].message)
"""

"""
异步调用示例，调用后会立即返回一个任务 ID ，然后用任务ID查询调用结果（根据模型和参数的不同，通常需要等待10-30秒才能得到最终结果）
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="") # 请填写您自己的APIKey
response = client.chat.asyncCompletions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {
            "role": "user",
            "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"
        }
    ],
)
print(response)
"""

"""
SSE调用示例，调用后可以流式的实时获取到结果直到结束
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="") # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
        {"role": "user", "content": "我对太阳系的行星非常感兴趣，特别是土星。请提供关于土星的基本信息，包括其大小、组成、环系统和任何独特的天文现象。"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)
"""
