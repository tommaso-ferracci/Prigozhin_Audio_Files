import pandas as pd

from ..helper_functions.geography import * 

def processing_input(data):
    """
    Processes dataframe read from prigozhin_audio_files_en.csv, modifying date to YYYY-MM-DD format, 
    joining all sentences with same id and date (so from the same audio file) and sorting by date.

    Arguments:
        data (pd.DataFrame): dataframe read from prigozhin_audio_files_en.csv

    Returns:
        processed_data (pd.DataFrame): processed dataframe
    """
    processed_data = data[["id", "datetime", "text"]].copy()
    # Cast full date to YYYY-MM-DD format
    processed_data["date"] = pd.to_datetime(processed_data["datetime"]).dt.date
    processed_data = processed_data.drop(columns=["datetime"])
    # Group same audio files and merge sentences
    processed_data = processed_data.groupby(["id", "date"])["text"].agg(lambda sentences: " ".join(sentences))
    processed_data = processed_data.reset_index()
    # Sort by date (ascending)
    processed_data = processed_data.sort_values(by="date")
    return processed_data

def processing_result_for_hist(data):
    """
    Processes dataframe read from res_data.csv counting the weekly number of complaints of each kind.

    Arguments:
        data (pd.DataFrame): dataframe read from res_data.csv

    Returns:
        weekly_data (pd.DataFrame): processed dataframe with weekly complaints count
    """
    # drop columns not needed for histogram
    data = data.drop(columns=["id", "text"])
    # Simplify column names
    data.columns = ["date", "general_complaint", "specific_complaint"]
    # Cast "date" column to datetime object
    data["date"] = pd.to_datetime(data["date"])
    # Set index and resample weekly
    data = data.set_index("date")
    weekly_data = data[["general_complaint", "specific_complaint"]].resample("W").sum()
    return weekly_data

def processing_result_for_map(data):
    """
    Processes dataframe read from loc_data.csv to manually clean location names and get coordinates.

    Arguments:
        data (pd.Series): series read from loc_data.csv

    Returns:
        data (pd.DataFrame): cleaned location names with latitude and longitude
    """
    data.columns = ["name"]
    # Manually fix most incorrect names
    data["name"] = data["name"].apply(correct_names)
    # Retrieve latitude and longitude and add respective columns
    data["latitude"], data["longitude"] = zip(*data["name"].apply(lambda x: get_coordinates(x)))
    return data
