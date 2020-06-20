import pandas as pd
from forecast import TideChecker



cars = {'day1': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
        'day12': [22000,25000,27000,35000]
        }

index=['Período:','Velocidade do Vento:','Direção do Vento:','Tamanho da Ondulação:']
columns =  ['day1','day12','day13']
df = pd.DataFrame(cars, columns = columns, index=index)

print(df)


def processData(period, energy, wave_height, wind_speed, wind_direction, dates):
                """ All the data retrieved is gonna be treated now to be sent to Telegram
                Send as text? Generate table using Pandas but then converting to csv style?
                """
                pass
                # Using pandas, try to create a table from this csv and then generate image/text?


def main():
    td = TideChecker()
    period, energy, wave_height, wind_speed, wind_direction, dates, time = td.checkContent()
    processData(period, energy, wave_height, wind_speed, wind_direction, dates, time)