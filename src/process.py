import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import forecast


def process_data(table_length, period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide):
    """ All the data retrieved is gonna be treated now to be sent to Telegram as an image
    """

    initialColumns = check_displacement(time)

    # Creating our pandas dataframe
    forecastTable = {}
    rowsIndex = ['Horário','Período da Ondulação (s)','Velocidade do Vento (km/h)','Direção do Vento', 'Tamanho da Ondulação (m)','Direção da Ondulação', 'Máxima Energia da Ondulação (kJ)']
    columns = []
    counter = 0
    # 8 is the number of subdivisions in a day
    secondThreshold = initialColumns + 8
    thirdThreshold = secondThreshold + 8
    
    # Colocar len
    for i in range(table_length):
        counter+=1
        if counter <= initialColumns:
            columns.append(dates[0])
        elif counter <= secondThreshold:
            columns.append(dates[1])
        elif counter <= thirdThreshold:
            columns.append(dates[2])
        elif counter > thirdThreshold:
            columns.append(dates[3])


    df = pd.DataFrame(forecastTable, columns=columns, index=rowsIndex)
    df.loc['Horário'] = time
    df.loc['Período da Ondulação (s)'] = period
    df.loc['Velocidade do Vento (km/h)'] = wind_speed
    df.loc['Direção do Vento'] = wind_direction
    df.loc['Tamanho da Ondulação (m)'] = wave_height
    df.loc['Direção da Ondulação'] = wave_direction
    df.loc['Máxima Energia da Ondulação (kJ)'] = energy
    # pegar max.energy() p/ avaliar melhor dia com min.wind()

    # Low and high tides are independent from all the rest but we still have to clean it out because it comes with a lot of empty values:
    high_tide = list(filter(None, high_tide))
    low_tide = list(filter(None, low_tide))

    # Get only the first values
    high_tide = high_tide[0:2]
    low_tide = low_tide[0:2]

    return df, high_tide, low_tide


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                        header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                        bbox=[0, 0, 1, 1], header_columns=0,
                        ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in mpl_table._cells.items():
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return ax.get_figure(), ax


def df_to_img(df):
    """ Using matplotlib to generate our image instead of Weasyprint (dataframe to html, then CSS and saving as png) """
    print("DF Ta como?")
    print(df)
    fig, ax = render_mpl_table(df, header_columns=0, col_width=2.0)
    print("[INFO]: Saving image...")
    fig.savefig("table.png")


def check_displacement(time):
    """ Since the day the we're looking isn't going to display the full day (all the eight times), then we have to know before how many
    days we're going to plot since it's not 8. We do that by checking the transition between PM -> AM (when it's the transition between days) 
    
    The variable returned here is the number of columns with the first day to be plotted.
    """
    pmCounter = 0
    amCounter = 0
    generalCounter = 0
    initialTime = time[0]
    initialState = initialTime[-2:]
    #print(time)
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
            #print("General: There was a transition!")
            if (initialState == "PM"):
                #print("\nThe initial stage was PM:")
                #print("There was a transition between days!")
                # Since we detect the transition after n+1 iterations, we have to decrease by 1
                displacement = generalCounter - 1
                #print("How many times to plot PM: ", displacement)
                return displacement
            else:
                #print("\nThe initial stage was AM:")
                #print("Não houve transição de dias")
                #print("How many times to plot AM: ", amCounter)
                # Since everytime we come to transition AM->PM and the PM ALWAYS appears 4x times on a day when preeceded by AM, then the number is fixed: 4.
                displacement = amCounter + 4
                return displacement


def generate_image():
    """ Generates a png image from the data retrieved from the web scrapping. This should be sent then to the user in the Telegram API. """
    response = forecast.checkPage()
    pageText = forecast.checkContent(response)
    table_length, period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide = forecast.getContent(pageText)
    df, high_tide, low_tide = process_data(table_length, period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide)
    df_to_img(df)
    # Primeiro de tudo, o dataframe nao esta sendo sliced, usar notebook pra testar de forma interativa
    df[0:15]
    print(df) 
    return high_tide, low_tide
