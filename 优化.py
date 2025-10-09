# 控制台交互过程

prompt = "请输入你的问题："
user_input = input("欢迎使用智能回答系统：" + prompt)

# 输入处理： 去空格，转小写， 首字母大写

original_input = user_input #保留数据
user_input = user_input.strip().lower().capitalize()

#判断是否退出
if (user_input == "Exit"):
    print("感谢使用， 再见！")

#如果不是exit， 则继续处理
else:
    # 字符反转
    reversed_input = user_input[::-1]
    replace_input = original_input.strip()
    replace_rules = {
        "hello": "你好",
        "hi": "嗨",
        "thanks": "谢谢",
        "thank you": "谢谢你",
    }
    #处理只是钱钱的使用循环，仅仅是为了将replace_rules规则放置到对话中
    for key, value in replace_rules.items():
        replace_input = replace_input.lower().replace(key, value).capitalize()

    #特征分析(字符串操作)
    is_question = user_input.endswith("?")
    is_greeting = user_input.startswith("Hello") or user_input.startswith("Hi")
    is_math = (user_input.replace("+", "").replace("-", "").replace("*", "").replace("/", "").isdigit())

    #判断开头和结尾的特殊内容
    starts_with_what = user_input.startswith("what")
    ends_with_period = user_input.endswith(".")
    has_exclamation = "|" in user_input

    #初始化response变量

    response = ""

    # 使用and/or创建响应
    if (is_greeting):
        response = "你好， 有什么可以帮助的吗？"
    elif (is_question):
        response = "这是个好问题，答案是也许吧"
    elif (is_math):
        response = "计算结果为" + str(eval(user_input))
    elif (starts_with_what):
        response = "你问的是什么问题呢？可以详细说说吗？"
    elif(ends_with_period):
        response = "我注意到你的句子以句号结尾"
    elif(has_exclamation):
        response = response + "看起来你很需要解决"
    else:
        response = "抱歉， 我不太明白"

    response = response.center(50, " ")
    response_upper = response.upper()
    response_clean = response.strip()
    response_word = "|".join(response.split())
    response_final = f"回答：{response_clean}\n" \
    f"大写:{response_upper}"\
    f"分词：{response_word}"\
    f"反转输入：{reversed_input}"\
    f"替换后输入:{replace_input}"
    # print(response_final)
    print("\n" + "=" * 60 + "\n" + response_final + "\n" + "="*60)

print("结束")
