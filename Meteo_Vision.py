import streamlit as st
import speech_recognition as sr
import requests

# Fonction pour la reconnaissance vocale
def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Parlez maintenant...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio, language="fr-FR")
        st.write(f"Vous avez dit : {text}")
        return text
    except sr.UnknownValueError:
        st.write("Impossible de reconnaître la parole.")
        return ""
    except sr.RequestError as e:
        st.write(f"Erreur lors de la demande de reconnaissance vocale : {e}")
        return ""

# Fonction pour obtenir les informations météorologiques
def get_weather_data(url):
    response = requests.get(url)
    data = response.json()
    import dtale
    dtale.show(data)
    
    if response.status_code == 200:
        return data
    else:
        st.write("Erreur lors de la récupération des données météorologiques.")
        return None

# Interface utilisateur Streamlit
st.title("ChatBot MeteoVision")

# Demande à l'utilisateur de parler
st.write("Appuyez sur le bouton 'Démarrer' et parlez...")
if st.button("Démarrer"):
    text_input = get_speech_input()
    if text_input:
        url = "http://api.openweathermap.org/data/2.5/forecast?lat=14.6937&lon=-17.4441&cnt=200&lang=fr&units=metric&appid=cc111499c1a4174dd8ba752247c6001c"
        weather_data = get_weather_data(url)
        if weather_data:
            st.write("Prévisions météorologiques :")
            for forecast in weather_data['list']:
                date_time = forecast['dt_txt']
                temperature = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                st.write(f"Date/Heure : {date_time}")
                st.write(f"Température : {temperature}°C")
                st.write(f"Description : {description}")
                st.write("-------")