"""
RSS Translator Service: An HTTP server for translating RSS feeds.
Fetches RSS feeds in multiple languages, translates them to a specified language, and serves them.
Supports caching and dynamic titling.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Timer
from urllib.parse import parse_qs, urlparse
from feedgen.feed import FeedGenerator
import feedparser
from googletrans import Translator

# Global dictionary to hold the cached RSS feeds
CACHED_RSS_FEEDS = {}

def translate_text(text, target_language='en'):
    """Translate text to a target language."""
    translator = Translator()
    return translator.translate(text, dest=target_language).text

def detect_language(text):
    """Detect the language of a text."""
    translator = Translator()
    return translator.detect(text).lang.upper()

def update_specific_feed(rss_url, dest_lang):
    """Update a specific cached RSS feed."""
    print(f"Updating cached RSS feed for {rss_url}...")
    translated_feed = translate_feed(rss_url, dest_lang)
    CACHED_RSS_FEEDS[rss_url] = translated_feed
    Timer(600, lambda: update_specific_feed(rss_url, dest_lang)).start()

def translate_feed(original_feed_url, target_language='en'):
    """Fetch and translate an RSS feed."""
    feed_gen = FeedGenerator()
    original_feed = feedparser.parse(original_feed_url)
    feed_gen.id(original_feed.feed.link)

    detected_language = detect_language(original_feed.feed.title)
    domain_parts = urlparse(original_feed_url).netloc.split('.')
    main_domain = (
        domain_parts[-2].capitalize() if len(domain_parts) > 1
        else domain_parts[0].capitalize()
    )

    translated_title = f"{main_domain} {detected_language}->{target_language.upper()}"
    feed_gen.title(translated_title)
    feed_gen.link(href=original_feed.feed.link)
    feed_gen.description(translate_text(original_feed.feed.description, target_language))

    for entry in original_feed.entries:
        entry_fe = feed_gen.add_entry()
        entry_fe.id(entry.link)
        entry_fe.title(translate_text(entry.title, target_language))
        entry_fe.description(translate_text(entry.summary, target_language))

    return feed_gen.rss_str(pretty=True)

class RSSRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request handler class."""
    def do_GET(self):
        """Handle GET requests."""
        query = urlparse(self.path).query
        query_components = parse_qs(query)
        rss_url = query_components.get('rss_url', [None])[0]
        dest_lang = query_components.get('dest_lang', ['en'])[0]

        if rss_url:
            if rss_url not in CACHED_RSS_FEEDS:
                update_specific_feed(rss_url, dest_lang)
            self.send_response(200)
            self.send_header('Content-type', 'application/rss+xml')
            self.end_headers()
            self.wfile.write(
                CACHED_RSS_FEEDS.get(
                    rss_url, b"RSS feed is being updated, please try again later."
                )
            )
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Missing rss_url parameter.")

def run():
    """Start the HTTP server."""
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RSSRequestHandler)
    print('RSS Translation server is running on port 8080...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
