
import dotenv
import os

from utils.openai_client import OpenAIWrapper

dotenv.load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
AZURE_OPENAI_LLM_DEPLOYMENT = os.getenv('AZURE_OPENAI_LLM_DEPLOYMENT')

wrapper = OpenAIWrapper(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_LLM_DEPLOYMENT
)

print(wrapper.return_keyword_by_mood_weather('Rainy', 'Energetics, Motivated'))