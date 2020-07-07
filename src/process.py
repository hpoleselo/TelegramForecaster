import pandas as pd
import forecast


def processData(period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time):
    """ All the data retrieved is gonna be treated now to be sent to Telegram
    Send as text? Generate table using Pandas but then converting to csv style?
    """

    initialColumns = checaDeslocamento(time)

    # Creating our pandas dataframe
    forecastTable = {}
    rowsIndex = ['Horário','Período da Ondulação:','Velocidade do Vento:','Direção do Vento:', 'Tamanho da Ondulação:','Direção da Ondulação:', 'Energia da Ondulação:']
    columns = []
    counter = 0
    # 8 is the number of subdivisions in a day
    secondThreshold = initialColumns + 8
    thirdThreshold = secondThreshold + 8
    
    # Colocar len
    for i in range(23):
        counter+=1
        if counter <= initialColumns:
            columns.append(dates[0])
            # colocar horário times
        elif counter <= secondThreshold:
            columns.append(dates[1])
        elif counter <= thirdThreshold:
            columns.append(dates[2])
        elif counter > thirdThreshold:
            columns.append(dates[3])


    df = pd.DataFrame(forecastTable, columns=columns, index=rowsIndex)
    print(df)
    # pegar max.energy() p/ avaliar melhor dia com min.wind()
    # Using pandas, try to create a table from this csv and then generate image/text?


def generateImage(df):
    pass
    #return image


def checaDeslocamento(time):
    """ Since the day the we're looking isn't going to display the full day (all the eight times), then we have to know before how many
    days we're going to plot since it's not 8. We do that by checking the transition between PM -> AM (when it's the transition between days) 
    
    The variable returned here is the number of columns with the first day to be plotted.
    """
    pmCounter = 0
    amCounter = 0
    generalCounter = 0
    initialTime = time[0]
    initialState = initialTime[-2:]
    print(time)
    for i in range(len(time)):
        generalCounter += 1
        currentTime = time[i]
        # Since we want to detect the transition from PM to AM, then we just have to check when this transiion happens.
        # -2: gets the PM/AM suffix from the time
        currentState = currentTime[-2:]

        if currentState == "AM":
            amCounter += 1

        # To check if there's been transition, whether is AM->PM or PM->AM
        if not (currentState == initialState):
            print("General: There was a transition!")
            if (initialState == "PM"):
                print("\nThe initial stage was PM:")
                print("There was a transition between days!")
                # Since we detect the transition after n+1 iterations, we have to decrease by 1
                displacement = generalCounter - 1
                print("How many times to plot PM: ", displacement)
                return displacement
            else:
                print("\nThe initial stage was AM:")
                print("Não houve transição de dias")
                print("How many times to plot AM: ", amCounter)
                # Since everytime we come to transition AM->PM and the PM ALWAYS appears 4x times on a day when preeceded by AM, then the number is fixed: 4.
                displacement = amCounter + 4
                return displacement

def main():
    response = forecast.checkPage()
    pageText = forecast.checkContent(response)
    period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time = forecast.getContent(pageText)
    processData(period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time)


if __name__ == "__main__":
        main()
