import pandas as pd
import forecast
import weasyprint as wsp
import PIL as pil


def process_data(period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide):
    """ All the data retrieved is gonna be treated now to be sent to Telegram
    Send as text? Generate table using Pandas but then converting to csv style?
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
    for i in range(23):
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


def trim(source_filepath, target_filepath=None, background=None):
    """ Source code from norek: https://stackoverflow.com/questions/35634238/how-to-save-a-pandas-dataframe-table-as-a-png """
    if not target_filepath:
        target_filepath = source_filepath
    img = pil.Image.open(source_filepath)
    if background is None:
        background = img.getpixel((0, 0))
    border = pil.Image.new(img.mode, img.size, background)
    diff = pil.ImageChops.difference(img, border)
    bbox = diff.getbbox()
    img = img.crop(bbox) if bbox else img
    img.save(target_filepath)


def df_to_img(df):
    """ Takes a dataframe and generates an image using weasyprint (dataframe to html) """
    # TODO: Alternate colors on table so we it's visually better
    img_filepath = 'table.png'
    css = wsp.CSS(string='''
    @page { size: 2048px 2048px; padding: 0px; margin: 0px; }
    table, td, tr, th { border: 1px solid black; }
    td, th { padding: 4px 8px; }
    ''')
    html = wsp.HTML(string=df.to_html())
    html.write_png(img_filepath, stylesheets=[css])
    trim(img_filepath)


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
    period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide = forecast.getContent(pageText)
    df, high_tide, low_tide = process_data(period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide)
    df_to_img(df)
    return high_tide, low_tide
