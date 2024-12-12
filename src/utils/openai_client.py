from openai import AzureOpenAI

class OpenAIWrapper:
    def __init__(self, api_key, endpoint, api_version, deployment):
        
        self.openai_client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
            azure_deployment=deployment
        )
        
    def return_keyword_by_mood_weather(self, weather, mood):
        completion = self.openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                    You are a specialized assistant for generating YouTube search keywords for popular and specific music tracks. 
                    Based on the given weather and user mood, suggest exactly three keywords that reference artists, song titles, or well-known 
                    genres that match the context. Ensure the keywords will likely lead to individual songs by artists or trending music. 
                    Do not use generic terms like 'playlist' or 'beats.' 
                    Provide results separated by commas, without comments or explanations."""},
            {"role": "user", "content": f"Currently the weather is {weather} and the mood of the user is {mood}"}
        ],
        max_tokens=50
        )

        return completion.choices[0].message.content
