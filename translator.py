from feedgen.feed import FeedGenerator
import feedparser
from googletrans import Translator
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Timer
from urllib.parse import parse_qs, urlparse

# Function to translate text
def translate_text(text, target_language='en'):
    translator = Translator()
    return translator.translate(text, dest=target_language).text

# Function to fetch and translate RSS feed
def translate_feed(original_feed_url, target_language='en'):
    fg = FeedGenerator()
    original_feed = feedparser.parse(original_feed_url)
    fg.id(original_feed.feed.link)
    
    # Translate and set the title dynamically
    translated_title = translate_text(original_feed.feed.title, target_language)
    fg.title(translated_title)
    
    fg.link(href=original_feed.feed.link)
    fg.description(translate_text(original_feed.feed.description, target_language))
    
    
    for entry in original_feed.entries:
        fe = fg.add_entry()
        fe.id(entry.link)
        fe.title(translate_text(entry.title, target_language))
        fe.description(translate_text(entry.summary, target_language))
    
    return fg.rss_str(pretty=True)

# Global dictionary to hold the cached RSS feeds
cached_rss_feeds = {}

# Function to update a specific cached RSS feed
def update_specific_feed(rss_url):
    print(f"Updating cached RSS feed for {rss_url}...")
    translated_feed = translate_feed(rss_url)
    cached_rss_feeds[rss_url] = translated_feed
    Timer(600, lambda: update_specific_feed(rss_url)).start()

# HTTP Server to serve the translated RSS feed
class RSSRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        query_components = parse_qs(query)
        rss_url = query_components.get('rss_url', [None])[0]
        
        if rss_url:
            if rss_url not in cached_rss_feeds:
                update_specific_feed(rss_url)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/rss+xml')
            self.end_headers()
            self.wfile.write(cached_rss_feeds.get(rss_url, b"RSS feed is being updated, please try again later."))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Missing rss_url parameter.")

# Main function to start the HTTP server
def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RSSRequestHandler)
    print('RSS Translation server is running on port 8080...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
