import os
import json

from openai import OpenAI

# Automatically locates .env file and retrieves API key
# Obviously .env should be in .gitignore
client = OpenAI()

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    """
    Given a specific prompt, returns response from the LLM using OpenAI API.

    Arguments:
        messages (str): text containing prompt and specific message
        model (str): specifies which LLM to use
        temperature (float): value in [0, 1] controlling the model's creativity
        max_tokens (int): maximum number of tokens (message + response). 1 token ~ 1 word and cost of using the API is calculated per token.

    Returns:
        response (str): text containing the LLM's response to the message
    """
    response = client.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
    return response.choices[0].message.content

def get_tags(data, system_message, delimiter="####"):
    """
    Given processed data and formatted prompt, extracts required information from the LLM's response.

    Arguments:
        data (pd.DataFrame): dataframe after having called processing function
        system_message (str): prompt, asking the model to return a json file with keys "topic" and "location"
        delimiter (str): sequence of characters to isolate the specific message in the prompt

    Returns:
        result_data (pd.DataFrame): dataframe with added one-hot columns for all identified tags
        list_of_locations (list): list containing all Russian or Ukrainian locations mentioned in the specific message
    """
    list_of_locations = []
    for index, row in data.iterrows():
        # Retrieve text
        prigozhin_text = row["text"]
        # Retrieve LLM's response in JSON format
        message = [{"role": "system", "content": system_message},    
                   {"role": "user", "content": f"{delimiter}{prigozhin_text}{delimiter}"}] 
        json_string = get_completion_from_messages(message)
        # Retrieve topic and location tags
        tags_dict = json.loads(json_string)
        topics = tags_dict.get("topic", [])
        locations = tags_dict.get("location", [])
        # Update dataframe with identified topic tags
        for topic in topics:
            if topic not in data.columns:
                data[topic] = 0  # Initialize with 0 for all rows
            data.loc[index, topic] = 1  # Set to 1 if the tag has been identified in the text
        # Update list of locations
        for location in locations:
            list_of_locations.append(location)
    return data, list_of_locations

