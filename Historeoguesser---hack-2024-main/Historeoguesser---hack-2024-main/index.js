
const poi_list =  [
  { 
    name: "SWEM Library",
    desc: "The Earl Gregg Swem Library, located at the College of William and Mary, is named after Earl Gregg Swem, College Librarian from 1920-1944. It was rated the eighth best library system in the U.S. by the Princeton Review in 2008, based on a survey of 120,000 students from 368 campuses.",
    coords: {lat: 37.2702944, lng: -76.7163559} 
  },
  
  { 
    name: 'Integrated Science Center',
    desc: "The Integrated Science Center (ISC) integrates William & Mary’s science programs, enabling multidisciplinary research. This 100,000 sq. ft. facility houses labs for Applied Science, Biology, Chemistry, Neuroscience, Physics, and Psychology. It's the only campus building with biological and hazardous waste rooms managed by the EH&S Office.",
    coords: {lat: 37.2702364, lng: -76.7144971}
  },
  
  { 
    name: 'Sadler Center',
    desc: "Renamed in honor of Sam Sadler, the Sadler Center is located adjacent to Zable Stadium. This three-story complex includes the largest auditorium on campus, various multi-purpose rooms, a dining hall, student post office, and recreational spaces. The new Cohen Career Center is also nearby.",
    coords: {lat: 37.2718334, lng: -76.7134909}
  },
  
  { 
    name: 'Monroe Hall',
    desc: "Monroe Hall, named for James Monroe, is a co-ed dormitory for freshmen at William & Mary. Constructed in 1924, it initially served as a men’s dormitory and can house 168 students. The building has historical significance, including serving as a residence for Navy chaplains during WWII.",
    coords: {lat: 37.2716826, lng: -76.7103896}
  },
  
  { 
    name: 'Commons Dining Hall',
    desc: "The Commons, or 'Caf', is the only free-standing dining facility at William & Mary. Opened in 1967, it underwent significant renovations in 1987 and 2005. During the latter renovation, a temporary dining tent called 'deCaf' was pitched on Yates Field.",
    coords: {lat: 37.2718533, lng: -76.719333}
  },
  
  { 
    name: 'Green and Gold Village',
    desc: "The Green & Gold Village is a co-ed freshman housing complex at William & Mary, consisting of Griffin, Eagle, and Lion buildings. Accommodating up to 428 residents, it was built between 1965 and 1968 and previously served as the fraternity complex until 2013.",
    coords: {lat: 37.2745679, lng: -76.7171769}
  },
  
  { 
    name: 'Randolph Complex',
    desc: "The Randolph Complex is a cluster of dormitories for upperclassmen at William & Mary, featuring various housing styles. Named for Virginia governors, the complex was completed in 1980 and includes two additional dormitories built in 1988. It has historical significance, including a fire in 2005.",
    coords: {lat: 37.2712101, lng: -76.7195004}
  },
      
  { 
    "name": "Jefferson Hall", 
    "desc": "Constructed between 1920 and 1921, Jefferson Hall was built as a women's dormitory and now houses co-ed upperclassmen. Named for Thomas Jefferson, it opened in September 1921 with amenities like a gymnasium and pool. The building underwent renovations in the late 1970s and was rebuilt after a fire in 1983. It officially reopened in January 1985.",
    "coords": { "lat": 37.2694185, "lng": -76.7101715 }
  },
  
  { 
    "name": "Lemon Hall", 
    "desc": "Lemon Hall is named in honor of Lemon, a man held enslaved by William & Mary. Today, his legacy is remembered through the Lemon Project, which aims to explore and heal the relationship between the university and the African and African-American communities.",
    "coords": { "lat": 37.2681929, "lng": -76.7131253 }
  },
  
  { 
    "name": "Tucker Hall", 
    "desc": "Tucker Hall, originally William & Mary’s first dedicated library, now houses the Department of English. Opened in 1909, it underwent several renovations before becoming Tucker Hall in 1968, named after Revolutionary War veteran St. George Tucker.",
    "coords": { "lat": 37.2716983, "lng": -76.7099414 }
  },
  
  { 
    "name": "One Tribe Place", 
    "desc": "One Tribe Place is a co-ed dormitory for upperclassmen at William & Mary, created from the Hospitality House, acquired in 2013 to meet housing needs. The first residents moved in during the fall of 2013.",
    "coords": { "lat": 37.2741128, "lng": -76.7133839 }
  },
  
  { 
    "name": "Jones Hall", 
    "desc": "Constructed in 1969, Jones Hall houses the Office of Information Technology and the Math department. It was named for Rev. Hugh Jones and features 25 classrooms and various academic departments over its history.",
    "coords": { "lat": 37.267699, "lng": -76.7177079 }
  },
  
  { 
    "name": "Small Hall", 
    "desc": "Completed in 1963 and named for Thomas Jefferson’s mentor, William Small, Small Hall houses the Department of Physics and features a notable observatory. It underwent major renovations, including solar panel installation.",
    "coords": { "lat": 37.2690829, "lng": -76.7174615 }
  },
  
  { 
    "name": "Zable Stadium", 
    "desc": "Zable Stadium, originally Cary Field, is William & Mary's main venue for football and track. It was dedicated in 1990 and named after Walter J. Zable. The stadium has hosted various significant events since its establishment.",
    "coords": { "lat": 37.272925, "lng": -76.7143516 }
  },
  
  { 
    "name": "Kaplan Arena", 
    "desc": "Kaplan Arena, formerly William & Mary Hall, is an 8,600-seat venue for university events, concerts, and athletic competitions. Named in 2005 in honor of Jim and Jane Kaplan, it has hosted many notable performers.",
    "coords": { "lat": 37.2726219, "lng": -76.7199043 }
  },
       
  { 
    "name": "Alan B. Miller Hall", 
    "desc": "Located at the corner of Ukrop Way and Jamestown Road, Miller Hall is home to the Mason School of Business. Construction was completed in 2009, and the hall is named after alumnus Alan B. Miller, a prominent donor. The business school has evolved significantly since its early courses were offered in 1919-1920.",
    "coords": { "lat": 37.2662743, "lng": -76.7177205 }
  },
  
  { 
    "name": "School of Education", 
    "desc": "Established in 1961, the School of Education became a distinct entity at William & Mary. The current building, completed in 2010, centralizes the school's operations, which have included both undergraduate teacher education and various graduate programs since its inception.",
    "coords": { "lat": 37.2785785, "lng": -76.7238843 }
  }, 
  
  { 
    "name": "Sunken Garden", 
    "desc": "The Sunken Garden extends west from the Wren Building and serves as a place for relaxation and recreation. Its design follows the spirit of eighteenth-century English landscape gardens, which abandoned the geometric parterres of Europe in favor of sweeping lawns intended to uplift the spirit by leading the eye toward a distant, natural setting.",
    "coords": { "lat": 37.27082877, "lng": -76.71144537 }
  }, 

  { 
    "name": "James Blair Hall", 
    "desc": "James Blair Hall, known as Marshall-Wythe Hall until 1968, is located on the west end of the Sunken Gardens. It currently houses the Philosophy and History departments as well as some administrative offices. The building is named after James Blair, founder and first President of William & Mary from 1693-1743.",
    "coords": { "lat": 37.27168771, "lng": -76.7118584}
  }, 

  { 
    "name" : "Chancellors Hall", 
    "desc" : " Chancellors Hall, located on the Sunken Gardens between James Blair Hall and Tucker Hall, was formerly named Rogers Hall, Chancellors Hall, then Tyler Hall in 1988 after U.S. President John Tyler and his son, Lyon Gardiner Tyler Sr. In 2021, the Board of Visitor’s approved reverting Tyler Hall back to its previous name of Chancellors Hall. ", 
    "coords": { "lat": 37.27168043, "lng": -76.71083538}
  },   

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  },  

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  },  

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 

    //  { 
    //   "name" : "", 
    //   "desc" : " ", 
    //   "coords": { "lat": , "lng": }
    //  }, 


]


let guess_location;
let random_poi;
let random_location;
let random_name;
let random_desc;

let markers = [];

// Google Maps API setup  
const { Map } = await google.maps.importLibrary("maps");
const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

const myLatLng = { lat: 37.2706829, lng: -76.7159741 };
const map = new Map(document.getElementById("minimap"), {
  center: myLatLng,
  zoom: 16,
  streetViewControl: false,
  mapTypeControl: false,
  fullscreenControl: false,
  zoomControl: false,
  mapId: "4504f8b37365c3d0",
});

let marker = new AdvancedMarkerElement({
  map,
  position: { lat: 37.2706829, lng: -76.7159741 },
});
markers.push(marker); 

// Initialize rndmarker but don't set its map until later
let rndmarker = new AdvancedMarkerElement({
  map: null, // Initially null; it will be set when we reveal the location
});

// Function to initialize the game
function initialize() { 
  if (!random_location) {
    randomize_location(); // Only randomize location once 
  }
  
  clear_markers();
  
  let panorama = new google.maps.StreetViewPanorama(
      document.getElementById("map"),
        {  
          position: random_location,
          linksControl: false,
          panControl: true,
          enableCloseButton: false,
          fullscreenControl: false,
          addressControl: false,
          showRoadLabels: false,
          clickToGo: false,
          zoomControl: false,
          zoomControlOptions: {
              position: google.maps.ControlPosition.TOP_LEFT,
          }
        },
  );

  map.addListener("click", (mapsMouseEvent) => {
      marker.setMap(null);
      guess_location = mapsMouseEvent.latLng;  
      marker = new AdvancedMarkerElement({
          map,
          position: mapsMouseEvent.latLng, 
      });   
      markers.push(marker);  

      
      const checkbox = document.getElementById("myCheckbox");
      const label = document.getElementById("custom-checkbox");
      const guessButton = document.getElementById("translateCheckbox");  
      // const message = document.getElementById("preguess-message");  
      // const location = document.getElementById("next-location-btn");

      checkbox.disabled = false;
      label.disabled = false;
      // guessButton.removeAttribute("hidden");
      guessButton.disabled = false; 
      // message.style.display = "none";  
      // location.setAttribute("hidden", true)
  });

  document.getElementById("myCheckbox").addEventListener("change", function() {
    const descriptionFlexbox = document.querySelector(".description-flexbox"); 
    const nextLocationButton = document.getElementById("next-location-btn"); 
    // const DistanceValue = document.getElementById("distance-value");   
    const Score = document.getElementById("score-flexbox")

  
    if (this.checked) { 
      guess(); // Call function to reveal location when checkbox is checked 
      disableMap(); // Disable the map 

      descriptionFlexbox.classList.add("translate"); 
      descriptionFlexbox.hidden = false;  

      nextLocationButton.removeAttribute("hidden");  
      nextLocationButton.classList.remove("hidden"); 
      nextLocationButton.hidden = false;

    } 
  });    
} 

function resetGame() {
  clear_markers(); // Clear current guess and revealed markers
  randomize_location(); // Get a new random location
  enableMap(); 


  // Reset UI elements
  const checkbox = document.getElementById("myCheckbox");
  const label = document.getElementById("custom-checkbox");
  const guessButton = document.getElementById("translateCheckbox");
  const message = document.getElementById("preguess-message");
  const distanceValue = document.getElementById("distance-value");
  const nextLocationBtn = document.getElementById("next-location-btn");
  const descriptionBox = document.querySelector(".description-flexbox");

  // Reset the checkbox and button states
  checkbox.checked = false;
  checkbox.disabled = true;
  label.disabled = true;
  guessButton.hidden = true;
  guessButton.disabled = true;
  nextLocationBtn.hidden = true;
  distanceValue.innerText = ""; // Clear the distance display

  // Re-show the description box and prepare for the next guess 
  descriptionBox.hidden = false;
  // descriptionBox.classList.remove("hidden"); 
  descriptionBox.classList.remove("translate");  

  // Reinitialize the Street View with the new location
  let panorama = new google.maps.StreetViewPanorama(
    document.getElementById("map"),
    {
      position: random_location,
      linksControl: false,
      panControl: true,
      enableCloseButton: false,
      fullscreenControl: false,
      addressControl: false,
      showRoadLabels: false,
      clickToGo: false,
      zoomControl: false,
      zoomControlOptions: {
        position: google.maps.ControlPosition.TOP_LEFT,
      },
    }
  );
  
  rndmarker.setMap(null); // Hide the previous random location marker
}


document.getElementById("myCheckbox").addEventListener("change", function() {
  const descriptionFlexbox = document.querySelector(".description-flexbox"); 
  const nextLocationButton = document.getElementById("next-location-btn");

  if (this.checked) { 
    guess(); // Call function to reveal location when checkbox is checked 
    disableMap(); // Disable the map 

    // Move the description flexbox down
    descriptionFlexbox.classList.add("translate"); // Add the translation class  
    descriptionFlexbox.classList.remove("hidden");

    nextLocationButton.removeAttribute("hidden");  // Remove the 'hidden' attribute
    nextLocationButton.classList.remove("hidden"); 
    nextLocationButton.hidden = false;

  }  
});

// Add event listener to the Next Location button
document.getElementById("next-location-btn").addEventListener("click", function () {
  resetGame(); // Call the reset game function
  this.classList.add("hidden"); // Hide the 'Next Location' button after reset

  const descriptionBox = document.querySelector(".description-flexbox");
  descriptionBox.classList.add("hidden"); 
});


// Function to calculate the distance between guess and actual location
function calculate_distance() {
  var randomLat = random_location.lat;
  var randomLng = random_location.lng;
  var guessLat = guess_location.lat();
  var guessLng = guess_location.lng();

  var dLat = 111.32 * Math.abs(randomLat - guessLat);
  var dLng = (40075 * Math.cos(randomLat * Math.PI / 180) / 360) * (randomLng - guessLng); 
  var distance = 1000 * (Math.sqrt(Math.pow(dLat, 2) + Math.pow(dLng, 2))); 

  if (distance > 3000) {
      return "WTF"; 
  } else {
      return distance;
  }
}

// Clear all markers on the map
function clear_markers() {
  markers.forEach(marker => {
      marker.setMap(null);
  });
  markers = [];
}

// Assuming rndmarker is your correct location marker
let isCorrectMarker = false; // This will track if the rndmarker is the correct one

function reveal_location() {
    rndmarker.setMap(map); // Show the random marker on the map
}



// Guess function to reveal location and calculate distance
function guess() {
  reveal_location(); 
  var result = calculate_distance(); 

  if (typeof result === "string") {
      document.getElementById("distance-value").innerText = result; 
  } else {
      document.getElementById("distance-value").innerText = Math.round(result); 
  } 

  const checkbox = document.getElementById("myCheckbox");
  const guessButton = document.getElementById("translateCheckbox");
  checkbox.disabled = true; 
  guessButton.disabled = true;  


  // Show the "Next Location" button after the guess
  const nextLocationBtn = document.getElementById("next-location-btn");
  nextLocationBtn.removeAttribute("hidden"); // Show the button
}



// Randomize the POI location and set the global variables
function randomize_location() {
  random_poi = poi_list[Math.floor(Math.random() * poi_list.length)];
  random_location = random_poi.coords;
  random_name = random_poi.name;
  random_desc = random_poi.desc;

  // Update the position of rndmarker
  rndmarker.position = random_location; // Update the position for the marker

  // Update the description and correct answer in HTML
  document.getElementById("poi-description").innerText = random_desc;
  document.getElementById("correct-answer").innerText = "Location: " + random_name;
} 

function disableMap() {
  map.setOptions({
      draggable: true, // Disable dragging
      disableDefaultUI: true, // Disable default UI elements (optional) 
      zoomControl: true, // Enable zoom control
      scrollwheel: true, // Allow zooming with scrollwheel
      gestureHandling: "auto" // Allow zooming with gestures (like pinch zoom on touch devices)
  });

  // Optionally, remove the click listener to prevent adding markers
  google.maps.event.clearListeners(map, 'click');
} 

function enableMap() {
  map.setOptions({
    draggable: true, // Enable dragging
    disableDefaultUI: false // Enable default UI elements (optional)
  }); 

  map.addListener("click", (mapsMouseEvent) => {
    marker.setMap(null);
    guess_location = mapsMouseEvent.latLng;
    marker = new AdvancedMarkerElement({
        map,
        position: mapsMouseEvent.latLng
    });   
    markers.push(marker); 
    
    const checkbox = document.getElementById("myCheckbox");
    const label = document.getElementById("custom-checkbox");
    const guessButton = document.getElementById("translateCheckbox");  
    const message = document.getElementById("preguess-message"); 

    checkbox.disabled = false;
    label.disabled = false;
    guessButton.removeAttribute("hidden");
    guessButton.disabled = false; 
    message.style.display = "none"; 
});
} // Close the enableMap function 

function initializeStartScreen() {
  const startScreen = document.getElementById("start-screen");
  const startButton = document.getElementById("start-button");

  startButton.addEventListener("click", () => {
    startScreen.style.display = "none"; // Hide the start screen
    initialize(); // Start the game by calling the initialize function
  });
}

// Call the initializeStartScreen function when the page loads
window.onload = initializeStartScreen;
initialize();