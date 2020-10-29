# speech-img-vid-generator

This does a few things together

1. Audio input
2. Google speech to text API call
3. Bing image request HTML scrape (because Google hates scraping)
4. Download images and arrange into collage (1280x720)
5. Create frames for video following timecode of words
6. Generate video file w/ ffmpeg

# To Run

You need a Google Service Account for the API.
https://cloud.google.com/speech-to-text/docs/libraries

You may need to pip install the libraries you dont have.

Then, run python3 handler.py
