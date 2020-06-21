import pandas as pd
import forecast

#testar criacao de dataframe com for
#for i in range(3)

#forecastTable = {'Sun-20'}

#forecastTable = {'day1': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
#        'day12': [22000,25000,27000,35000]
#        }

#index=['Horário','Período:','Velocidade do Vento:','Direção do Vento:'] #,'Tamanho da Ondulação:','Direção da Ondulação:', 'Energia da Ondulação:']
#columns =  ['day1','day12']
#columns =  ['day1','day12','day13']
#df = pd.DataFrame(forecastTable, columns = columns, index=index)
#energy.max() pra pegar o dia com a maior energia ou o dia com o menor vento? fazer um matching?

#print(df)

def processData(period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time):
    """ All the data retrieved is gonna be treated now to be sent to Telegram
    Send as text? Generate table using Pandas but then converting to csv style?
    """
    print(time)
    if time[0] == "6PM":
        for i in range(2):
            print("Gera 2 datas")

    # IDENTIFICAMOS AS TRANCISOES DOS DIAS (A TRANSICAO EH DE 9PM P 0AM NA TABELA)
    # CONTAMOS QTO LEVA DO PRIMEIRO TERMO ATE O TERMO QUE POSSUI A TRANSICAO DE 9PM P AM
    # USAREMOS 2 FOR, O PRIMEIRO PRA UM CASO GERAL CASO HAJA TRANSICAO AM->PM E O SEGUNDO PRA CHECAGEM FINA DE EH DE 

    checaDeslocamento(time)

    # Using pandas, try to create a table from this csv and then generate image/text?


def checaDeslocamento(time):
    # NA VERDADE EH MAIS FACIL AINDA, SO CHECAR A TRANSICAO PM->AM, SO OCORRE QUANDO PASSA DE UM DIA PRO OUTRO!!!
    # dependendo do numero de casas , geramos o numero inicial a partir desse contador e ai colocamos os dias x vezes no forecastable
    firstCounter = 0
    secondCounter = 0
    generalCounter = 0
    initialState = time[0]
    for i in range(len(time)):
        generalCounter += 1
        currentState = time[i]
        # -2: gets the PM/AM
        if currentState[-2:] == "PM":
            print("Current state is PM")
            firstCounter += 1
            print("\nFirst counter: ", firstCounter)
        elif currentState[-2:] == "AM":
            print("Current state is AM")
            secondCounter += 1
            print("\nSecond counter: ", secondCounter)
        if not firstCounter < generalCounter:
            print("Chegou a transicao pois o contador geral ultrapassou o contador local do PM")
            break
    print("Contador global: ", generalCounter)
    print("Contador local 1: ", firstCounter)
    # Because the counting begins on 0.. So we're gonna place 2 spots if the generalCounter reutnrrs 1
    displacement = generalCounter + 1

    # test tomorrow for other cases and check if the number of initial pms on the list matches the displacement

def main():
    response = forecast.checkPage()
    pageText = forecast.checkContent(response)
    period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time = forecast.getContent(pageText)
    processData(period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time)


if __name__ == "__main__":
        main()
