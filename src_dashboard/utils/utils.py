from components.data import flight_df

grouping_columns = ["DEPARTING_AIRPORT", "MONTH", "DAY_OF_WEEK",  "CARRIER_NAME", "DEP_DEL15",]

carrier_dropdown_options = [{'label': carrier, 'value': carrier} for carrier in
                            sorted(flight_df['CARRIER_NAME'].unique())]

airport_dropdown_options = [{'label': carrier, 'value': carrier} for carrier in
                            sorted(flight_df['DEPARTING_AIRPORT'].unique())]

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
months_num = [i for i in range(1, len(months) + 1)]
months_slider_ticks = {num: month for num, month in zip(months_num, months)}
month_to_num = {month: num for month, num in zip(months, months_num)}

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Tuesday', 'Friday', 'Saturday', 'Sunday']
days_of_week_num = [i for i in range(1, len(days_of_week) + 1)]
day_checklist_options = [{'label': day, 'value': num} for day, num in zip(days_of_week, days_of_week_num)]
delay_checklist_options = [{'label': 'Delayed', 'value': 1}, {'label': 'On-Time', 'value': 0}]


def extract_data_points(__subset, months):
    count = __subset['COUNT']
    num_months = len(months)

    # Compute features
    return dict(
        mean_concurrent=__subset['CONCURRENT_FLIGHTS'] / count,
        mean_seats=__subset['NUMBER_OF_SEATS'] / count,
        mean_plane_age=__subset['PLANE_AGE'] / count,
        mean_num_flights_per_month = count / num_months,
        pct_delayed_flt=(100 * __subset['SUM_DEP_DEL15']) / count
    )


def subset_to_text(__subset, **kwargs):
    def parse_num(num):
        return "{:.2f}".format(num)

    features = extract_data_points(__subset, **kwargs)
    features = {key: series.apply(parse_num) for key, series in features.items()}

    text = '<b>' + __subset['DEPARTING_AIRPORT'] + '<br><br>[Mean]</b>' \
           + '<br>Concurrent Flights: ' + features['mean_concurrent'] \
           + '<br>Number of Seats: ' + features['mean_seats'] \
           + '<br>Plane Age: ' + features['mean_plane_age'] \
           + '<br>Number of Flights/Month: ' + features['mean_num_flights_per_month'] \
           + '<br>-------' \
           + '<br><br><b>Delayed Flights:</b> ' + features['pct_delayed_flt'] + '%'

    return text
