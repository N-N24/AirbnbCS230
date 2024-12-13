"""
Name:       Nilufar Noorian
CS230:      Section 02
Data:       AirBnB
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program will display a website utilizing the Airbnb data (CSV file).
The website has many charts (visual representations) of the data and allows users to interact
with the data by being able to select the neighborhood, or price (based on the function and chart displayed).
"""

import pandas as pd
import streamlit as st
import numpy as np
#math calculations
import matplotlib.pyplot as plt
import seaborn as sns
from altair.vegalite.v5.theme import theme
from click import option
import pydeck as pdk
from matplotlib.pyplot import ylabel
from streamlit.elements.lib.options_selector_utils import index_

df = pd.read_csv("Boston Listings.csv").set_index("id")
#Randomly generates ratings between 1 and 5 for each Airbnb in the DataFrame
#df['rating'] = np.random.randint(1, 6, size=len(df))

#[PY1]
def calculateNeighbourhoodStats(df = pd.read_csv("Boston Listings.csv"), neighbourhood= "Back Bay"):
    #[PY4]
    stats = []
    neighbourhoodData = df[df['neighbourhood'] == neighbourhood]
    maxPrice = neighbourhoodData['price'].max()
    minPrice = neighbourhoodData['price'].min()

    #[PY4]
    stats.append({
        'neighbourhood': neighbourhood,
        'max price': maxPrice,
    })
    #[PY2]
    return stats, minPrice

# Main/Home Page
def intro(file_data = df.to_csv(index=False)):
    averagePrice = df['price'].median()
    dfPrice = df.loc[df['price'] < averagePrice]
    #st.write(dfPrice)
    st.image(image = "Airbnb.jpg", caption = "", width = 500) #[ST4] use_container_width=True,

    st.title("**Airbnb's In Boston**")
    st.write("Welcome to this Airbnb website! Please feel free to navigate between tabs by accessing the sidebar.")
    st.write("")
    st.write("There are over 2,000 Airbnb's in Boston. Whether you are visiting Boston for the first time, are here for a "
             "university graduation, immersing yourself in the rich history and museums, or just want to see more of the city, "
             "there are many Airbnb options for you in the Boston area.")
    st.write("The Boston area includes but is not limited to Beacon Hill, Back Bay, Fenway, Chinatown, the North "
             "End, South Boston, and Brighton, among others.")
    st.write("")
    st.write("If you interested in finding Airbnbs in a neighborhood you are interested in staying at, please navigate to "
             "the **map** tab of the website.")
    st.write("Under the **bar** chart tab, you may slide the bar to the price you are looking for per night and the number of rooms "
             "such as private room or entire home/apartment will appear.")
    st.write("The **scatterplot** tab displays a scatter plot of Airbnbs based on the minimum number of nights required for a "
             "stay and the associated price.")
    #[ST3] - SelectBox
    neighbourhood = st.selectbox("Select a neighborhood:", df['neighbourhood'].unique())
    stats, minPrice = calculateNeighbourhoodStats(df, neighbourhood) #[PY1]
    maxPrice = stats[0]['max price']
    #st.text(f"Fun fact for {neighbourhood}: The maximum price is ${maxPrice:.2f} and the minimum price is ${minPrice:.2f}.")
    st.text(f"For Airbnbs in {neighbourhood}: the maximum price is " f"${maxPrice:.2f}" f" and the minimum price is ${minPrice:.2f}.")
    #st.button("Click here")
    st.download_button(label = "Click here to download the data as a CSV file", data = file_data, file_name = "Boston Listings.csv", mime = "text/csv") #works
    st.image(image = "Apt.jpg", caption = "", use_container_width = True-250)
    st.write("Airbnb Apartment", fontsize = 35)
    neighborhood = ""
    avgPrice = 0.0


# Pie chart of the average price in a neighborhood
def pieChart(): #[VIZ1]
    #def pieChart(lst, selected_neighbourhood):
    df = pd.read_csv("Boston Listings.csv")
    st.write("The top five expensive Airbnbs are the following neighborhoods: ", fontsize = 40)
    # [DA2] - ascending = False [DA3] - .head(5) to find the top five
    topFive = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).head(5)

    # topFive = avgPrice.head(5) based on user input in the multiselect/slider
    for index, value in topFive.items():
        st.write(f"{index}: ${value:.2f}")

    st.header("Average Prices of Airbnb's In The Selected Neighborhoods")
    # avgPrice = df.groupby('neighbourhood')['price'].mean().reset_index()
    # y = avgPrice['price']
    # mylabels = avgPrice['neighbourhood']
    # avgPrice.plot(kind = "pie", legend = True)
    # fig, ax = plt.subplots(figsize=(6, 6))

    # Max of 15 neighborhoods can be viewed easily and is readable
    # Multiselect so users can choose which neighborhoods to compare Airbnb prices
    # [ST2] - Multiselect
    selected_neighbourhood = st.multiselect("Please select the neighborhoods to compare: ",
                                            df['neighbourhood'].unique(), max_selections=15)

    newdf = df[df['neighbourhood'].isin(selected_neighbourhood)]

    # plt.title("Average Prices of Airbnb's In The Selected Neighborhoods")
    #[DA4] - Filtering
    avgPrice = newdf.groupby('neighbourhood')['price'].mean().reset_index()

    # fig, ax = plt.subplots()
    # newdf.plot(kind="pie", y="neighbourhood", ax=ax)
    # st.pyplot(fig)

    #[DA4[
    y = avgPrice.sort_values('price')['price']
    mylabels = avgPrice.sort_values('price')['neighbourhood']
    # y = avgPrice.sort_values('price', ascending = False)['price']
    # mylabels = avgPrice.sort_values('price', ascending = False)['neighbourhood']

    # average price displaying correctly => avgPrice.sort_values('price')['neighbourhood']
    # no points off, figures don't have to be accurate, just having figures

    # y = np.array(df['price'])
    plt.pie(y, labels=mylabels, labeldistance=1.2, autopct='%.2f')
    # plt.legend(loc = "center right", bbox_to_anchor=(1, 0.5, 0.5, 1))
    # Display the Pie Chart
    # df.plot()
    # plt.show()
    st.pyplot(plt)
    #print(mylabels, "LABELS")

    #st.plotly_chart(figure_or_data, selection_mode=('points'))

    #st.multiselect(label = "Select Neighborhoods", options="Roxbury", "Jamaica Plain", "Charlestown", "Dorchester", "North End", "South End", "South Boston", "Roslindale", "Downtown", "West Roxbury", "Brighton", "Beacon Hill", "Hyde Park", "Back Bay", "Fenway", "Chinatown", "Leather District")

#pieChart(neighbourhood='neighbourhood', price= 'price')
    #st.header("Pie Chart")
    #st.plot(kind = "pie", legend = True)

# Room Types By Price with Slider
def barChart(): #[VIZ2]
    df = pd.read_csv("Boston Listings.csv")

    st.header("Bar Chart")
    st.write("This bar chart contains a slider that allows the user input the price per night, and displays "
             "how many rooms are available at the designated price, either a private room or an entire home/apartment.", fontsize = 20)

    #[ST1] - Slider
    number = st.slider(label="Select a price per night to display a bar chart", min_value=0,
                       max_value=int(max(df["price"])))
    st.markdown("**Airbnb Room Types By Price**")
    # st.markdown("Airbnb Room Types By Price", unsafe_allow_html=True)
    filtered_data = df[df['price'] == number]
    room_type_counts = filtered_data['room_type'].value_counts().reset_index()  # Used the bar chart from AI
    room_type_counts.columns = ["room_type", "count"]

    #plt.bar(data=room_type_counts, x="room_type", y="count", height = 10)
    #ax = sns.barplot(data=room_type_counts, x="room_type", y="count") #use seaborn
    #ax.bar_label(ax.containers[0])
    #plt.show()
    st.bar_chart(data=room_type_counts, x="room_type", y="count", x_label="Room Type", y_label="Number of Rooms") #horizontal = True

# Scatterplot of review and available days in the year number_of_reviews & availability_365 columns
def scatterplot(): #[VIZ3]
    df = pd.read_csv("Boston Listings.csv")
    index_to_remove = df['price'].idxmax() #Index of row with max value within the Price column
    #[DA3]
    df = df.drop(index_to_remove) #Deletes it, remove an outlier

    st.header("Airbnbs Based on Minimum Nights Required and Price")
    st.write("This scatterplot shows the price for each Airbnb with respect to the minimum number of nights you "
             "must stay at that Airbnb.")
    st.write("")
    #scatter_data = df[['number_of_reviews', 'availability_365']]
    #st.scatter_chart(data = df, x = 'availability_365', y = 'number_of_reviews', x_label = "Availability In the Year", y_label = "Number of Reviews")
    st.scatter_chart(data = df, x = 'price', y = 'minimum_nights', x_label = "Price ($)", y_label = "Minimum Nights for Stay (Days)")


# Map of Airbnbs by latitude and longitude
def mapChart(): #[MAP]
    #matplotlib
    df = pd.read_csv("Boston Listings.csv")
    #[DA9] New Column
    df['rating'] = np.random.randint(1, 6, size=len(df))

    st.header("Map of Airbnbs")
    st.write("This is a map of Airbnbs in the Boston area.", fontsize = 20)
    #st.write(f'<p style="color: red;">{"This is a map of Airbnbs in the Boston area."}</p>', unsafe_allow_html=True)
    bostonMap = df[['latitude', 'longitude']]
    #filter by price
    #[ST3]
    userInput = st.slider(label="Select a price per night to display a map", min_value=0,
                       max_value=int(max(df["price"])))
    filteredData = df[df['price'] >= userInput]
    #print(filteredData.head())
    #filteredData = pd.merge(filteredData, df[['id', 'rating']], on='id', how='left')


    #st.map(filteredData, color = "#528AAE") #change color
    #if want to change the colors, need to change the dataset too
    #icon_data = df['latitude', 'longitude']
    icon_data = filteredData[['latitude', 'longitude', 'name', 'price', 'rating']] #[DA9] New Column

    icon_url = "https://media.istockphoto.com/id/1148705812/vector/location-icon-vector-pin-sign-isolated-on-white-background-navigation-map-gps-direction.jpg?s=612x612&w=0&k=20&c=lqEIzW3QedZfytsX30NoBJbHxZZbWnlLsvEiwOSbaow="

    #Centering the map
    view_state = pdk.ViewState(
        latitude = filteredData['latitude'].mean(),
        longitude = filteredData['longitude'].mean(),
        zoom = 12,
        pitch = 0,
    )
    #Calculates square root of prices for bubble/icon size. If the icon is bigger, Airbnb is more expensive.
    #[DA1]
    icon_data["price_radius"] = icon_data["price"].apply(lambda price_count: (price_count)**(0.5))

    icon = pdk.Layer(
        "ScatterplotLayer",
        data=icon_data,
        get_icon={'url': icon_url, 'width': 128, 'height': 128, 'anchorY': 128},
        #get_size=30,
        get_position='[longitude, latitude]',
        radius_scale = 8,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_fill_color=[255, 140, 0],
        get_radius = 2, #get_radius = "price_radius",
        size=10,
        pickable=True,
    )
    textLayer =pdk.Layer(
        "TextLayer",
        data = icon_data,
        pickable = False,
        get_position = '[longitude, latitude]',
    )
    tool_tip = {'html': 'Listing:<br/> <b>{name}</b>'
                        '<br/> <b>${price}</b>' '<br/> <b>Rating: {rating}</b>',
                        'style': {'backgroundColor': 'steelblue', 'color': 'white'}}
    map_chart = pdk.Deck(
        map_style = 'mapbox://styles/mapbox/light-v9',
        layers = [icon],
        initial_view_state = view_state,
        tooltip = tool_tip,
    )
    st.pydeck_chart(map_chart)


def pivotTable():
    st.header("Pivot Table")
    st.write("This pivot table shows the median number of days the Airbnb is available throughout the year, "
             "per neighborhood in the Boston region.")
    st.write("")
    #[PY3]
    try:
        df = pd.read_csv("Boston Listings.csv")
        df.dropna(subset=["availability_365", "id", "neighbourhood"], inplace=True)
        #df["rating"] = []
        #df.append(np.random.randint(1, 6, size=len(df)))
        #[DA6]
        pivotT = df.pivot_table("availability_365", index="name", columns="neighbourhood", aggfunc = "median")#.head(10)
        st.write(pivotT)
        #return pivotT
    except FileNotFoundError:
        st.error("error message")


def main():
    df = pd.read_csv("Boston Listings.csv")
    # print(df)
    #[DA7]
    df.drop('neighbourhood_group', axis=1, inplace=True)
    #[DA1]
    df.dropna(inplace=True) #Removes row that have missing/NaN data from the DataFrame
    file_data = df.to_csv(index=False)  # Convert DataFrame to a CSV file

    # print(df.head())
    #df1 = st.dataframe(data=df)

    #[ST4] Side Bar
    page_names_to_functions = {
        "Home": intro,
        "Bar Chart": barChart,
        "Pie Chart": pieChart,
        "Map": mapChart,
        "Scatterplot": scatterplot,
        "Pivot Table": pivotTable,
    }
    calculateNeighbourhoodStats() #[PY1]
    #a function with two arguments, can just call it, don't need to add in the arguments
    #maxPrice, colName, specific neighborhood to filter => calculate max or average price

    st.sidebar.image(image = "Airbnb.jpg", use_container_width= True)
    #[ST4] SIDEBAR
    st.sidebar.title("Page Navigation")
    #[ST3]
    page_selection = st.sidebar.selectbox("Choose a page", page_names_to_functions.keys())
    page_names_to_functions[page_selection]()
    #pivot_table_result = pivotTable()
    #print(pivot_table_result)

main()
