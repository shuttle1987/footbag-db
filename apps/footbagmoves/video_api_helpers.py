"""Helper functions for the video APIs we are using in the project"""
__all__ = ['extract_first_yt_url', 'extract_yt_id']

from urlparse import urlparse, parse_qs

from .constants import YOUTUBE_VIDEO_TYPE

def extract_first_yt_url(demo_vids, tutorial_vids):
    """Extract the first youtube url from the demo or tutorial videos.
    For use in loading the first youtube video when the page loads.
    Searches through the demo videos first then the tutorial videos second.
    TODO: perhaps make this search based on video ratings."""
    for video in demo_vids:
        if video.video_type == YOUTUBE_VIDEO_TYPE:
            return video.URL

    for video in tutorial_vids:
        if video.video_type == YOUTUBE_VIDEO_TYPE:
            return video.URL

def extract_yt_id(youtube_url):
    """Extract the youtube video ID from a complete URL.
    Inspired by http://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python

    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def is_youtube_video(youtube_url):
    """Returns true if the video is a youtube link and false otherwise"""
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return True
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return True
        if query.path[:7] == '/embed/':
            return True
        if query.path[:3] == '/v/':
            return True
    # fail?
    return False
