//This script loads the youtube IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

//This function calls the youtube_ready function after the youtube API code downloads.
function onYouTubeIframeAPIReady() {
    youtube_ready();
}

//The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.playVideo();
}

/*Extract youtube ID from a complete youtube link.
Formats supported:

    latest short format: http://youtu.be/-E1DwhGH8FE
    nocookie domain: http://www.youtube-nocookie.com
    iframe: http://www.youtube.com/embed/-E1DwhGH8FE
    iframe (secure): https://www.youtube.com/embed/-E1DwhGH8FE
    object param: http://www.youtube.com/v/-E1DwhGH8FE?fs=1&hl=en_US
    object embed: http://www.youtube.com/v/-E1DwhGH8FE?fs=1&hl=en_US
    watch: http://www.youtube.com/watch?v=-E1DwhGH8FE
    any/subdomain/too: http://gdata.youtube.com/feeds/api/videos/-E1DwhGH8FE
    more params: http://www.youtube.com/watch?v=-E1DwhGH8FE&feature=g-vrec
    query may have dot: http://www.youtube.com/watch?v=-E1DwhGH8FE&feature=youtu.be

ID for the video is assumed to be exactly 11 characters long.

Regex solution based on http://stackoverflow.com/questions/5830387/
*/
function extractYouTubeID(url_text) {
    var re = /https?:\/\/(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\S*[^\w\s-])([\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['"][^<>]*>|<\/a>))[?=&+%\w.-]*/ig;
    var id_match = re.exec(url_text);
    return id_match[1];
}
