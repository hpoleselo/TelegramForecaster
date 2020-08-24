import re
from telegram import Bot
from telegram.ext import Updater
import process


def retrieve_token():
    """ Retrieves the Token from the txt file. """
    try:
        with (open("tokAccess.txt")) as fileRead:
            lines = fileRead.readlines()
            # Remove the \n in the txt file
            lines_wout_n = [s.replace('\n','') for s in lines]
            # Getting token
            return lines_wout_n[0]
    except(KeyboardInterrupt):
        print("Proccess interrupted, could not get the Token.")


def send_message(token, chat_id, high_tide, low_tide):
    """ The bot sends the message to a channel without the user's prompt. """
    bot = Bot(token=token)
    print("[INFO]: Sending message to channel")
    msg = "Dados obtidos do site: surf-forecast.com \n\nObservações:\n - As direções estão em inglês, portanto: \nE - East = Leste \nW - West = Oeste. \n- A energia da onda é uma função do período e do tamanho da onda, dado em kJ, a partir de 200kJ já se tem ondas surfáveis e acima de 400kJ já representa ondas maiores (meio metrão ou maior)."
    tides_msg = "Maré cheia de hoje às:" + high_tide[0] + " com o tamanho de" + high_tide[1] + "m" + "\nMaré seca de hoje às:" + low_tide[0] + " com o tamanho de" + low_tide[1] + "m" 
    #\n\nPróxima maré baixa:"
    bot.send_message(chat_id=chat_id, text=msg)
    bot.send_message(chat_id=chat_id, text=tides_msg)
    bot.send_photo(chat_id=chat_id, photo=open('table.png', 'rb'))


def main():
    """ Generates the image that has to be sent to the Telegram Channel. """
    print("[INFO]: Generating image from the web scrapping.")
    high_tide, low_tide = process.generate_image()
    print(high_tide, low_tide)
    token = retrieve_token()
    # On version 12 use_context is mandatory, on 13 this will be default
    updater = Updater(token=token, use_context=True)
    chat_id = "@previsaoVilas"
    print("[INFO]: Running bot...")
    send_message(token, chat_id, high_tide, low_tide)
    print("[INFO]: Message sent, exiting.")


if __name__ == "__main__":
    main()