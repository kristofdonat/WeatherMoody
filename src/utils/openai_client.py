from openai import AzureOpenAI

class OpenAIWrapper:
    def __init__(self, api_key, endpoint, api_version, deployment):
        
        self.openai_client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
            azure_deployment=deployment
        )
        
    def return_keyword_by_mood_weather(self, weather, mood, temp, describe_mood):
        completion = self.openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a specialized assistant for finding specific music tracks. 
                    Based on the given weather and user mood  (1 is bad, 10 is superb), suggest exactly one well-known song title and artist 
                    that best matches the context. Ensure the suggestion is a concrete track and avoid vague or overly broad results.
                    Provide the result as 'Song Title - Artist' without comments or explanations.
                """
            },
            {
                "role": "user",
                "content": f"""
                    Currently the weather is {weather} ({temp} celsius degrees) and the mood of the user is {mood}
                    """ + (f" and the user described the mood as {describe_mood}" if describe_mood else "")
            }
        ],
        max_tokens=50
        )

        return completion.choices[0].message.content
