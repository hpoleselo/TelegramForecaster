import logging
import re
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import seaForecast



class TeleBot(object):
    def __init__(self):
        self.tk = self.retrieveToken()
        # On version 12 use_context is mandatory, on 13 this will be default
        self.updater = Updater(token=self.tk, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.channelID = "@mareVilas"
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    def retrieveToken(self):
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

    def getForecast(self):
        """ Gets the data from our script """
        tc = seaForecast.TideChecker()
        self.firstHigh, self.secondHigh, self.firstLow, self.secondLow = tc.seeTides()

    def sendMessageChannel(self):
        """ The bot sends the message to a channel without the user's prompt.
        Receives the token as argument and message that must be sent as argument. """
        bot = Bot(token=self.tk)
        # Gets the tide information to pass to the message body
        print("[INFO]: Sending message to channel")
        self.getForecast()
        bot.send_message(chat_id=self.channelID, text=self.firstHigh)
        bot.send_message(chat_id=self.channelID, text=self.secondHigh)
        bot.send_message(chat_id=self.channelID, text=self.firstLow)
        bot.send_message(chat_id=self.channelID, text=self.secondLow)
    
            
    # ----- Functions on Telegram to interact with bot ------

    def start(self, update, context):
        """ Callback function to send a message """
        context.bot.send_message(chat_id=update.message.chat_id, text="Sou o bot barril das marés, para saber sobre as marés atualmente em Vilas do Atlântico escreva neste chat /mare")

    def mares(self, update, context): 
        """ Just prints text when the command /start is given on the bot chat """
        self.getForecast()
        context.bot.send_message(chat_id=update.message.chat_id, text=self.firstHigh)
        context.bot.send_message(chat_id=update.message.chat_id, text=self.secondHigh)
        context.bot.send_message(chat_id=update.message.chat_id, text=self.firstLow)
        context.bot.send_message(chat_id=update.message.chat_id, text=self.secondLow)

    def helloWorld(self):
        """ Sent to the polling so when the message is sent on the channel we show the responses. """
        # The second argument is the callback function self.start()
        startHandler = CommandHandler('start', self.start)
        # We pass the start function to our Bot, so when we write "/start" on telegram he should reply whats in self.start()
        self.dispatcher.add_handler(startHandler)

        tidesHandler = CommandHandler('mare', self.mares)
        self.dispatcher.add_handler(tidesHandler)

    def runBot(self):
        print("[INFO]: Trying to run Bot...")
        # Commented out because we're using the Bot only as interface to send automate messages to our channel!
        # If we wanted to really use the bot and its functions we would then uncomment both here
        #self.updater.start_polling()
        #self.helloWorld()
        self.sendMessageChannel()
        print("[INFO]: Message sent. Exiting...")



def run():
    tb = TeleBot()
    tb.runBot()

if __name__ == "__main__":
    run()