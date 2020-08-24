# Waves Forecast on Telegram

![ezgif com-resize](https://user-images.githubusercontent.com/24254286/89701303-da62d800-d90b-11ea-9e64-75c5e7d6537c.gif)

This application scrapes the website [surf-forecast](https://pt.surf-forecast.com/breaks/Vilas/forecasts/latest) from [Vilas do Atlântico](https://www.google.com/maps/place/Vilas+do+Atl%C3%A2ntico,+Lauro+de+Freitas+-+BA/@-12.8878487,-38.3036089,15z/data=!3m1!4b1!4m5!3m4!1s0x7163e0b19cade15:0x3f93745901875860!8m2!3d-12.8868037!4d-38.2975914), which can be easily replaced on the code by your wished location, just change the URL from surf-forecast in the ``` /src/forecast.py ``` file.
Original project was being developed under my ``` tools ``` [repository](https://github.com/hpoleselo/tools/tree/master/WavesForecast). But since it could be used by others i thought it would be nicer to have a separate repo for it.

## Requirements

This was done using Python3.5, the main dependencies are:
```pandas```, ```lxml```, ```BeautifulSoup```, ```python-telegram-bot``` and ```requests```. Clone the repository to your computer and run this command to install them all:

``` $ pip3 install -r requirements.txt ```

## Usage

In order to run the application, just access the ``` src ``` folder and:

``` $ python3 telegramInterface.py ```

## Automate using anacron

Instead of having a server to run our script, one possible solution is to use ``` anacron ``` to run our Python script periodically. I decided to run it once a day. If you want to do it yourself, create an executable shell script but **without** the ``` .sh ``` extension, otherwise cron won't run your script, there's an example located on this repository (without underline, dashes etc, otherwise cron won't run it as well) called ``` runforecaster.sh ```.

1. Make sure to remove the ``` .sh ``` extension from the file
2. If you wish to run it daily, then ``` $ sudo cp runforecaster /etc/cron.daily ```
3. To debug and check if it's running properly: ``` $ sudo run-parts /etc/cron.daily ``` if anything goes wrong it will output on the same terminal.
4. To check the log from anacron ``` $ grep anacron /var/log/syslog ```
5. To check when anacron will run your daily scripts ``` $ grep run-parts /etc/crontab ```

## Improvements
- [ ] Add tide high and low times column
- [ ] Analisys from the energy and wind and create a condition column
- [ ] Try to get data from windguru and send both graphs
- [ ] Send report to e-mail

## Author
* **Henrique Poleselo** - [hpoleselo](https://github.com/hpoleselo)

