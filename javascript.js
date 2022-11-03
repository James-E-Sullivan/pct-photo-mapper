// Initialize and add the map
function initMap() {
    // The location of South Lake Tahoe
    const tahoe = { lat: 38.918, lng: -120.001 };
    // The map, centered at South Lake Tahoe
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: tahoe,
    });
    // The marker, positioned at South Lake Tahoe
    const marker = new google.maps.Marker({
      position: tahoe,
      map: map,
    });
}
  

// Get object containing currently loaded/selected image
function getCurrentImage() {
    return document.getElementById('pct-photo');
}


window.initMap = initMap;
let currentImage = getCurrentImage();