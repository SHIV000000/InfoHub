import streamlit as st
import requests
from datetime import datetime
from streamlit_option_menu import option_menu

# Function to fetch weather data
def get_weather(city_name):
    api_key = "6b2e355758d6ffc9cfb3c03f934c4636"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to get weather icon URL
def get_weather_icon_url(icon_id):
    return f"http://openweathermap.org/img/wn/{icon_id}.png"

# Function to display weather information
def display_weather(weather_data):
    if not weather_data:
        return

    if weather_data.get('cod') == 200:
        st.subheader('Current Weather Conditions')
        st.write(f"City: {weather_data['name']}")
        st.write(f"Temperature: {weather_data['main']['temp']}°C")
        st.image(get_weather_icon_url(weather_data['weather'][0]['icon']), caption=weather_data['weather'][0]['description'])
        st.write(f"Weather: {weather_data['weather'][0]['description']}")
        st.write(f"Sunrise: {datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')} UTC")
        st.write(f"Sunset: {datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    elif weather_data.get('cod') == '404':
        st.error("City not found. Please enter a valid city name.")
    else:
        st.error("An error occurred. Please try again later.")

# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    # You can use any currency conversion API or library here
    # For demonstration purposes, this function returns a dummy conversion
    conversion_rate = 1.5  # Dummy conversion rate
    converted_amount = amount * conversion_rate
    return converted_amount

# Function to display currency conversion
def display_currency_conversion():
    st.title('Currency Converter Dashboard')
    amount = st.number_input('Enter amount to convert', min_value=0.01, step=0.01)
    from_currency = st.selectbox('From Currency', ['USD', 'EUR', 'GBP'])
    to_currency = st.selectbox('To Currency', ['USD', 'EUR', 'GBP'])
    if st.button('Convert'):
        converted_amount = convert_currency(amount, from_currency, to_currency)
        st.success(f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')


# Function to fetch COVID-19 data
def get_covid_data():
    # You can use any COVID-19 data source here
    # For demonstration purposes, this function returns dummy data
    data = {
        'total_cases': 1000,
        'total_deaths': 100,
        'total_recovered': 900,
    }
    return data

# Function to display COVID-19 tracker
def display_covid_tracker():
    st.title('COVID-19 Tracker Dashboard')
    covid_data = get_covid_data()
    st.subheader('COVID-19 Statistics')
    st.write(f'Total Cases: {covid_data["total_cases"]}')
    st.write(f'Total Deaths: {covid_data["total_deaths"]}')
    st.write(f'Total Recovered: {covid_data["total_recovered"]}')


dashboard_selection = option_menu(
    menu_title= "MAIN MENU",
    options = ["Weather Forecast", "Currency Converter", "COVID-19 Tracker"],
    icons=["weather", "currency",'covid' ],
    orientation= "horizontal" ,)


# Display selected dashboard
if dashboard_selection == "Weather Forecast":
    st.title('Weather Forecast Dashboard')
    city_name = st.text_input('Enter city name', 'New York')
    weather_data = get_weather(city_name)
    display_weather(weather_data)
elif dashboard_selection == "Currency Converter":
    display_currency_conversion()
elif dashboard_selection == "COVID-19 Tracker":
    display_covid_tracker()
