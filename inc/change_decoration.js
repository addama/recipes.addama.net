var isMobile = /iPhone|iPad|iPod|Android|BlackBerry|webOS|Windows Phone/i.test(navigator.userAgent)
if (isMobile) document.getElementById('decoration').innerHTML = '&hearts;'