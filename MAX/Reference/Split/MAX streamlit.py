import streamlit as st
import speech_recognition as sr
import pyttsx3
import pywhatkit as kit
import re
from streamlit_chat import message
from MAX_chatbot_logic import MAXAssistant

class MAXStreamlitApp:
    def __init__(self, api_key):
        """
        Initialize the Streamlit application for MAX Assistant
        
        Args:
            api_key (str): Google Gemini API key
        """
        # Set up Streamlit page configuration
        st.set_page_config(page_title="MAX - Student's Personal Assistant", layout="wide")
        
        # Initialize the MAX Assistant
        self.assistant = MAXAssistant(api_key)
        
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self._setup_tts_voice()
    
    def _setup_tts_voice(self):
        """
        Set up text-to-speech with a female voice if available
        """
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def _clean_text(self, text):
        """
        Clean text by removing special characters
        
        Args:
            text (str): Input text
        
        Returns:
            str: Cleaned text
        """
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    def _speak(self, text):
        """
        Convert text to speech
        
        Args:
            text (str): Text to be spoken
        """
        cleaned_text = self._clean_text(text)
        try:
            self.tts_engine.say(cleaned_text)
            self.tts_engine.runAndWait()
        except RuntimeError as e:
            if str(e) == 'run loop already started':
                pass
    
    def _send_whatsapp_message(self, message_text):
        """
        Send a WhatsApp message
        
        Args:
            message_text (str): Message to send
        """
        try:
            _, phone_number, *message_parts = message_text.split()
            message_to_send = ' '.join(message_parts)
            kit.sendwhatmsg_instantly(phone_number, message_to_send)
            st.success(f"Message sent to {phone_number}!")
        except Exception as e:
            st.error(f"Failed to send WhatsApp message: {e}")
    
    def _handle_voice_input(self):
        """
        Handle voice input from the user
        """
        with sr.Microphone() as source:
            st.write("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                user_query = self.recognizer.recognize_google(audio)
                st.write(f"You said: {user_query}")
                return user_query
            except sr.UnknownValueError:
                st.error("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                st.error("Sorry, there was an error with the speech recognition service.")
                return None
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                return None
    
    def run(self):
        """
        Run the Streamlit application
        """
        # Sidebar with app information
        with st.sidebar:
            st.title("MAX - The Assistant")
            st.markdown("You can ask MAX anything here.")
            st.markdown("### About")
            st.markdown("MAX is your friendly assistant to help with student tasks!")

        # Main title
        st.title("MAX - Student's Personal Assistant")

        # Initialize messages in session state
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
            introduction_text = self.assistant.get_introduction()
            st.session_state["messages"].append({"role": "assistant", "content": introduction_text})
            self._speak(introduction_text)

        # Display existing messages
        for i, message_dict in enumerate(st.session_state["messages"]):
            if message_dict["role"] == "user":
                message(message_dict["content"], is_user=True, key=str(i))
            else:
                message(message_dict["content"], key=str(i))

        # Voice input button
        if st.button("🎤"):
            user_query = self._handle_voice_input()
            if user_query:
                # Process voice input
                st.session_state["messages"].append({"role": "user", "content": user_query})
                response_text = self.assistant.send_message(user_query)
                st.session_state["messages"].append({"role": "assistant", "content": response_text})
                message(user_query, is_user=True)
                message(response_text)
                self._speak(response_text)

        # Text input
        user_text = st.chat_input("Type your message or click the microphone button to speak:")
        if user_text:
            if user_text.startswith("send whatsapp"):
                self._send_whatsapp_message(user_text)
            else:
                # Process text input
                st.session_state["messages"].append({"role": "user", "content": user_text})
                response_text = self.assistant.send_message(user_text)
                st.session_state["messages"].append({"role": "assistant", "content": response_text})
                message(user_text, is_user=True)
                message(response_text)
                self._speak(response_text)

        # Quit button
        if st.button("Quit"):
            st.write("Thanks for using MAX!")

def main():
    # Replace with your actual Gemini API key
    api_key = "AIzaSyBrt8SRJ0kn8ySTQ5EEHVfBGM7NhGUk53s"
    app = MAXStreamlitApp(api_key)
    app.run()

if __name__ == "__main__":
    main()