import os
import openai
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from src.data_cleaning.processing import processing_input
from src.helper_functions.llm import get_tags

data = pd.read_csv("data/raw/prigozhin_audio_files_en.csv")

delimiter = "####"
system_message = f"""
You are provided with transcribed audio messages from Yevgeny Prigozhin. \
Each text query is delimited with {delimiter} characters. \
You are required to assign to each query topic and location tags. \
Provide your output in json format with the keys: "topic", "location". Each key contains a list of assigned tags. \
You can assign multiple tags. If none are identified, return []. You can only use the tags specified below. \

Topic tags: 
generic complaint about situation at the front,
specific complaint mentioning Shoigu or Gerasimov. \
Remember, no other topic tags are allowed outside of these two. \

Location tags:
list of cities, towns and villages (not geographic regions!) in Ukraine or Russia mentioned in the query. \
There might be spelling mistakes, fix them (example: Bahmut --> Bakhmut). \
If the Russian name of a city is used, report the Ukrainian name (example: Artemovsk --> Bakhmut). \
Report only locations in  or Russia! (example: Khartoum --> []). \

Example of what you should do: \
query:
{delimiter}
Because of severe incompetence of the Minister of Defense, Ukrainians have recaptured Neskuchne. 
In spite of this, we have been successful in advancing in the Bahmut direction.
{delimiter}
return:
{{
    "primary": ["specific complaint mentioning Shoigu or Gerasimov"],
    "location": ["Neskuchne", "Bakhmut"]
}}
"""

processed_data = processing_input(data)
res_data, list_of_locations = get_tags(processed_data, system_message, delimiter)
loc_data = pd.Series(list_of_locations)
# When the analysis is partly performed by a LLM, it is clear that reproducibility will be limited.
# By carefully engineering the prompt and setting the temperature at 0 results should be fairly consistent.
# However, results are saved in .csv files to guarantee complete reproducibility of the analysis from now on.
res_data.to_csv("data/derived/res_data.csv")
loc_data.to_csv("data/derived/loc_data.csv")

