import vertexai
from vertexai.generative_models import GenerativeModel
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import config

def load_generative_ai_model():
    vertexai.init(project='skills-building-413521', location="asia-east1")
    model = GenerativeModel(model_name="gemini-1.0-pro-002")

    return model
    

# 封裝 echo 函數以包含 model 參數
def echo_with_model(model):
    def echo(update: Update, context: CallbackContext) -> None:
        # 獲取用戶發送的消息
        user_message = update.message.text
        response = model.generate_content(user_message)
        
        # Access the actual attribute containing generated text
        generated_text = response.text

        update.message.reply_text(generated_text)
    return echo


def main():
    model = load_generative_ai_model()
    token = config.get_tg_bot_token()
    
    # 創建 Updater 對象
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # 使用封裝後的 echo 函數
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo_with_model(model))
    dispatcher.add_handler(echo_handler)

    # 開始輪詢
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
