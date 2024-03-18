from geopy.geocoders import Nominatim

def get_coordinates(location_name):
    """
    Given string containing a location name, returns latitude and longitude.

    Arguments:
        location_name (str): name of the location to search

    Returns
        latitude (float): latitude of the location (by default EPSG:4326 format)
        longitude (float): lomgitude of the location (by default EPSG:4326 format)
    """
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    if location: # Check location is found
        return location.latitude, location.longitude
    else: # Otherwise return None for both latitude and longitude
        print("Coordinates not found for the location:", location_name)
        return None, None
    
def correct_names(name):
    """
    While the prompt specifically tries to minimize these issues, the LLM still struggles with location names.
    Some have been incorrectly transcribed by whisper, other match several different locations in Ukraine, and to 
    make things worse Prigozhin uses both Ukrainian and Russian names interchangeably (ex. Bakhmut, Artemovsk).
    With some expert knowledge most of the common mistakes can be fixed.

    Arguments:
        name (str): wrong name of the location

    Returns:
        name (str): correct name of the location
    """
    if name == "Solidar":
        name = "Soledar"
    elif (name == "Kresheevka") or (name == "Kleschevka"):
        name = "Klishchiivka"
    elif name == "Praskoveivka":
        name = "Paraskoviivka"
    elif name == "Verkhovka":
        name = "Berkhivka"
    elif (name == "Chasov-Yar") or (name == "Chasov Yar") or (name == "Chastny Yar"):
        name = "Chasiv Yar"
    elif name == "Orekhovo-Vasilyevka":
        name = "Orikhovo-Vasylivka"
    elif name == "Zaliznyaske":
        name = "Zaliznianske"
    elif name == "Popasnaya":
        name = "Popasna"
    elif name == "Sivore":
        name = "Siversk"
    elif name == "Krematorsk":
        name = "Kramatorsk"
    elif name == "Konstantynivka":
        name = "Kostiantynivka"
    elif name == "Krasny Liman":
        name = "Liman"
    elif name == "Urazhaina":
        name = "Urozhaine"
    return name

