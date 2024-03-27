import time
import pandas as pd

#Dictionary containing file names for each city.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_data = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'january', 'february', 'march', 'april', 'may', 'june']
day_data = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Ask users to specify filters for city, month and day.
    Returns:
        city, month and day filters
    """
    #Filter by city. valid_city updates to True when a valid city is inputted.
    valid_city = False
    while not valid_city:
        input_city = input("What city would you like to view? Chicago, New York City, Washington or all?  \n").lower() 
        if input_city in CITY_DATA.keys():
            city = input_city
            valid_city = True
        elif input_city == 'all':
            city = input_city
            valid_city = True
        else:
            print("Something went wrong... Try again")

    
    #filter by month of year (Jan - Jun)
    valid_month = False
    while not valid_month:
        input_month = input("Which month would you like to view? Jan, Feb, Mar, Apr, May, Jun or all? \n").lower() 
        if input_month in month_data:
            month = input_month
            valid_month = True
        elif input_month == 'all':
            month = input_month
            valid_month = True
        else:
            print("Something went wrong... Try again")
    
    #filter by day of week
    valid_day = False
    while not valid_day:
        input_day = input("Which day of the week would you like to view? Mon, Tue, Wed, Thu, Fri, Sat, Sun or all? \n").lower()
        if input_day in day_data:
            valid_day = True
            day = input_day
        elif input_day == 'all':
            day = input_day
            valid_day = True
        else:
            print("Something went wrong... Try again")


    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Returns:
        selected_df - DataFrame containing city data filtered by month and day

    dfs is an empty dictionary which gets populated dynamically by CITY_DATA. This allows for scaling up.
    """
    
    #dictionary to store dataframes for each city.
    dfs = {}

    for city_key, filename in CITY_DATA.items():
        df = pd.read_csv(filename, index_col=0)
        df['City'] = city_key.title()
        dfs[city_key] = df

    selected_df = pd.DataFrame()

    #if city exists in dfs dictionary then assign the city dataframe to selected_df
    if city in dfs:
        selected_df = dfs[city]

    #if city == 'all', then concat all dataframes stored in the dfs dictionary to selected_df
    elif city == 'all':
        for city, df in dfs.items():
            #check if the selected_df is empty
            if selected_df.empty:
                selected_df = df
            else:
                selected_df = pd.concat([selected_df, df])

    #convert column to datetime format
    selected_df['Start Time'] = pd.to_datetime(selected_df['Start Time'])
    selected_df['End Time'] = pd.to_datetime(selected_df['End Time'])
    
    #convert mixed int/float values in 'Trip Duration' column into a float.
    selected_df['Trip Duration'] = selected_df['Trip Duration'].astype(float)
    
    #filter dataframe by month
    if month != 'all':
        month = month.title()
        selected_df = selected_df[(selected_df['Start Time'].dt.strftime('%b') == month) | (selected_df['Start Time'].dt.strftime('%B') == month)]
    
    #filter dataframe by day
    if day != 'all':
        day = day.title()
        selected_df = selected_df[(selected_df['Start Time'].dt.strftime('%a') == day) | (selected_df['Start Time'].dt.strftime('%A') == day)]

    return selected_df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate the most common month
    most_common_month = df['Start Time'].dt.strftime('%B').value_counts().idxmax()
    month_count = df['Start Time'].dt.strftime('%B').value_counts().max()
    print(f"The most common month of travel is: {most_common_month} with a count of: {month_count}")

    # Calculate the most common day of week
    most_common_day = df['Start Time'].dt.strftime('%A').value_counts().idxmax()
    day_count = df['Start Time'].dt.strftime('%A').value_counts().max()
    print(f"The most common day of travel is: {most_common_day} with a count of: {day_count}")

    # Calculate the most common start hour
    most_common_hour = df['Start Time'].dt.strftime('%H').value_counts().idxmax()
    hour_count = df['Start Time'].dt.strftime('%H').value_counts().max()
    print(f"The most common hour of travel is: {most_common_hour} with a count of: {hour_count}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df['Start Station'].value_counts().idxmax()
    start_station_count = df['Start Station'].value_counts().max()
    
    print(f"Most popular start station: {most_popular_start_station}, Total count: {start_station_count}")

    # display most commonly used end station
    most_popular_end_station = df['End Station'].value_counts().idxmax()
    end_station_count = df['End Station'].value_counts().max()
    
    print(f"Most popular end station: {most_popular_end_station}, Total count: {end_station_count}")

    # display most frequent combination of start station and end station trip
    most_popular_combo = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    max_count_index = most_popular_combo['Count'].idxmax()
    max_count_row = most_popular_combo.loc[max_count_index]

    print(f"The most frequent station combination is... Start Station: {max_count_row['Start Station']} and "
          f"End station: {max_count_row['End Station']} with a count of {max_count_row['Count']}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #count the number of rows
    table_count = df['Trip Duration'].count()
   
    #display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print(f"Count: {table_count}, Total Duration: {total_travel_time}, Avg Duration: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_result = "User Type and Count: "
    user_type = df.groupby(['User Type'])['User Type'].count().reset_index(name='Count')
    for index, row in user_type.iterrows():
        user_type_result += f"{row['User Type']} {row['Count']}, "
    print(user_type_result[:-2])

    #create a new dataframe called filtered_df that excludes washington rows
    filtered_df = df[df['City'] != 'Washington']

    #if the dataframe doesn't return empty then carry out gender and birth year stats
    if not filtered_df.empty:
        # Display counts of gender
        user_gender_result = "User Gender and Count: "
        user_gender = filtered_df.groupby(['Gender'])['Gender'].count().reset_index(name='Count')
        for index, row in user_gender.iterrows():
            user_gender_result += f"{row['Gender']} {row['Count']}, "
        print(user_gender_result[:-2])

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(filtered_df['Birth Year'].min())
        count_earliest_year = (filtered_df['Birth Year'] == earliest_year).sum()

        most_recent_year = int(filtered_df['Birth Year'].max())
        count_recent_year = (filtered_df['Birth Year'] == most_recent_year).sum()

        most_common_year = int(filtered_df['Birth Year'].value_counts().idxmax())
        count_most_common_year = (filtered_df['Birth Year'] == most_common_year).sum()

        print(f"The earliest year of birth is {earliest_year} (count:{count_earliest_year}), " 
            f"the most recent year of birth is {most_recent_year} (count:{count_recent_year}) " 
            f"and the most common birth year is {most_common_year} (count: {count_most_common_year}).")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Display raw data on bikeshare users """
    
    #if more rows is yes, 5 more rows will be shown, if no the loop will stop.
    more_rows = 'yes'
    while more_rows == 'yes':
        print(df.sample(n=5))
        more_rows = input("\nWould you like to view 5 more rows of raw data?\n")
    else:
        more_rows == 'no'

def main():
    while True:
        print(f"Welcome! Let's explore some Bikshare data.\n")
        
        #provide city, month, day from get_filters() to load_data() to create the dataframe
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(f"\nYou have selected: City = {city}, Month = {month}, Day = {day}\n")
           
        time_stats(df) 
        station_stats(df)
        user_stats(df)
        trip_duration_stats(df)

        view_raw_data = input('\nWould you like to view 5 rows of raw data? \n')
        if view_raw_data == 'yes':
            raw_data(df)
              
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()