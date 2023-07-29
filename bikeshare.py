import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_city_name():
    """
    Asks the user to select a city from the provided options.

    Returns:
        str: The name of the selected city (e.g., 'chicago', 'new york city', or 'washington').
    """
    while True:
        city_name = input('\nPlease select a city to apply the filter. Choose from the following options: New York City, Chicago, or Washington\n').lower()
        if city_name not in ('new york city', 'chicago', 'washington'):
            print('Please enter a valid city name')
        else:
            return city_name

def get_month_name():
    """
    Asks the user to specify the desired month for filtering.

    Returns:
        str: The name of the selected month (e.g., 'january', 'february', ..., 'june') or 'none' for no month filter.
    """
    while True:
        month_name = input('\nPlease specify the desired month for filtering. Kindly provide the name of the month (January, February, ... June), or enter \'none\' for no month filter.\n').lower()
        if month_name not in ('january', 'february', 'march', 'april', 'may', 'june', 'none'):
            print('Please enter a valid month ')
        else:
            return month_name

def get_day_name():
    """
    Asks the user to indicate the day of the week for filtering.

    Returns:
        str: The name of the selected day (e.g., 'monday', 'tuesday', ..., 'sunday') or 'none' for no day filter.
    """
    while True:
        day_name = input('\nPlease indicate the day of the week you wish to filter. Kindly enter the name of the day (Monday, Tuesday, ..., Sunday), or type \'none\' if you do not want to apply a day filter.\n').lower()
        if day_name not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'none'):
            print('Please enter a valid day name.')
        else:
            return day_name

def get_filters():
    """
    Gets user input for city, month, and day filters.

    Returns:
        tuple: A tuple containing three elements - city name, month name, and day name.
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    city_name = get_city_name()
    month_name = get_month_name()
    day_name = get_day_name()
    print('-' * 40)
    return city_name, month_name, day_name

def load_data(city_name, month_name, day_name):
    """
    Loads bikeshare data based on user's filtering choices.

    Args:
        city_name (str): The name of the selected city.
        month_name (str): The name of the selected month or 'none' for no month filter.
        day_name (str): The name of the selected day or 'none' for no day filter.

    Returns:
        DataFrame: A pandas DataFrame containing the filtered bikeshare data.
    """
    filename = CITY_DATA[city_name]
    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    if month_name != 'none':
        month_name = month_name.title()
        df = df[df['month'] == month_name]

    if day_name != 'none':
        day_name = day_name.title()
        df = df[df['day'] == day_name]

    return df

def calculate_execution_time(start_time):
    """
    Calculates and prints the execution time of a function.

    Args:
        start_time (float): The start time in seconds.
    """
    execution_time = time.time() - start_time
    print(f'\nThis took {execution_time} seconds.')

def format_time(seconds):
    """
    Formats seconds into hours, minutes, and seconds.

    Args:
        seconds (float): The duration in seconds.

    Returns:
        str: The formatted duration (e.g.,'2 hours, 30 minutes, 15 seconds').
    """
    hours, remaining_seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(remaining_seconds, 60)
    return f'{hours} hours, {minutes} minutes, {seconds} seconds'

def time_stats(df):
    """
    Calculates and prints popular times of travel.

    Args:
        df (DataFrame): The bikeshare data as a pandas DataFrame.
    """
    print('\nCalculating Popular times of travel \n')
    start_time = time.time()
    mode_month = df['month'].mode()[0]
    mode_day = df['day'].mode()[0]
    mode_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'The Most Common Month: {mode_month}')
    print(f'The Most Common Day: {mode_day}')
    print(f'The Most Common Hour: {mode_hour}')

    calculate_execution_time(start_time)
    print('-' * 40)

def station_stats(df):
    """
    Calculates and prints popular stations and trip combinations.

    Args:
        df (DataFrame): The bikeshare data as a pandas DataFrame.
    """
    print('\nCalculating Popular Stations And Trip \n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    end_station = df['End Station'].mode()[0]
    combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most Commonly Used Start Station: {start_station}')
    print(f'Most Commonly Used End Station: {end_station}')
    print('Most Frequent Combination of Start Station and End Station:')
    print(combination_station)

    calculate_execution_time(start_time)
    print('-' * 40)

def trip_duration_stats(df):
    """
    Calculates and prints trip duration statistics.

    Args:
        df (DataFrame): The bikeshare data as a pandas DataFrame.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    total_hours, total_seconds = divmod(total_travel_time, 3600)
    total_minutes, total_seconds = divmod(total_seconds, 60)
    mean_hours, mean_seconds = divmod(mean_travel_time, 3600)
    mean_minutes, mean_seconds = divmod(mean_seconds, 60)

    print(f'Total Travel Time: {int(total_hours)} hours, {int(total_minutes)} minutes, {int(total_seconds)} seconds')
    print(f'Mean Travel Time: {int(mean_hours)} hours, {int(mean_minutes)} minutes, {int(mean_seconds)} seconds')

    calculate_execution_time(start_time)
    print('-' * 40)

def user_stats(df):
    """
    Calculates and prints user information statistics.

    Args:
        df (DataFrame): The bikeshare data as a pandas DataFrame.
    """
    print('\nCalculating User Info \n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Types:')
    print(user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Breakdown:')
        print(gender_counts)
    else:
        print('\nGender Breakdown:')
        print('No data available for this city.')

    if 'Birth Year' in df.columns:
        birth_year_available = True
        earliest_year = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f'\nThe Most Earliest Birth-Year: {earliest_year}')
        print(f'The Most Recent Birth-Year: {most_recent}')
        print(f'The Most Common Birth-Year: {most_common_year}')
    else:
        birth_year_available = False
        print('\nBirth Year Information:')
        print('No data available for this city.')

    calculate_execution_time(start_time)
    print('-' * 40)

def display_data(df):
    """
    Asks the user if he want to see 5 rows of raw data, then displays that data if the answer is 'yes'.
    Continues iterating the prompts and displaying the next 5 rows of raw data at each iteration.
    Stops the program when the user says 'no' or there is no more raw data to display.

    Args:
        df (DataFrame): The bikeshare data as a pandas DataFrame.
    """
    start_loc = 0
    while True:
        display_raw_data = input('\nDo you want to see 5 rows of raw data? Enter "yes" or "no".\n').lower()
        if display_raw_data == 'yes':
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)

            print(tabulate(df.iloc[start_loc: start_loc + 5], headers='keys', tablefmt='grid'))
            start_loc += 5
        elif display_raw_data == 'no':
            break
        else:
            print('Invalid input. Please enter "yes" or "no".')
            
def main():
    """
    Main function to run the program.
    """
    while True:
        city_name, month_name, day_name = get_filters()
        df = load_data(city_name, month_name, day_name)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to start again? Please enter yes or no: ')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
