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
