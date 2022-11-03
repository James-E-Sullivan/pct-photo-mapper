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
  
// get exif data from current image
function getExif(image) {
    EXIF.getData(image, () => {
        let allMetaData = EXIF.getTag(this, "Flash");
        console.log(allMetaData);
    })
}

// Get object containing currently loaded/selected image
function getCurrentImage() {
    return document.getElementById('pct-photo');
}

const EXIF = window.EXIF;

window.initMap = initMap;
let currentImage = getCurrentImage();
window.onload=getExif(currentImage);