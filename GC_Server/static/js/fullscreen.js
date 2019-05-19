window.onload(function(){
    if (docV.requestFullscreen)
    docV.requestFullscreen();
else if (docV.webkitRequestFullscreen) // Chrome, Safari (webkit)
    docV.webkitRequestFullscreen();
else if (docV.mozRequestFullScreen) // Firefox
    docV.mozRequestFullScreen();
else if (docV.msRequestFullscreen) // IE or Edge
    docV.msRequestFullscreen();
});