import datetime
from datetime import datetime, timezone
import imaplib
import email
from email.header import decode_header
import time
import telebot
from telebot import types
from settings import *

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')


def check_email():
    """Подключается к ящику, чекает новые письма, если есть - парсит и отправляет увед через тг бота"""
    try:
        mail = imaplib.IMAP4_SSL(YANDEX_IMAP, 993)
        mail.login(YANDEX_EMAIL, YANDEX_PASSWORD)
        mail.select('inbox')

        typ, data = mail.search(None, 'UNSEEN')
        unseen_email_ids = data[0].split()

        if unseen_email_ids:
            print(f"{datetime.now(timezone.utc)} New emails found: {len(unseen_email_ids)}.")
            for num in unseen_email_ids:
                result, msg_data = mail.fetch(message_set=num, message_parts='(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                if isinstance(decode_header(msg["Subject"])[0][0], str):
                    email_subject = decode_header(msg["Subject"])[0][0]
                else:
                    email_subject = decode_header(msg["Subject"])[0][0].decode()
                ticket_data = email_subject.split('_*_')
                notification_type = ticket_data[0]
                ticket_id = ticket_data[1]
                ticket_author = ticket_data[2]
                ticket_url = ticket_data[3]
                notification_message = "✉️<b>Freshdesk\n</b> "
                if notification_type == "newticket" or notification_type == 'Test Mail - newticket':
                    notification_message += "<u>Новая заявка</u>🆕\n"
                if notification_type == "ticketupdated" or notification_type == 'Test Mail - ticketupdated':
                    notification_message += "<u>Заявка обновлена</u>🔄\n"
                notification_message += (f"<b>ID заявки:</b> {ticket_id}\n"
                                         f"<b>Автор:</b> {ticket_author}")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="👀 Перейти к заявке", url=ticket_url))
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=notification_message, reply_markup=markup)
                print(f"{datetime.now(timezone.utc)} Notification message sent.")

        mail.logout()
        print(f"{datetime.now(timezone.utc)} emails checked.")
    except Exception as e:
        print(f"Ошибка при проверке почты: {e}")


def main():
    while True:
        check_email()
        time.sleep(60)  # Проверка каждые 60 секунд


if __name__ == "__main__":
    main()
