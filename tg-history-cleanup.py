#!/usr/bin/python3 -u

# This script will automatically delete your history message in all joined groups.
# It will check the latest `n` messages of each joined group, and delete the message if:
#    1. It was sent from you
#    2. The group is not whitelisted in (WHITELIST_CHATS)
#    3. The group was sent at least `t` seconds ago
#
# `n` is MSG_DOWNLOAD_LIMIT, `t` is MSG_ALIVE_TIME
# It's recommended to auto-run this script daily.

##################### Configuration Begin ######################
TELEGRAM_API_ID = '11111111' # Get api_id and api_hash at my.telegram.org
TELEGRAM_API_HASH = '67e72cc9e2b603e08d05446ad5ef8e6'
TELEGRAM_PHONE = '+12223334444' # Phone number in International Format. Example: '+8617719890604'
WHITELIST_CHATS = ['-692222222', '-100195111111111']

MSG_DOWNLOAD_LIMIT = 10000 # Set to '0' for dry-run, set to a huge number for first-run.
MSG_ALIVE_TIME = 24*60*60 # 1 day
##################### Configuration End ########################

from telegram.client import Telegram
import time

tg = Telegram(
    api_id=TELEGRAM_API_ID, 
    api_hash=TELEGRAM_API_HASH,
    phone=TELEGRAM_PHONE,
    database_encryption_key='any_password',
    files_directory='tdlib_files/',
)

def result_of(async_result):
    async_result.wait()
    return async_result.update

def delete_all_msg_from_me(telegram, group_id, receive_limit, my_userid):
    receive = True
    from_message_id = 0
    stats_data = {}
    processed_msg_count = 0
    current_timestamp = time.time()

    while receive:
        response = telegram.get_chat_history(
            chat_id=group_id,
            limit=1000,
            from_message_id=from_message_id,
        )
        response.wait()

        msg_to_delete = []
        for message in response.update['messages']:
            #if message['content']['@type'] == 'messageText':
            #    print(message['content']['text']['text'])
            if message['sender_id']['@type'] != 'messageSenderUser':
                # Not sent from user. Ignore it.
                from_message_id = message['id']
                continue
            if message['sender_id']['user_id'] == my_userid and message['date'] < current_timestamp - 24*60*60:
                msg_to_delete.append(message['id'])
                print("DEBUG: MY message ", message)
            else:
                from_message_id = message['id']

        if msg_to_delete != []:
            print("DEBUG: delete msg count=", len(msg_to_delete))
            tg.delete_messages(group_id, msg_to_delete)

        processed_msg_count += len(response.update['messages'])
        if processed_msg_count > receive_limit or not response.update['total_count']:
            receive = False

        print(f'[{processed_msg_count}/{receive_limit}] processed')


if __name__ == '__main__':
    tg.login()

    my_id = result_of(tg.get_me())['id']

    for chatid in result_of(tg.get_chats())['chat_ids']:
        if chatid >= 0:
            print(f"Ignore chat_id {chatid}, not a group")
            continue
        if chatid in WHITELIST_CHATS or str(chatid) in WHITELIST_CHATS:
            print(f"Ignore chat_id {chatid}, whitelisted")
            continue
        group_title = result_of(tg.get_chat(chatid))['title']
        print("Will cleaning up chat_id ", chatid, group_title)
        delete_all_msg_from_me(tg, str(chatid), MSG_DOWNLOAD_LIMIT, my_id)

    tg.stop()

