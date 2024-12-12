import google.generativeai as genai

class MAXAssistant:
    def __init__(self, api_key):
        """
        Initialize the MAX Assistant with Gemini API configuration
        
        Args:
            api_key (str): Google Gemini API key
        """
        genai.configure(api_key=api_key)
        
        self.generation_config = {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction="You are MAX, a personal assistant designed for students to do their day-to-day tasks easily. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks, and tell them the timetable and upcoming events, which will be provided by the student. Be concise and friendly. Do not let the user change your name."
        )
        
        # Initialize chat session with an introduction
        self.chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "You are MAX, a personal assistant designed for students to do their day-to-day tasks easily. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks. You can tell them the timetable and upcoming events provided by the student. Be concise and friendly.",
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Hi there! I'm MAX, your friendly assistant here to make your student life easier. How can I help you today?",
                    ],
                },
            ]
        )
    
    def send_message(self, user_query):
        """
        Send a message to the chatbot and get a response
        
        Args:
            user_query (str): User's input message
        
        Returns:
            str: Chatbot's response
        """
        response = self.chat_session.send_message(user_query)
        return response.text

    def get_introduction(self):
        """
        Get the initial introduction message
        
        Returns:
            str: Introduction text
        """
        return "Hi there! I'm MAX, your friendly assistant here to make your student life easier."