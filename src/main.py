import streamlit as st
import requests

from utils.openai_client import OpenAIWrapper
from utils.last_fm_client import LastFMWrapper


st.write("""
         # WeatherMoody""")

def mood_detector():
    mood = st.select_slider(
    "Choose your mood from 1 to 10 - 1 is Horrible, 10 is is SuperB",
    options=[
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10"
    ],
    )
    st.session_state.mood = mood

def play_sound(sound_file): st.audio(sound_file, format="audio/mpeg", loop=True)

def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def weather_output(city, api_key):
        if st.button("Get Weather"):
            if api_key and city:
                data = get_weather_data(city, api_key)
                if data.get("cod") != 200:
                    st.error("City not found or invalid API key")
                else:
                    st.session_state.weather_data = data
                    st.write(f"### Weather in {city}")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Temperature (°C)", round(data['main']['temp']))
                    col2.metric("Humidity (%)", data['main']['humidity'])
                    col3.metric("Wind Speed (m/s)", data['wind']['speed'])
                    col4.text(f"Weather: {data['weather'][0]['description'].capitalize()}")               
                    
            else:
                st.error("Please enter a valid city name")

class LikeDislikeApp:
    def __init__(self):
        if 'like' not in st.session_state:
            st.session_state.like = False
        if 'dislike' not in st.session_state:
            st.session_state.dislike = False

    def handle_like(self):
        st.session_state.like = True
        st.session_state.dislike = False

    def handle_dislike(self):
        st.session_state.like = False
        st.session_state.dislike = True

    def render(self):
        st.button("Like :+1:", on_click=self.handle_like, key="like_button")
        st.button("Dislike :-1:", on_click=self.handle_dislike, key="dislike_button")

        st.write("Like:", st.session_state.like)
        st.write("Dislike:", st.session_state.dislike)

def main():
    api_key = st.secrets.get('OPEN_WEATHER_MAP_API')
    AZURE_OPENAI_API_KEY = st.secrets.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = st.secrets.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = st.secrets.get('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_LLM_DEPLOYMENT = st.secrets.get('AZURE_OPENAI_LLM_DEPLOYMENT')
    
    openai_wrapper = OpenAIWrapper(
        AZURE_OPENAI_API_KEY,
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_API_VERSION,
        AZURE_OPENAI_LLM_DEPLOYMENT
    )

    city = st.text_input("Enter city name")

    weather_output(city, api_key)

    mood_detector()

    describe_mood = st.text_input("Describe your moody")        

    if st.button("Get Music"):
        weather, temp = st.session_state.weather_data['weather'][0]['description'], st.session_state.weather_data['main']['temp']
        result = openai_wrapper.return_keyword_by_mood_weather(weather, st.session_state.mood , temp, describe_mood)
        title, artist = result.split(' - ')
        title = title.strip()
        
        last_fm_wrapper = LastFMWrapper(st.secrets.get('LAST_FM_API_KEY'))
        
        track = last_fm_wrapper.search_track(title)
        youtube_video_id = last_fm_wrapper.get_youtube_link_id(track['url'])
        st.components.v1.html(
        f"""
            <iframe width="560" height="315" src="https://www.youtube.com/embed/{youtube_video_id}" 
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
            gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """, height=315)

    app = LikeDislikeApp()
    app.render()

    st.subheader("Add some ambient to your moody")

    if st.button("Rain Drops"):
        play_sound("/home/gabor/Downloads/WeatherMoody/sounds/rain.mp3")
    if st.button("River Gurgling"):
        play_sound("/home/gabor/Downloads/WeatherMoody/sounds/river.mp3")
    if st.button("Fire Crackling"):
        play_sound("/home/gabor/Downloads/WeatherMoody/sounds/fire.mp3")
if __name__ == "__main__":
    main()
