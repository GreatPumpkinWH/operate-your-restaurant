# Final Project Report

**Project URL**: (https://github.com/CMU-IDS-Spring-2024/final-project-team6/)

**Video URL**: (https://www.youtube.com/watch?v=G2CPzgFBIfU)

# Restaurant Success Analysis and Prediction 
## Abstract

In the highly competitive restaurant business, success depends on many things, including picking the right spot and having a deep understanding of how the market works. MarketScope: Restaurant Viability Analyzer is a state-of-the-art analysis tool that gives user who want to open a restaurant important information about these things. Our project uses the large Yelp dataset, which has specific information on businesses and customers who have checked in, to combine data on customer demographics, market segmentation, and the competitive scene to give a more complete picture of possible business locations.

MarketScope uses advanced data visualization methods and machine learning models to not only visualize how many customers will come in and what demographics will be most likely to buy, but it also looks at the competition to predict how well a restaurant will do. MarketScope uses interactive maps, charts, and predictive scores to give personalized advice that helps potential owners make choices based on data. This helps them improve their business plans and increase their chances of success in a market that is already very crowded.

## Introduction

In today's highly competitive restaurant industry, many new establishments struggle to survive and often close their doors shortly after opening. This phenomenon can be attributed to various factors, but one of the most critical is the lack of thorough understanding of the optimal location and the strategies needed for success. Restaurant owners who fail to grasp the demographics, market dynamics, and competitive landscape of their chosen location are at a higher risk of failure.

To address this pressing issue, our project aims to provide potential restaurant owners with valuable insights and tools to make informed decisions. By leveraging effective visualizations and predictive models, we can offer a comprehensive analysis of the target location, helping entrepreneurs understand the viability of their venture before investing significant resources.

The motivation behind solving this problem is twofold. First, by assisting restaurant owners in making data-driven decisions, we can help reduce the number of business failures, which can have devastating financial and emotional consequences for the owners and their employees. Second, by promoting the establishment of successful restaurants, we can contribute to the growth and diversity of local economies, creating jobs and enhancing the overall quality of life in the community.

Our solution will focus on answering the critical question: "How can we help business owners understand the demographics of the location and estimate the success of the business?" By providing a clear, data-backed answer to this question, we aim to empower restaurant owners with the knowledge and confidence they need to make informed decisions, increasing their chances of success in a highly competitive market.

## Related Work

Recent reports from Yelp provide valuable insights into the current state of the restaurant industry and evolving consumer trends, highlighting the resilience and growth of the sector despite economic challenges. The [State of the Restaurant Industry 2023 report](https://data.yelp.com/state-of-the-restaurant-industry-2023) reveals that the restaurant industry shows strong signs of growth, with new business openings up nationally, especially for pop-up concepts and full-service experiences. Yelp data confirms rising consumer demand, with increased interest in restaurants and nightlife businesses, while other discretionary spending categories like shopping and beauty services have seen a decline.

The report also uncovers shifts in dining habits, with consumers demonstrating an eagerness for special nights out, fine dining experiences, off-peak dining hours, and last-minute reservations. Notably, consumer interest in fine dining has surpassed pre-pandemic levels, while interest in affordable restaurants has dipped. This trend is consistent across major U.S. cities, even in those most impacted by layoffs.

Furthermore, the [Yelp 2023 Business Openings Report](https://data.yelp.com/business-openings-report-2023) highlights the record-breaking growth in new business openings across all categories, with the restaurant and nightlife industry surpassing its pre-pandemic baseline. This growth is driven by diverse entrepreneurs, with LGBTQ-owned, Latinx-owned, and Black-owned businesses outpacing the national average.

As we develop our project to help restaurant owners understand the demographics and potential success of their chosen location, these Yelp reports serve as a valuable foundation. Beyond these prior works, we can provide actionable insights that help restaurant owners make informed decisions, adapt to changing consumer preferences, and increase their chances of success in a highly competitive market. The reports underscore the importance of data-driven decision-making in the restaurant industry and the potential for our solution to make a meaningful impact in supporting business owners navigating the evolving landscape.

## Methods

### Data Processing Methods

1. **Load dataset**: The data is read from `business.csv` and `checkin.csv` files, creating `business_df` and `checkin_df` DataFrames respectively.
2. **Select the category containing 'food' or 'restaurant'**: Rows from `business_df` are filtered to include only those with categories containing 'Restaurants', 'Food', 'Restaurant', or 'Foods'.
3. **Check and handle null values**: Null values are checked, and rows with missing data in the 'hours', 'attributes', and 'address' columns are dropped. After the cleanup, the dataset is reduced from 150,340 rows to 54,441 rows.
4. **Separate business hours by day**: The business hours information in the 'hours' column is parsed to extract the operating hours for each day of the week. New columns, `Monday_hours` to `Sunday_hours`, are created to store the daily operating hours. The total business hours (`hours_sum`) and average business hours (`hours_mean`) are calculated for each business.
5. **Separate 'attributes' and keep only three features**: Three features, 'BusinessAcceptsCreditCards', 'RestaurantsTakeOut', and 'RestaurantsDelivery', are extracted from the 'attributes' column and added as new columns. Rows with missing values in these new columns are dropped.
6. **Divide 'category' into several major categories**: A `category_mapping` dictionary is defined to map various restaurant categories into 8 main categories: Ethnic Cuisine, Fast Food, Coffee & Tea, Bars & Nightlife, Bakeries & Desserts, Healthy Food, Other Cuisine, and Other Food & Drink. The 'categories' column is processed to convert the category information into the main categories, and a new 'main_category' column is created.
7. **Count the number of checkins for each business**: The 'date' column in `checkin_df` is split into individual date entries. The check-in counts for each business are aggregated, and a new 'count' column is added.
8. **Join the two tables and final cleaning**:
   - The `business_df` and `checkin_counts` DataFrames are merged to create the final `clean_data` DataFrame.
   - Rows with missing values in the 'count' and 'postal_code' columns, as well as rows with 'state' as 'AB', are dropped.
   - The cleaned data is saved to a `clean_data.csv` file.

Through these data preprocessing and feature engineering steps, a clean and structured dataset is obtained, ready for further analysis and modeling tasks.

### Visualization Methods

1. Create filters for all the variables we'll be using for our visualizations: location based on states, ratings based on how many stars a restaurant has, what type of restaurant it is, and additional amenities that improve business.
2. Establish the default values of the filters to allow data be shown across all visuals.
3. Most visualizations start out the same with a filtered dataset that will be responsive to any changes made with the filter.
4. Use Altair to create the charts needed for each visualization: bar charts, line charts, map.
   - Two line charts are grouped by different columns, one is by states and one is by the `main_categories`. The color is used to indicate different states or categories to provide more information to the graph.
5. To show the number of restaurants per state, the data for the map is grouped by states, and we used the mean of latitude and longitude as the latitude and longitude for each state. To make the map more interactive and informative, the Pydeck package is used to add tooltips and assign different colors to different states. 
6. For the time plot specifically, the time data needed to be adjusted slightly:
   - Needed to check whether or not the restaurant was open on certain days by checking the duration (0:0-0:0 and 00:00-00:00 means that the restaurant was closed).
   - Restaurants that were open had their hours and minutes values separated to determine when they opened and closed.
   - This was all put into a separate data frame that had all the hours.
7. First visualization was to group all the restaurants that are (on average) opened at certain hours.
8. Second set of visualizations were split up between the days of the week.

## Results

### Visualization Results

Case study: A potential business owner is considering starting his business in California or Pennsylvania. He is considering either opening a Bar or Coffee shop. His business will be accepting credit cards and take-outs, but he is still trying to decide whether to do delivery or not. He is hoping that by using our dashboard, he can decide his business type and the way to operate it.

To reach his goal, the business owner can utilize our dashboard in the following ways:

1. **Set filters to his needs**: According to the above information, we can set the state to California and Pennsylvania, set Category to Coffee & Tea and Bar & Nightlife to compare the choices. Then mark yes to the checkboxes for credit cards and take out. By changing the choice for delivery, we can compare the plots as the data changes accordingly. 

2. **Get the first observation**: By looking at the map under this filter, we can see that there are 507 restaurants in Pennsylvania and 60 restaurants in California. However, by looking at the line chart, we can see that the average check-ins for California is more than the check-ins in Pennsylvania. Therefore, the business owner might consider opening the business in California. By looking at the bar chart, we can see that there are more bars than coffee shops, but the check-ins for bars also outweigh those for coffee shops. 

3. **Use the ML to narrow the focus**: As the business owner can't decide between the Bar and Coffee shop, he can utilize the Machine Learning predictive model that we provide. By selecting California as the state, then comparing the success rate for different cuisine types and delivery choices, the user will be able to decide on the type of business and way to operate. After the try-outs, the user will find out that a coffee shop without delivering service would give the highest success rate of 83.39%.

4. **Use the open hour plot to decide on operating hours**: After the user decides on the type of business he wants to open, he can go back to the plots page and filter down the plots to the business he wants. Then look at the open hour plot to look at the time that his competitors would operate. Since food is a necessary need, having a diverse set of hours in comparison to other businesses can attract more customers. The user can decide on the operating hours based on this. In this case, the user will find out that most coffee shops open on Tuesday through Sunday between 11 am to 2 pm. Based on this information, he can choose the desired opening time.

## Discussion

From a business perspective, this dashboard has loads of information that could help increase sales of the restaurant. One example could be diversifying the hours. There are fewer restaurants opened on Monday, which could give a business owner the advantage of having restaurants opened on Monday. Another way this dashboard could be used to improve business would be allowing them to analyze high-performing restaurants in the area of interest. There are categories and location data that are capable of sorting the data to the desired market. From there, by looking at the rating and check-in visualization, a business owner can stake out high-performing restaurants to understand what additional work such as marketing or food quality makes them more profitable than others. They can also purposefully go to lower-rated restaurants to analyze mistakes that need to be avoided as well. This allows business owners to do more purposeful and thorough analysis of the competition landscape around them.

In addition to being able to make data-driven decisions, the dashboard also allows them to untap potential in restaurants. For example, there are limited bars and nightlife places that are open after midnight. While there are other potential factors such as working hours and people's behavior that could make it difficult, this could also be the start of a new business. As long as there is additional research that proves that there is a need, the business can be successful. Understanding that there are potentially untapped markets within the data could be the next step to a new line of business.

## Future Work

The first potential expansion of the data would be to include all 50 states and eventually add international data as well. This can help businesses all over the world make better decisions in investing in the industry and analyze how they can differentiate themselves in the already competitive market. With more data inputted into the database, this allows for an enhanced predictive model that forecasts future trends in the industry, which enables proactive decision-making and strategic planning for restaurant owners. 

Additionally, this data isn't just limited to business owners but can also be used by average citizens as well. What it has is a list of restaurants, already sorted into different categories, that allows people to quickly discover high-ranking or well-loved restaurants in the area of interest, which could be highly used for social media influencers or traveling. 

With this, a tighter community can be developed from partners and restaurant businesses. This can allow more opportunities for restaurants to branch out and improve their craft by training young professionals or holding collaborations to boost the publicity of their restaurant.
