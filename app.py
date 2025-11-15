import requests
import time
import csv

# REAL RapidAPI key (replace this with your key)
scraptik_apikey = "f01a509558mshfbf6bce6d82a50fp13ef9bjsn702ba6d9c194"

# TikTok secUid (NOT user_id)
secUid = "MS4wLjABAAAAqB08cUbXaDWqbD6MCga2RbGTuhfO2EsHayBYx08NDrN7IE3jQuRDNNN6YwyfH6_6"

fieldnames = [
    'unique_id',
    'uid',
    'region',
    'language',
    'following_count',
    'follower_count',
    'favoriting_count',
    'ins_id',
    'youtube_channel_id',
    'youtube_channel_title',
    'twitter_id',
    'twitter_name'
]

# Write CSV header
with open('data.csv', 'w', encoding="utf-8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

def get_followers(secUid, cursor=0):
    try:
        url = "https://scraptik.p.rapidapi.com/user/followers"

        querystring = {
            "secUid": secUid,
            "cursor": str(cursor),
            "count": "2000"
        }

        headers = {
            "x-rapidapi-key": scraptik_apikey,
            "x-rapidapi-host": "scraptik.p.rapidapi.com"
        }

        r = requests.get(url, headers=headers, params=querystring).json()

        data = r.get("data", {})
        followers = data.get("followers", [])
        has_more = data.get("hasMore", False)
        next_cursor = data.get("cursor", 0)

        # Save followers
        with open('data.csv', 'a', encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for u in followers:
                row = {k: u.get(k, "") for k in fieldnames}
                writer.writerow(row)

        # Pagination
        if has_more:
            get_followers(secUid, next_cursor)

    except Exception as e:
        print("Error:", e)

# Start download
get_followers(secUid)
