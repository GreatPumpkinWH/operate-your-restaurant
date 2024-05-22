import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Wide layout for streamlit
st.set_page_config(
    page_title="Landscape Plots",
    page_icon="📊",
    layout="wide"
)

# Importing cleaned data
df = pd.read_csv("data/clean_data.csv")
# st.dataframe(df)

# Replace state abbreviations with full state names in the 'state' column
state_map = {
    'PA': 'Pennsylvania',
    'TN': 'Tennessee',
    'IN': 'Indiana',
    'FL': 'Florida',
    'NV': 'Nevada',
    'IL': 'Illinois',
    'AZ': 'Arizona',
    'LA': 'Louisiana',
    'CA': 'California',
    'MO': 'Missouri',
    'NJ': 'New Jersey',
    'ID': 'Idaho',
    'DE': 'Delaware',
    'NC': 'North Carolina'
}

df['state'] = df['state'].map(state_map)

# Title of the Dashboard
st.title("Restaurant Market Landscape Charts")
st.markdown("This page features a variety of interactive visualizations designed to enhance users' understanding of market dynamics.")

# Filters for charts and graphs
st.header("Filters")
st.markdown("Select the states, business category, operational details, and business rating according to your needs; the filter will apply to all the plots below.")
col1, col2, col3 = st.columns(3)

# Filter for states
state_options = sorted(df["state"].unique())
state_filter = col1.multiselect(
    label = "Select State(s)",
    options = state_options,
    default = state_options
)

# Filter for rating
df["stars"] = df["stars"].astype(float)

min_rating = df["stars"].min()
max_rating = df["stars"].max()

rating_filter = st.slider(
    label = "Select rating",
    min_value = min_rating,
    max_value = max_rating,
    value = (min_rating, max_rating),
    step = 0.5
)

# Filter for category
category_options = sorted(df["main_category"].unique())
category_filter = col2.multiselect(
    label = "Select Category",
    options = category_options,
    default = category_options
)

# Boolean Filters
credit_card_filter = col3.checkbox("Business Accepts Credit Cards", True)
takeout_filter = col3.checkbox("Restaurants Offer TakeOut", True)
delivery_filter = col3.checkbox("Restaurants Offer Delivery", True)

# Charts and graphs
st.header("Visualizations")

# Filter the data to use in the following graphs 
filtered_data = df[
    (df['state'].isin(state_filter)) &
    (df['stars'].between(rating_filter[0], rating_filter[1])) &
    (df['main_category'].isin(category_filter)) &
    (df["BusinessAcceptsCreditCards"] == credit_card_filter) &
    (df["RestaurantsTakeOut"] == takeout_filter) &
    (df["RestaurantsDelivery"] == delivery_filter)
]

# Main categories chart
st.subheader("Main Categories")
st.markdown("This plot displays the number of restaurants per business category, aimed at helping users better understand the competitiveness within each category.")

category_counts = filtered_data['main_category'].value_counts().reset_index()
category_counts.columns = ['main_category', 'count']

category_chart = alt.Chart(category_counts).mark_bar().encode(
    x = alt.X("main_category:N", title = "Category", sort = alt.EncodingSortField(field = "count", op = "sum", order = "descending")),
    y = alt.Y("count:Q", title = "Number of Restaurants")
).properties(
    width=600,
    height=400
)

# Display bar chart
st.altair_chart(category_chart, use_container_width=True)

# Checkins vs rating line plots
st.subheader("Average Number of Checkins by Rating, State, and Category")
st.markdown("The two line charts presented here illustrate the average number of check-ins per rating. The left chart is grouped by states and the right chart by business category. Color coding is used to differentiate groups, assisting users in comparing the average number of check-ins across different states or categories.")

# Group by category
line_chart_cat = alt.Chart(filtered_data).mark_line(point=True).encode(
    x=alt.X('stars:O', title="Rating"),
    y=alt.Y('average(count):Q', title="Average Number of Checkins"),
    color='main_category',
    tooltip=['main_category', 'average(count)']  # Display state, category, and average count on hover
).properties(
    width=700,
    height=400
)

# Group by state
line_chart_state = alt.Chart(filtered_data).mark_line(point=True).encode(
    x=alt.X('stars:O', title="Rating"),
    y=alt.Y('average(count):Q', title="Average Number of Checkins"),
    color='state',  # Color lines by state
    tooltip=['state', 'average(count)']  # Display state, category, and average count on hover
).properties(
    width=700,
    height=400
)
# Display the line plots side by side
col1, col2 = st.columns(2)

with col1:
    st.altair_chart(line_chart_state, use_container_width=True)

with col2:
    st.altair_chart(line_chart_cat, use_container_width=True)


# Map
st.subheader("Map of Restaurants by State")
st.markdown("The map below displays the number of restaurants per state, with different states represented by various colors. Larger circles indicate a higher number of restaurants in a state. This visualization can be used to examine the competitiveness of each state.")
# Group the data by state and calculate the number of restaurants in each state
plot_data = filtered_data.groupby('state').agg({
    'latitude': 'mean',  # Use the mean latitude of restaurants in the state
    'longitude': 'mean',  # Use the mean longitude of restaurants in the state
    'business_id': 'count'  # Count the number of restaurants
}).reset_index().rename(columns={'business_id': 'count'})

# Assign a unique color to each state using a colormap
unique_states = plot_data['state'].unique()
np.random.seed(42)  # For consistent colors across runs
colors = np.random.choice(range(256), size=(len(unique_states), 3))
state_to_color = {state: colors[i].tolist() for i, state in enumerate(unique_states)}
plot_data['color'] = plot_data['state'].apply(lambda x: state_to_color[x] + [160]) 

# Set the viewport location
view_state = pdk.ViewState(
    latitude=plot_data['latitude'].mean(),
    longitude=plot_data['longitude'].mean(),
    zoom=3,
    pitch=0
)

# Define the layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=plot_data,
    get_position=['longitude', 'latitude'],
    get_color='color',
    get_radius='count * 100',  # Adjust radius scale to data
    pickable=True  # necessary for tooltip to work
)

# Render the deck.gl map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{state}\nNumber of Restaurants: {count}"}
)

# Plot the map
st.pydeck_chart(r)

#Plot open-hours
st.subheader("Number of Open Restaurants by Hour and Day")
st.markdown("The blue chart below displays the general number of open restaurants throughout the day, with the y-axis showing the number of restaurants and the x-axis representing the hour of the day. Darker shades indicate a higher concentration of restaurants. The red charts provide the same information but are segmented by weekdays for a more detailed analysis. These charts are designed to help users identify optimal operating times to minimize competition.")
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Convert opening hours to a list of hours
def get_open_hours(row):
    open_hours = []
    for day in days:
        hours = row[f"{day}_hours"]
        if pd.isna(hours) or hours == '0:0-0:0' or hours == '00:00-00:00':
            continue
        start, end = hours.split('-')
        start_h, _ = map(int, start.split(':'))
        end_h, _ = map(int, end.split(':'))
        if end_h < start_h:
            end_h += 24
        open_hours.extend([(day, hour) for hour in range(start_h, end_h+1)])
    return open_hours

# Apply the function and explode the result
filtered_data.loc[:, 'open_hours'] = filtered_data.apply(get_open_hours, axis=1)
open_hours_data = filtered_data.explode('open_hours')
open_hours_data[['day', 'hour']] = pd.DataFrame(open_hours_data['open_hours'].tolist(), index=open_hours_data.index)

# Create a DataFrame containing all hours
all_hours = pd.DataFrame({'hour': range(24)})

# Define color schemes
color_scheme_alldays = "blues"
color_scheme_days = "yelloworangered"

# Create a chart with all days data
all_data = open_hours_data.groupby('hour').size().reset_index(name='count')
all_data = all_hours.merge(all_data, on='hour', how='left').fillna(0)
all_data['hour'] = all_data['hour'].apply(lambda x: f"{x:02d}:00")

all_chart = alt.Chart(all_data).mark_bar().encode(
    x=alt.X('hour:O', title='Operating Hour'), # Manually setting x-axis ticks
    y=alt.Y('count:Q', title='Number of Open Restaurants'),
    color=alt.Color('count:Q', scale=alt.Scale(scheme=color_scheme_alldays)),
    tooltip=['hour', 'count']
)
st.altair_chart(all_chart, use_container_width=True)

# Create a list of charts for each day
day_charts = []
for day in days:
    day_data = open_hours_data[open_hours_data['day'] == day]
    open_restaurants_by_hour = day_data.groupby('hour').size().reset_index(name='count')
    open_restaurants_by_hour = all_hours.merge(open_restaurants_by_hour, on='hour', how='left').fillna(0)
    open_restaurants_by_hour['hour'] = open_restaurants_by_hour['hour'].apply(lambda x: f"{x:02d}:00")

    chart = alt.Chart(open_restaurants_by_hour).mark_bar().encode(
        x=alt.X('hour:O', title='Operating Hour'),
        y=alt.Y('count:Q', title='Number of Open Restaurants'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme=color_scheme_days)),
        tooltip=['hour', 'count']
    ).properties(
        width=300,
        height=200,
        title=f"{day}"
    )
    day_charts.append(chart)

# Combine charts for all days
combined_chart = alt.vconcat(
    *[alt.hconcat(*day_charts[i:i+4]) for i in range(0, len(day_charts), 4)]
)

# Apply configurations
combined_chart = combined_chart.configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)

# Display the chart
st.altair_chart(combined_chart, use_container_width=True)
