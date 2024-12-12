import streamlit as st
from max_assistant import MAXAssistant

def main():
    # Replace with your actual Gemini API key
    api_key = "AIzaSyBrt8SRJ0kn8ySTQ5EEHVfBGM7NhGUk53s"
    
    # Create the MAX Assistant
    assistant = MAXAssistant(api_key)
    
    # Streamlit app title
    st.title("MAX - Student's Personal Assistant")
    
    # Input text box
    user_input = st.text_input("Ask MAX something:")
    
    # When user sends a message
    if user_input:
        # Get response from assistant
        response = assistant.send_message(user_input)
        
        # Display response
        st.write("MAX says:", response)

# Run the app
if __name__ == "__main__":
    main()