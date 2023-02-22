var map;
function createMap(div, lat, lon, depth) {
    //'map'
    map = L.map(div).setView([lat, lon], depth);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
}

function getColour(colour) {
    const tags = {
        'Technology': "blue",
        'entertainment': 'red',
        'Fitness': "red",
        'Smart home' : "red", 
        "Music": "red",
        "Security": "blue", 
        "Medical": "grey", 
        "Analytics": "blue", 
        "Storage": "blue", 
        "automotive": "yellow", 
        "Household": "red" 
      };

      return tags[colour];
}