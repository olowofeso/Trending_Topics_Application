from flask import Flask, render_template, jsonify
import praw
from datetime import datetime, timedelta
import prawcore

app = Flask(__name__)

# Reddit API credentials (verify these match your app)
CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = '' 

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def search_trending_products():
    subreddits = ['cheap', 'deals', 'shopping', 'productreviews', '99off', 'gadgets', 'sale', 'clearancesale', 'sales', 'clearance', 'walmart', 'gaming']
    trending_products = []
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for submission in subreddit.top(time_filter='week', limit=10):  # Reduced limit for testing
                product_info = {
                    'title': submission.title,
                    'url': submission.url,
                    'score': submission.score,
                    'subreddit': subreddit_name,
                    'created_utc': submission.created_utc
                }
                trending_products.append(product_info)
                
        except prawcore.exceptions.Forbidden:
            print(f"Access denied to r/{subreddit_name}. Skipping...")  
        except prawcore.exceptions.NotFound:
            print(f"r/{subreddit_name} not found. Skipping...")
        except prawcore.exceptions.ResponseException as e:
            print(f"API error: {e}. Skipping r/{subreddit_name}")

    trending_products.sort(key=lambda x: x['score'], reverse=True)
    return trending_products[:30]  # Return top 30 results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trending')
def trending():
    try:
        trending_products = search_trending_products()
        return jsonify(trending_products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)