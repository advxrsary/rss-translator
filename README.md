# RSS Translator Service

## Overview

RSS Translator Service is an enhanced Python-based web server designed to fetch RSS feeds in various languages, translate them into a specified target language, and serve the translated versions. The service supports dynamic titling based on the source and target languages and allows users to specify the translation language through query parameters. It can be easily integrated with Slack or any other RSS reader.

## Features

- Fetches RSS feeds in multiple languages and translates them into a user-specified language.
- Dynamic feed titling to indicate source and destination languages.
- Caches translated feeds for quicker response times, considering both source URL and target language.
- Scalable: Capable of handling multiple RSS feeds.
- Simple HTTP interface: Add your RSS feed URL and desired language as query parameters.
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

4. The service will be running on port 8080 on your server. To consume a specific RSS feed and specify the target language, append the `rss_url` and `dest_lang` query parameters to the server's URL.

    ```
    http://your-server-address:8080/?rss_url=https://example.lt/rss&dest_lang=fr
    ```

5. Add this URL to your Slack RSS bot or any RSS reader to start receiving the translated articles. If `dest_lang` is not provided, it will default to English (`en`).

---

## Advanced Usage

- To change the default language for translations, modify the `target_language` default value in the `translate_feed` function within the `translator.py` file.

- To change the default port, locate the following line in the `run()` function in the `translator.py` file:

    ```python
    server_address = ('', 8080)
    ```
    Change `8080` to your desired port number.
