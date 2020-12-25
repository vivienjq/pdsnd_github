
import time
import pandas as pd
import numpy as np
import json


CITY_DATA = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}

CITIES = ['chicago', 'new york', 'washington', 'all']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare datails!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
       city = input('Please choose a city to explore: Chicago, New York or Washington: ').lower()
       if city in CITIES:
           break

    # get user input for month (all, january, february, ... , june)
    while True:
       month = input('Now please enter a month: january, february, march, april, may, june or enter all: ').lower()
       if month in MONTHS:
          break
    # TO DO: get user input for day
    while True:
        day = input('Which day of the week would you like to check out or enter all: ').lower()
        if day in DAYS:
            break

    print('-'*40)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day)

    # display the most common start hour

    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    for index,gender_count   in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))

    print()


def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']

    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)

    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)

    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data != 'no'):
        print(df.iloc[start_loc:(start_loc + 5)])
        start_loc += 5
        view_display = input('Do you wish to continue?: ').lower()
        if view_display != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
