import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ["january","february","march","april","may","june"]
DAYS = ["sunday","monday","thursday","wednesday","tuesday","friday","saturday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please specify a a city from the list [chicago, new york city, washington]:\n ").strip().lower()
        if not city in ["chicago", "new york city", "washington"]:
            print("Please specify a valid city name from the list only.")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(f"Please specify a name of the month from {MONTHS} to filter by, or 'all' to apply no month filter:\n ").strip().lower()
        if not (month in MONTHS or month == "all"):
            print("Please specify a valid month name or 'all' to apply no month filter.")
            continue
        else:
            break  

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(f"Please specify a name of the day from {DAYS} to filter by, or 'all' to apply no month filter:\n ").strip().lower()
        if not (day in DAYS or day == "all"):
            print("Please specify a valid day name or 'all' to apply no filter.")
            continue
        else:
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
    df = pd.read_csv(CITY_DATA.get(city))
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    
    df["Month"] = df["Start Time"].dt.month
    
    df["Day"] = df["Start Time"].dt.weekday_name
    
    df["Start Hour"] = df["Start Time"].dt.hour
    
    if month != "all":
        month = MONTHS.index(month) + 1
        df = df.loc[df["Month"] == month]
        
    if day != "all":
        day = day.title()
        df = df.loc[df["Day"] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = MONTHS[((df["Month"].mode()[0]) - 1)].upper()
    print(f"The Most Common Month Is : {most_common_month}")

    # TO DO: display the most common day of week
    most_common_day = df["Day"].mode()[0].upper()
    print(f"The Most Common Day Is : {most_common_day}")
    # TO DO: display the most common start hour
    most_common_st_hour = df["Start Hour"].mode()[0]
    hour = ""
    if most_common_st_hour == 0 :
        hour = "12 AM"
    elif most_common_st_hour == 12 :
        hour = "12 PM"   
    elif most_common_st_hour > 12 :
        hour = f"{most_common_st_hour - 12} PM"
    else:
        hour = f"{most_common_st_hour} AM"
        
    print(f"The Most Common Start Hour Is : {hour}")    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_most = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {start_station_most}")

    # TO DO: display most commonly used end station
    end_station_most = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {end_station_most}")

    # TO DO: display most frequent combination of start station and end station trip
    df["Start to End Stations"] = df["Start Station"] +" ---> "+df["End Station"]
    start_end_com_most = df["Start to End Stations"].mode()[0]
    print(f"The most frequent combination of start station and end station trip is: {start_end_com_most}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    """Convert the seconds to 'Hours, Minutes, Seconds' format """
    def seconds_to_hours(seconds):
        hours = int((seconds // 3600))
        minutes = int(((seconds % 3600)//60))
        seconds = int(((seconds % 3600) % 60).round())
        return f"{hours} Hour(s), {minutes} Minute(s), {seconds} Second(s)."
    
    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"The total travel time is: {seconds_to_hours(total_travel_time)}")

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"The total travel time is: {seconds_to_hours(mean_travel_time)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df["User Type"].value_counts().to_frame()
    print(f"Users Types Count is: \n{user_types_count}\n")

    # TO DO: Display counts of gender
    if city != 'washington' :
        gender_counts = df["Gender"].value_counts().to_frame()
        print(f"Users Gender Count is: \n{gender_counts}\n")

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_bth_year = int(df['Birth Year'].min())
        most_recent_bth_year = int(df['Birth Year'].max())
        most_common_bth_year = int(df['Birth Year'].mode())
        
        print(f"The earliest year of birth is: {earliest_bth_year}")
        print(f"The most recent year of birth is: {most_recent_bth_year}")
        print(f"The most common year of birth is: {most_common_bth_year}")
    else:
        print("There is no gender and birth year data for this city...")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_raw_data(city):
    """Displays the row data of bikeshare users."""  
    print("Row data is availabe ...")
    df = pd.read_csv(CITY_DATA.get(city))
    pd.set_option("display.max_columns",200)
    index = 0
    run = True
    while run:
        #Ask the user if he want to display a chunk of 5 rows from the row data.
        ans = input("Would you like to show 5 rows from the row data (yes/no)? \n").strip().lower()
        #Check if the user's answer invalid , repeat the question and ask him to enter valid input.
        if ans not in ("yes","no"):
            print("Please enter a valid input (yes/no).")
            continue
        elif ans == 'no':
            break
        else:
            while index < df.shape[0]:
                start_time = time.time()
                print(df.iloc[index : index+5])
                print("\nThis took %s seconds." % (time.time() - start_time))
                index += 5
                #Ask the user again if he want to display more 5 rows from the row data.
                ans = input("\nWould you like to show more 5 rows (yes/no)? \n").strip().lower()
                #Check if the user's answer invalid , repeat the question and ask him to enter valid input.
                while ans not in ("yes", "no"):
                    print("Please enter a valid input (yes/no).")
                    ans = input("Would you like to show more 5 rows (yes/no)? \n").strip().lower()
                if ans == "no":
                    run = False
                    break
                else:
                    pass
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()