# RSS Translator Service

## Overview

RSS Translator Service is a Python-based web server designed to fetch Lithuanian RSS feeds, translate them into English, and serve the translated versions. The service is built with scalability in mind, capable of handling multiple RSS feeds. It translates them either on-the-fly or serves them from a cache for quicker response times. The service can be integrated seamlessly with Slack or any other RSS reader that requires the feeds to be in English.

## Features

- Fetches Lithuanian RSS feeds and translates them into English.
- Caches translated feeds to improve performance.
- Scalable: Capable of handling multiple RSS feeds.
- Simple HTTP interface: Add your RSS feed URL as a query parameter.
- Easy integration with Slack or any other RSS reader.

## Requirements

- Python 3.x
- `feedparser` Python package
- `googletrans` Python package
- `feedgen` Python package

To install the required Python packages, run the following command:

```bash
pip install feedparser googletrans feedgen
```

## How to Use

1. Clone this repository to your server.

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory.

    ```bash
    cd rss-translator
    ```

3. Run the Python server script.

    ```bash
    python translator.py
    ```

4. The service will be running on port 8080 on your server. To consume a specific RSS feed, append the `rss_url` query parameter to the server's URL.

    ```
    http://your-server-address:8080/?rss_url=https://example.lt/rss
    ```

5. Add this URL to your Slack RSS bot or any RSS reader to start receiving the translated articles.