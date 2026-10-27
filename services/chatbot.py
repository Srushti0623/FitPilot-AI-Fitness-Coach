
from google import genai


MODEL_NAME = "gemini-3.6-flash"

SYSTEM_PROMPT = """
You are FitPilot, a friendly AI fitness coaching assistant.

Your responsibilities:
- Answer questions about exercise, workout planning,
  warm-ups, cool-downs, rest and recovery.
- Give general healthy-eating and hydration guidance.
- Explain fitness concepts in simple beginner-friendly language.
- Use the user's fitness profile when it is provided.
- Keep answers practical, supportive and reasonably concise.

Safety rules:
- Do not diagnose diseases or prescribe medicines.
- Do not recommend extreme dieting or unsafe exercise.
- Remind users to stop exercising if they experience chest pain,
  fainting, severe dizziness or unusual breathing difficulty
  and seek appropriate medical help.
- Do not claim that your recommendations replace a doctor
  or qualified fitness professional.
- Be honest when information is uncertain.
- You are a general fitness assistant, not an emergency service.
"""


def get_fitness_reply(api_key, messages, profile):
    """Send recent chat messages to Gemini and return its answer."""

    if not api_key:
        return (
            "Gemini API key is missing. Add GEMINI_API_KEY "
            "to .streamlit/secrets.toml and restart the app."
        )

    if not messages:
        return "Hello! I'm FitPilot. How can I help with your fitness goals?"

    profile_text = (
        f"Age: {profile.get('age', 'Not provided')}\n"
        f"Weight: {profile.get('weight', 'Not provided')} kg\n"
        f"Goal: {profile.get('goal', 'Not provided')}\n"
        f"Experience: {profile.get('level', 'Not provided')}\n"
        f"Environment: {profile.get('environment', 'Not provided')}\n"
        f"Workout duration: {profile.get('duration', 'Not provided')} minutes"
    )

    conversation = []
    for message in messages[-12:]:
        role = "User" if message["role"] == "user" else "FitPilot"
        conversation.append(f"{role}: {message['content']}")

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"User's fitness profile:\n{profile_text}\n\n"
        "Conversation so far:\n"
        + "\n".join(conversation)
        + "\n\nReply to the user's latest message."
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        if response.text:
            return response.text.strip()

        return "I couldn't generate a response. Please try again."

    except Exception as error:
        error_message = str(error).lower()

        if "api_key" in error_message or "api key" in error_message:
            return "The API key may be invalid. Check your Streamlit secrets file."

        if "429" in error_message or "quota" in error_message:
            return (
                "The Gemini API usage limit may have been reached. "
                "Please wait and try again later, or check your free-tier quota."
            )

        if "404" in error_message or "not found" in error_message:
            return (
                "The selected Gemini model may not be available for your API key. "
                "Check the current model list in Google AI Studio and update "
                "MODEL_NAME in services/chatbot.py."
            )

        return (
            "I couldn't connect to the AI service. Check your internet "
            "connection and API settings, then try again."
        )
