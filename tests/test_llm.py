import pytest
import openai
import pandas as pd

from openai import OpenAI
from src.helper_functions import llm

client = OpenAI()

# Not proper way to test a LLM for consistency, there are specific libraries!
def test_get_tags():
    delimiter = "####"
    system_message = f"""
        You are provided with a message delimited by {delimiter} characters. \
        You are required to assign to the message topic and location tags. \
        Provide your output in json format with the keys: "topic", "location". Each key contains a list of assigned tags. \
        You can assign multiple tags. If none are identified, return []. You can only use the tags specified below. \
        
        Topic tags:
        good_weather, bad_weather

        Location tags:
        list of geographical locations mentioned in the message
        """
    data = pd.DataFrame({"id": [1], "text": ["It's raining cats and dogs in Kiev!"]})
    res, list_of_locations = llm.get_tags(data, system_message, delimiter)
    expected_res = pd.DataFrame({"id": [1], "text": ["It's raining cats and dogs in Kiev!"], "bad_weather": [1]})
    assert (res.equals(expected_res)) and (list_of_locations == ["Kiev"])
