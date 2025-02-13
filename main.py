from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from database import save_user_interests, find_matching_users
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-13DJKXp6QBphm8MaRbUwOiwRmx9E2qwW6lf9dMP30eEeqyXJ",
    base_url="https://api.deerapi.com/v1"
)

async def start(update, context):
    """处理 /start 命令"""
    await update.message.reply_text("欢迎！请告诉我你喜欢的游戏类型，例如'我喜欢原神和王者荣耀'。")

async def handle_message(update, context):
    """处理用户消息"""
    user_id = update.message.from_user.id
    user_input = update.message.text

    # 调用 ChatGPT 提取兴趣关键词
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个兴趣标签提取助手。请从用户的消息中提取游戏相关的兴趣关键词，以逗号分隔。例如用户输入'我喜欢原神和VR游戏'，输出'原神,VR游戏'。"},
                {"role": "user", "content": f"提取兴趣关键词：{user_input}"}
            ]
        )
        # 解析 ChatGPT 的响应
        raw_interests = response.choices[0].message.content.strip()
        interests = [x.strip() for x in raw_interests.split(",") if x.strip()]
        
        if not interests:
            await update.message.reply_text("未识别到兴趣标签，请重新输入。")
            return

    except Exception as e:
        print(f"ChatGPT 调用失败: {e}")
        await update.message.reply_text("服务暂时不可用，请稍后再试。")
        return

    # 保存兴趣标签到数据库
    if save_user_interests(user_id, interests):
        await update.message.reply_text(f"已记录你的兴趣：{', '.join(interests)}！正在寻找匹配玩家...")
        matches = find_matching_users(user_id, interests)
        if matches:
            match_list = "\n".join([f"用户 {user['user_id']}（兴趣：{', '.join(user['interests'])}）" for user in matches])
            await update.message.reply_text(f"找到以下匹配玩家：\n{match_list}")
        else:
            await update.message.reply_text("暂时没有匹配的玩家。")
    else:
        await update.message.reply_text("保存兴趣失败，请重试。")

def main():
    """启动机器人"""
    # 使用 ApplicationBuilder 初始化应用
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # 启动轮询
    application.run_polling()

if __name__ == "__main__":
    main()