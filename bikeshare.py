import time
import pandas as pd
import numpy as np
import os


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def get_files():
    """
    Create a dictionary of .csv files and cities from the current directory

    Returns:
        (dict) city_dict - a dictionary with city names as keys and .csv file names as values
    """

    city_dict = {}
    #Fills a dictionary with only .csv files in the current directory
    for f in [f for f in os.listdir() if ".csv" in f]:
        city_dict[f.replace(".csv", "").replace("_"," ")] = f

    return city_dict

CITY_DATA = get_files()

def get_city():
    """
    Asks user to specify a city and uses the load_data() function to return the city and DataFrame of the city .csv file.

    Returns:
        (str) city - name of the city to analyze
        (DataFrame) - a DataFrame of the .csv file of the selected city
    """

    print("\nPlease type which of this cities you would like to select:")
    for i in CITY_DATA:
        print("-", i.title())
    filter_city = input("\nCity: ")
    filter_city = filter_city.strip().lower()

    #Checks if user input city is in the city dictionary
    while True:
        if filter_city in CITY_DATA:
            break
        else:
            filter_city = input("Not a valid city!\nPlease type a valid city: ")
            filter_city = filter_city.strip().lower()

    #Calls the load_data function to return a DataFrame based on the csv file of the city selected
    df = load_data(filter_city)

    return df, filter_city


def load_data(city):
    """
    Loads data for the specified city and adds datetime columns.

    Args:
        (str) city - name of the city to analyze
    Returns:
        df - Pandas DataFrame of selected city with additional columns Month and Day of the week, based on column Start Time
    """

    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name, index_col=0)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df.insert(1, 'Month', df['Start Time'].dt.month)
    df.insert(2,'Day of Week', df['Start Time'].dt.weekday_name) #Use this code when Pandas version == v0.23
    #df.insert(2,'Day of Week', df['Start Time'].dt.day_name()) #Use this code when Pandas version > v0.23

    return df

def get_filter_month(df):
    '''
    Creates a DataFrame filtered by the month the user inputs

    Args:
        (DataFrame) df - a dataframe with a column named 'Month'
    Returns:
        (DataFrame) df - a dataframe filtered by the user input of month
    '''

    #Calls the function extract_month to return a dictionary of available months in DataFrame
    month_dict = extract_month(df)

    #Prints name of months available on DataFrame. Each month in DataFrame is an int so the code below take that int
    #and compares it to a list of months so that the users sees the name of the month and not the number
    print("\nPlease type which of this months would you like to filter by:")
    for i in month_dict:
        print("-", i)
    print("If you would like all months, type 'All'")

    #Asks the users to select month
    month_filter = input("\nMonth: ")
    month_filter = month_filter.strip().title()

    #Validates user input
    while True:
        if month_filter in month_dict:
            df = df[df['Month'] == month_dict[month_filter]]
            break
        elif month_filter == 'All':
            break
        else:
            month_filter = input("Not a valid month!\nPlease type a valid month: ")
            month_filter = month_filter.strip().title()

    return df


def get_filter_day(df):
    '''
    Filters a DataFrame by day selected by user

    Args:
        (DataFrame) df - a dataframe with a column named 'Day of Week'
    Returns:
        (DataFrame) df - a dataframe filtered by the user input of day

    '''
    #Prints and asks the user which day from the available ones, would the user like
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print("\nPlease type which of this days would you like to filter by:")
    for i in days:
        print("-", i)
    print("If you would like all days, type 'All'")

    filter_day = input("\nDay: ")
    filter_day= filter_day.strip().title()

    #Validates user input and filters DataFrame by day selected by the user
    while True:
        if filter_day in days:
            df = df[df["Day of Week"] == filter_day]
            break
        elif filter_day == 'All':
            break
        else:
            filter_day = input("Not a valid day!\nPlease type a valid day: ")
            filter_day = filter_day.strip().title()

    return df

def extract_month(df):
    """
    Saves in a dictionary the months available in a data frame with the column 'Month'

    Args:
        (DataFrame) df - a data frame containing the info of a specific city
    Returns:
        (dict) month_dict - A dictionary with the available months in a the DataFrame provided
    """


    #Extract months available in data
    months_available = list(df['Month'].unique())

    #Convert months into int and sorts
    for i in range(len(months_available)):
        months_available[i] = int(months_available[i])
    months_available = sorted(months_available)

    #Construct month dictionary
    month_dict = {}
    for i in months_available:
        month_dict[months[i-1]] = i

    return month_dict

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most common month: ", months[int(df['Month'].mode()[0])-1])
    print("Most common day of the week: ", df['Day of Week'].mode()[0])
    print("Most common start hour: ", df['Start Time'].dt.hour.mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most common start station: ", df['Start Station'].mode()[0])
    print("Most common end station: ", df['End Station'].mode()[0])
    print("Most common combination of start station and end station: ", (df['Start Station'] + " - " + df['End Station']).mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total travel time: ", "{:.2f}".format(df['Trip Duration'].sum()), 'minutes')
    print("Mean travel time: ", "{:.2f}".format(df['Trip Duration'].mean()), "minutes")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User type counts: ")
    print(df['User Type'].value_counts().to_string())

    #If there is no column 'Gender' it prints out that there is no data available
    try:
        print("\nGender counts: ")
        print(df['Gender'].value_counts().to_string())
    except KeyError:
        print("\nNO GENDER DATA AVAILABLE")

    #If there is no column named 'Birth Year' it prints out that there is no data available
    try:
        print("\nEarlist birth year: ", int(df['Birth Year'].min()))
        print("Most recent birth year: ", int(df['Birth Year'].max()))
        print("Most common birth year: ", int(df['Birth Year'].mode()[0]))
    except KeyError:
        print("\nEarlist birth year: ",  "NO AVAILABLE DATA")
        print("Most recent birth year: ", "NO AVAILABLE DATA")
        print("Most common birth year: ", "NO AVAILABLE DATA")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print('Hello! Let\'s explore some US bikeshare data!')

    #Calls functions the first time
    df, city = get_city()
    df = get_filter_month(df)
    df = get_filter_day(df)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    #Prints out menu of options after first execution
    while True:
        print("\nOptions:")
        print("1 See raw data (with filters already applied)")
        print("2 Change filters")
        print("3 Change city")
        print("4 Close")

        #Validates user input for option selected
        while True:
            option = input('Enter the option number (e.g. Change filters type: 2): ')
            try:
                option = int(option)
                break
            except ValueError:
                print("Please input a valid number")
                continue

        if option == 1:
            print("\n\n")
            count = 0
            print(df.iloc[count:count+5,:])

            #Validates user input for more rows
            while True:
                row_data = input("Type 'y' for more rows or 'n' to exit): ")
                if row_data == 'n':
                    break
                elif row_data == 'y':
                    count += 5
                    print(df.iloc[count:count+5,:])
                else:
                    print("Input not recognized. Please enter 'y' or 'n'\n")


        elif option == 2:
            print("\n\nCity: ", city)
            df = load_data(city)
            df = get_filter_month(df)
            df = get_filter_day(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        elif option == 3:
            df, city = get_city()
            df = get_filter_month(df)
            df = get_filter_day(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            continue

        elif option == 4:
            print("\nPROGRAM CLOSED\nGood bye!")
            break

        else:
            print("\nOption not available\n")


if __name__ == "__main__":
	main()
print("REFACTORINg. SO MUCH WOW. I HOPE I DON'T BREAK THIS")
