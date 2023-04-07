import time
import pandas as pd
import numpy as np
import pprint

# test2 update for GitHub project

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
input_filter = 'none'


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    while city not in ['chicago', 'new york', 'washington']:
        city = input('input city name is not valid, please choose between Chicago, New York, or Washington\n').lower()
    if city == 'new york':
        city = 'new york city'  # match the names in CITY_DATA
    global input_filter
    input_filter = input(
        'Would you like to filter the date by month, day, both, or not at all? Type \"none\" for no time filter\n').lower()
    while input_filter not in ['month', 'day', 'both', 'none']:
        city = input('input option is not valid, please choose between month, day, both, or none\n')

    month = 'all'
    day = 'all'

    # get user input for month (all, january, february, ... , june)
    if input_filter == 'month' or input_filter == 'both':
        month = input('which month? January, February, March, April, May, or June?\n').lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input(
                'input not valid, please choose between January, February, March, April, May, or June?\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if input_filter == 'day' or input_filter == 'both':
        day = input('which day? Please type your response (e.g., Sunday)\n').lower()
        while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input('input not valid, please choose between Monday, Tuesday, Wednesday, Thursday, Friday, '
                        'Saturday, Sunday\n').lower()
        # day = int(day) - 1
        # if day == 0:
        #     day = 6  # Monday=0, Sunday=6
    # print(city + month + day)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    if input_filter not in ['month', 'both']:
        df['month'] = df['Start Time'].dt.month
        print('Most popular month: ' + str(df['month'].mode()[0]), end='')
        print(', Count: ' + str(df['month'].value_counts()[df['month'].mode()[0]]), end='')
        print(' Filter: ' + input_filter)

    # display the most common day of week
    if input_filter not in ['day', 'both']:
        df['day'] = df['Start Time'].dt.dayofweek
        most_popular_day = df['day'].mode()[0]
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print('Most popular day: ' + week[most_popular_day], end='')
        print(', Count: ' + str(df['day'].value_counts()[df['day'].mode()[0]]), end='')
        print(' Filter: ' + input_filter)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour  # find the most common hour (from 0 to 23)
    print('Most popular hour: ' + str(df['hour'].mode()[0]), end='')
    print(', Count: ' + str(df['hour'].value_counts()[df['hour'].mode()[0]]), end='')
    print(' Filter: ' + input_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular Start Station: ' + str(df['Start Station'].mode()[0]), end='')
    print(', Count: ' + str(df['Start Station'].value_counts()[df['Start Station'].mode()[0]]), end='')
    print(' Filter: ' + input_filter)

    # display most commonly used end station
    print('Most popular End Station: ' + str(df['End Station'].mode()[0]), end='')
    print(', Count: ' + str(df['End Station'].value_counts()[df['End Station'].mode()[0]]), end='')
    print(' Filter: ' + input_filter)

    # display most frequent combination of start station and end station trip
    print('Most popular Trip : ' + str(df.groupby(['Start Station', 'End Station']).size().idxmax()), end='')
    print(', Count: ' + str(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)[0]),
          end='')
    print(' Filter: ' + input_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time : ' + str(df["Trip Duration"].sum()), end='')
    print(', Count: ' + str(df.shape[0]), end='')
    # display mean travel time
    print(', mean travel time : ' + str(df["Trip Duration"].mean()), end='')
    print(' Filter: ' + input_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if city != 'washington':
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print(user_types)
        # Display counts of gender
        user_types = df['Gender'].value_counts()
        print(user_types)
        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: ' + str(df["Birth Year"].min().astype(np.int64)),
              end='')
        print(
            ', Most recent year of birth: ' + str(df["Birth Year"].max().astype(np.int64)),
            end='')
        print(', Most common year of birth: ' + str(df['Birth Year'].mode()[0].astype(np.int64)), end='')
        print(', Count: ' + str(df['Birth Year'].value_counts()[df['Birth Year'].mode()[0]]), end='')
        print(' Filter: ' + input_filter)
    else:
        print('Washington has no user gender and age data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """ Your docstring here """
    i = 0
    raw = input("Would you like to view individual trip data? Type 'yes': ").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            pprint.pprint(df.iloc[i:(i + 4)].to_dict(
                orient='records'))  # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Would you like to view more individual trip data? Type 'yes'").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in ['yes', 'no']:
            restart = input('input is not valid. Please enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
