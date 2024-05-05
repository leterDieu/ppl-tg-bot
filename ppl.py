from tchan import ChannelScraper
from config import CHANNEL_NAME, SEASON_NUMBER


def manage_unread_messages():
    with open('last-message-id.txt', 'r', encoding='utf-8') as f:
        last_message_id = int(f.read())

    scraper = ChannelScraper()
    execute = False
    last_message_id_write = last_message_id
    for message in scraper.messages(CHANNEL_NAME):
        if message.id <= last_message_id:
            break

        else:
            last_message_id_write += 1

        text = message.text
        if text is None:
            continue
        elif f'PepeLand {SEASON_NUMBER}' in text:
            execute = True

    with open('last-message-id.txt', 'w', encoding='utf-8') as f:
        f.write(str(last_message_id_write))

    return execute
