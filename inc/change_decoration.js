// Change fleuron UNICODE symbol to the much more widely implemented hearts symbol on mobile
var isMobile = /iPhone|iPad|iPod|Android|BlackBerry|webOS|Windows Phone/i.test(navigator.userAgent)
if (isMobile) document.getElementById('decoration').innerHTML = '&hearts;'