import feedparser
import sys
from datetime import datetime, timedelta
from urllib.parse import quote_plus

# Check if the number of days was provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python arxiv_search.py <number_of_days>")
    sys.exit(1)

# Try to convert the provided argument to an integer
try:
    number_of_days = int(sys.argv[1])
except ValueError:
    print("The number of days must be an integer.")
    sys.exit(1)

# Define your search keyword(s) here
keywords = ["planning", "multi-robot", "MPC", "robotics", "robot-learning"]

# Calculate the date N days ago in YYYYMMDD format
n_days_ago = (datetime.now() - timedelta(number_of_days)).strftime('%Y%m%d')

# Construct the query string for arXiv API using 'OR' to combine keywords
query = ' OR '.join(f'all:{kw}' for kw in keywords)
query += f' AND submittedDate:[{n_days_ago} TO {datetime.now().strftime("%Y%m%d")}]'


# URL encode the query
encoded_query = quote_plus(query)

# The max_results parameter is set to 10, you can increase this if needed
url = f'http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results=10'

# Fetch the feed data
feed = feedparser.parse(url)

# Check if the feed entries exist
if feed.entries:
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Authors: {', '.join(author.name for author in entry.authors)}")
        print(f"Abstract: {entry.summary}")
        print(f"Link: {entry.id}\n")
else:
    print("No papers found for the given query.")

# Save this to a file named `arxiv_search.py` and run it using `python arxiv_search.py <number_of_days>`.

