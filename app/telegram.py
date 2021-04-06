def telegram_bot_send_text(bot_message):
    try:
        print(bot_message)
        send_text = 'https://api.telegram.org/bot' \
                    + common_config.telegram_bot_token \
                    + '/sendMessage?chat_id=' \
                    + common_config.telegram_chat_id \
                    + '&parse_mode=html&text=' \
                    + quote(bot_message)

        requests.get(send_text, timeout=30)

    except Exception as ex:
        print(ex)
