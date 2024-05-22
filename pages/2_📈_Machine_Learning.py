import streamlit as st
import pandas as pd
import altair as alt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

st.set_page_config(
    page_title="Machine Learning",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_data():
    data = pd.read_csv('data/clean_data.csv')
    return data

data = load_data()

st.title('Restaurant Success Predictor')
st.markdown('Welcome to the Restaurant Success Predictor application! Here, we aim to provide insights into the potential success of restaurants based on various features. Our process involves utilizing machine learning techniques to predict both the ratings and check-in counts of restaurants.')
st.markdown('In this application, we define success rate as the likelihood of a restaurant receiving a high rating. We use a scale from 1 to 5, where a rating of 1 represents 0% success and a rating of 5 represents 100% success. The predicted success rate is calculated using the following formula: Success Rate = (predicted rating -1)/4 * 100% ')

boolean_features = ['BusinessAcceptsCreditCards', 'RestaurantsTakeOut', 'RestaurantsDelivery']
data[boolean_features] = data[boolean_features].fillna(False)

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

data['state'] = data['state'].map(state_map)

st.header('User Input Features')
selected_state = st.selectbox('State', sorted(data['state'].unique()))
selected_cuisine = st.selectbox('Cuisine', sorted(data['main_category'].unique()))
accepts_credit_cards = st.checkbox('Business Accepts Credit Cards')
offers_takeout = st.checkbox('Restaurants Takeout')
offers_delivery = st.checkbox('Restaurants Delivery')

# Define preprocessing for categorical and numeric features
categorical_features = ['state', 'main_category']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Imputer and scaler for numeric and Boolean features
numeric_and_boolean_features = boolean_features
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Define ColumnTransformer to apply feature processing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_and_boolean_features),
        ('cat', categorical_transformer, categorical_features),
    ])

# Prepare the features and targets for modeling
X = data[categorical_features + numeric_and_boolean_features]
y_rating = data['stars']
y_checkins = data['count']

# Create two model pipelines
pipeline_rating = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

pipeline_checkins = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

# Train the models
model_rating = pipeline_rating.fit(X, y_rating)
model_checkins = pipeline_checkins.fit(X, y_checkins)

# Interaction for predictions
if st.button('Predict') and (accepts_credit_cards or offers_takeout or offers_delivery):
    # Filter data according to user selection for visualization
    filtered_data = data[
        (data['state'] == selected_state) &
        (data['main_category'] == selected_cuisine) &
        (data['BusinessAcceptsCreditCards'] == accepts_credit_cards) &
        (data['RestaurantsTakeOut'] == offers_takeout) &
        (data['RestaurantsDelivery'] == offers_delivery)
    ]

    if not filtered_data.empty:
         # Display individual predictions
        user_input_df = pd.DataFrame([{
            'state': selected_state,
            'main_category': selected_cuisine,
            'BusinessAcceptsCreditCards': accepts_credit_cards,
            'RestaurantsTakeOut': offers_takeout,
            'RestaurantsDelivery': offers_delivery
        }])
        predicted_rating = model_rating.predict(user_input_df)[0]
        predicted_checkins = model_checkins.predict(user_input_df)[0]
        success_rate = ((predicted_rating - 1) / 4) * 100

        st.subheader("Individual Prediction Results:")
        st.write(f"Predicted Rating: {predicted_rating:.2f}")
        st.write(f"Predicted Check-ins: {predicted_checkins:.0f}")
        st.write(f"Predicted Success Rate: {success_rate:.2f}%")
        
        # Add actual columns for ratings and check-ins to filtered_data for visualization
        filtered_data['Actual Ratings'] = filtered_data['stars']
        filtered_data['Actual Check-ins'] = filtered_data['count']

        # Predict ratings and check-ins for the filtered data
        filtered_data['Predicted Ratings'] = model_rating.predict(filtered_data[categorical_features + numeric_and_boolean_features])
        filtered_data['Predicted Check-ins'] = model_checkins.predict(filtered_data[categorical_features + numeric_and_boolean_features])

        # Visualization: actual vs predicted scatter plot
        predicted_data = filtered_data.copy()
        predicted_data['Source'] = 'Predicted'

        # Add a Source column to the original filtered_data for actual points
        filtered_data['Source'] = 'Actual'
        filtered_data['Predicted Ratings'] = filtered_data['stars']
        filtered_data['Predicted Check-ins'] = filtered_data['count']

        # Combine the actual and predicted data
        combined_data = pd.concat([filtered_data, predicted_data])

        st.markdown("In the graph below, the actual data points under the given filter are showing in blue and the predicted result is showing in red.")

        # Plotting
        plot = alt.Chart(combined_data).mark_circle(size=60, opacity=0.5).encode(
            x=alt.X('Predicted Ratings', title='Ratings'),
            y=alt.Y('Predicted Check-ins', title='Check-ins'),
            color=alt.Color('Source:N', legend=alt.Legend(title="Data Type"),
                    scale=alt.Scale(domain=['Actual', 'Predicted'], range=['blue', 'red'])),
            tooltip=['Predicted Ratings', 'Predicted Check-ins', 'Source']
        ).properties(
            title="Actual vs. Predicted Check-ins and Ratings"
        ).interactive()

        st.altair_chart(plot, use_container_width=True)
        
    else:
        st.error('No data available for the selected filters. Please try different options.')
else:
    if not (accepts_credit_cards or offers_takeout or offers_delivery):
        st.error('Please select at least one amenity to display the results.')
