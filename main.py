import sqlite3
import facebook
from extract_locations import extract_locations
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('posts.db')
c = conn.cursor()

# Create the posts table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (name TEXT, surname TEXT, location TEXT, post_date TEXT)''')

# Connect to the Facebook group using the Facebook API
user_access_token = 'EAA0ec7kxuKkBAG57kcHYEuKwpoQU8wY0bMxv1XZBeQYHSkPaxetUX35ySLL8Ks4j4VpEERI8emFaVA2MrTgaoDn3syqpP61u9De2MG0ry6zXoXEb9nf1N9I3ep7sxCWhDNHITUE0ouFT1QVZBAMVqH8zwBu45UuZC5WWStTtqbFIlp1xOo5'
graph = facebook.GraphAPI(access_token=user_access_token, version='3.0')
group_id = '1498366080695635'
group_posts = graph.get_connections(group_id, 'feed')

# Loop through each post in the group
for post in group_posts['data']:
    # Extract the post text
    post_text = post['message']
    # Find all geo locations mentioned in the post text
    geo_matches = extract_locations(post_text)
    # Extract the author's name and surname from the post
    author_name = post['from']['name']
    author_surname = author_name.split()[-1]
    # Extract the post date
    post_date = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
    # Loop through each geo location mentioned in the post
    for location in geo_matches:
        # Insert the extracted information into the SQLite database
        c.execute("INSERT INTO posts (name, surname, location, post_date) VALUES (?, ?, ?, ?)", (author_name, author_surname, location, post_date))
        conn.commit()

# Close the database connection
conn.close()
