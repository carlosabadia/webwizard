import openai
import os

_client = None
_client_async = None

def get_openai_client():
    global _client
    if _client is None:
        _client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    return _client

def get_openai_client_async():
    global _client_async
    if _client_async is None:
        _client_async = openai.AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    return _client_async