#!/usr/bin/env python3
import os
import pandas as pd
import time
import requests
import datetime as dt
import re
import os

from yt_dl import download_music


def create_itunes_query(name):
    query = name[:-4] # remove ".mp3"
    query = "".join([char for char in query if char.isalnum() or char.isspace()])
    return query

def get_mp3_data(dir):
    """Get mp3 files from directory

    Args:
        dir (str): directory containing songs

    Returns:
        pd.DataFrame: mp3 files and paths
    """
    file_path = []
    file_name = []
    dir = os.path.expanduser(dir)
    # mp3s within whole directory
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith(".mp3"):
                file_name.append(name)
                file_path.append(os.path.join(root, name))

    mp3_df = pd.DataFrame({"file_name": file_name, "file_path":file_path})
    mp3_df["query"] = mp3_df.loc[:, "file_name"].apply(
        lambda x: create_itunes_query(x)
    )
    return mp3_df


def _format_query(query):
    # URL encoding: https://www.w3schools.com/tags/ref_urlencode.ASP
    return query

def call_api(query):

    itunes_api = "https://itunes.apple.com/search?"
    # entity - removed, attribute - removed
    query = "Masego Unhinged"
    param_fields = [("term", query), ("country", "US"), ("media", "music"), ("limit", 10), ("lang", "en_us")]
    r = requests.get(itunes_api, params=param_fields)   

    return r.json()['results']

   
def get_album_art(file_name, img_url, artwork_dir="~/Downloads/"):
    """Saves album art in downloads, for usage and moving later

    Args:
        img_url (_type_): _description_
    """
    file_path = os.path.join(os.path.expanduser(artwork_dir), f"file_name.jpeg")
    img_data = requests.get(img_url).content
    with open(os.path.expanduser(file_path), 'wb') as img_handler:
        img_handler.write(img_data)



        
def _is_single(candidate):
    album_fields = ["collectionName"]
    if "collectionName" not in candidate.keys():
        candidate['collectionName'] = f"{candidate['trackName']} - Single"
        candidate['discNumber'] = 1
        candidate['discCount'] = 1
        candidate['trackNumber'] = 1
        candidate['trackCount'] = 1
    return candidate

def format_candidate(candidate):
    """formats candidate information to print for user approval

    Args:
        candidate (dict): api call candidate

    Returns:
        printable custom format
    """
    #result_fields = ["artworkUrl100", "trackTimeMillis", "country", "primaryGenreName"]
    # result_fields = ["trackName", "artistName", "collectionName", "albumArtistName", "releaseDate", "discNumber", "discCount", 
                    #  "trackNumber", "trackCount", "trackTimeMillis", "country", "primaryGenreName"]

    candidate["albumArtistName"] = re.split(r'[,&]', candidate["artistName"])[0]
    candidate = _is_single(candidate)

    custom_format = f"""
    Track:          {candidate["trackName"]}
    Artist:         {candidate["artistName"]}
    Album:          {candidate["collectionName"]}
    Album Artist:   {candidate["albumArtistName"]}
    Genre:          {candidate["primaryGenreName"]}\
    Release Date:   {candidate["releaseDate"]}
    Track Number:   {candidate["trackNumber"]}/{candidate["trackCount"]}
    Disc Number:    {candidate["discNumber"]}/{candidate["discCount"]}
    """
    return custom_format

def _check_manual_format(input_value, metadata=None):
    if metadata in ["discNumber", "trackNumber"]:
        while True:
            parts = input_value.split("/")
            if (len(parts) == 2 and 
                parts[0].strip().isdigit() and 
                parts[1].strip().isdigit()):
                return input_value
            input_value = input("Ensure Format (#/total): ")
    if metadata == "releaseDate":
        while True:
            try:
                dt.strptime(input_value, "%Y/%m/%d")
                return input_value
            except ValueError:
                input_value = input("Ensure Format (YYYY/MM/DD): ")
    return input_value

def manual_metadata():
    attempt_manual = input("Attempy manual query? (y/n) ").strip().lower()
    while attempt_manual not in ['y', 'n']: 
        attempt_manual = input("Type only 'y' or 'n'? (y/n)\nAttempt manual query? (y/n)").strip().lower()
    if attempt_manual == 'y':
        print("Please fill fields (type 'q' at any point to restart):\n")
        trackName = _check_manual_format(input_values=input("Track: "))
        artistName = _check_manual_format(input_values=input("Artist: "))
        collectionName = _check_manual_format(input_values=input("Album: "))
        releaseDate = _check_manual_format("releaseDate", input("Release Date (YYYY/MM/DD): "))
        discNumber = _check_manual_format("discNumber", input("Disc Number (#/total): "))
        trackNumber = _check_manual_format("trackNumber", input("Track Number (#/total): "))
        country = _check_manual_format(input_values=input("Country: "))
        primaryGenreName = _check_manual_format(input_values=input("Genre: "))
    

def select_candidate(candidates):
    """loop and allow user to select correct candidate

    Args:
        candidates (list): list of candidates (ITunes API call results)

    Returns:
        dict: candidate metadata (None if no valid candidate)
    """
    for i in candidates:
        print(format_candidate(i))
        approved = input("Correct Candidate? (y/n) ").strip().lower()
        while approved not in ['y', 'n']:
            approved = input("Type only 'y' or 'n'.\nCorrect candidate? (y/n) ").strip().lower()
        if approved == "y":
            return i           
    return

def main(url, to_tag_dir, tagged_dir):
    # download_music(url, to_tag_dir)
    mp3_data = get_mp3_data(to_tag_dir)
    for i, row in mp3_data.iterrows(): # query each downloaded song
        candidates = call_api(row['query'])
        print(row['query'])
        user_candidate = select_candidate(candidates)
        if not user_candidate:
            # manual_query - need this
            manual_metadata()
    return

if __name__ == "__main__":
    dir = "~/Music/MyMusic/AllMusic/Music"

    start = time.time()

    url = "https://www.youtube.com/watch?v=MaRaF3nBrXg&list=PLcaoz5W3gCd8hzlosZNAl0SssWMbRJvNu"
    to_tag_dir = os.path.expanduser("~/Music/MyMusic/ToBeTagged")
    tagged_dir = os.path.expanduser("~/Music/MyMusic/Tagged")
    main(url, to_tag_dir, tagged_dir)    


    end = time.time()
    print(end-start)