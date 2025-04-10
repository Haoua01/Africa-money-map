document.addEventListener("DOMContentLoaded", async function () {
    const map = L.map("map").setView([14.5, 3.5], 5);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
    }).addTo(map);

    const geoJsonFile = "web_data/communes_all.geojson"; 
    const uemoaBordersFile = "web_data/uemoa_borders.geojson"; 
    const cemacBordersFile = "web_data/cemac_borders.geojson"; 

    const loadingSpinner = document.createElement("div");
    loadingSpinner.className = "loading-spinner"; // Set class for styling
    loadingSpinner.innerHTML = `
        <div class="spinner"></div>
        <span>Loading...</span>
    `;
    document.body.appendChild(loadingSpinner); // Append the spinner to the body or map container



    // Fetch GeoJSON data
    fetch(geoJsonFile)
        .then(response => response.json())
        .then(geoJsonData => {
            let selectedEquipment = "ISIBF_base";
            let selectedCommune = "";
            let selectedDepartment = "";
            let selectedRegion = "";
            let selectedCountry = "";

            // const equipmentDropdown = document.getElementById("equipment-select");

            //equipmentDropdown.querySelectorAll(".dropdown-item").forEach(item => {
                //item.addEventListener("click", function () {
                    //selectedEquipment = this.getAttribute("data-value");
                    //document.getElementById("equipmentDropdown").textContent = this.textContent;
                    //loadMapData(geoJsonData, selectedCommune, selectedDepartment, selectedRegion, selectedCountry, selectedEquipment);
                //});
            //});

            // Extract unique communes, departments, and regions from the GeoJSON data
            const communes = [...new Set(geoJsonData.features.map(f => f.properties.ADM3_FR))];
            const departments = [...new Set(geoJsonData.features.map(f => f.properties.ADM2_FR))];
            const regions = [...new Set(geoJsonData.features.map(f => f.properties.ADM1_FR))];
            const countries = [...new Set(geoJsonData.features.map(f => f.properties.ADM0_EN))];

            // Populate commune dropdown
            const communeDropdown = document.getElementById("commune-select");
            communes.forEach(comm => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${comm}">${comm}</a>`;
                listItem.addEventListener("click", () => {
                    selectedCommune = comm;
                    document.getElementById("communeDropdown").textContent = comm;
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("regionDropdown").textContent = "Default";
                    document.getElementById("countryDropdown").textContent = "Default";
                    selectedDepartment = "";
                    selectedRegion = "";
                    selectedCountry = "";
                    loadMapData(geoJsonData, "", comm, "", "", selectedEquipment);
                });
                communeDropdown.appendChild(listItem);
            });

            // Populate department dropdown
            const departmentDropdown = document.getElementById("department-select");
            departments.forEach(dep => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${dep}">${dep}</a>`;
                listItem.addEventListener("click", () => {
                    selectedCommune = "";
                    selectedDepartment = dep;
                    document.getElementById("communeDropdown").textContent = "Default";
                    document.getElementById("departmentDropdown").textContent = dep;
                    document.getElementById("regionDropdown").textContent = "Default";
                    document.getElementById("countryDropdown").textContent = "Default";
                    selectedRegion = "";
                    selectedCountry = "";
                    loadMapData(geoJsonData, "", "", dep, "", selectedEquipment);
                });
                departmentDropdown.appendChild(listItem);
            });

            // Populate region dropdown
            const regionDropdown = document.getElementById("region-select");
            regions.forEach(reg => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${reg}">${reg}</a>`;
                listItem.addEventListener("click", () => {
                    selectedRegion = reg;
                    document.getElementById("communeDropdown").textContent = "Default";
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("regionDropdown").textContent = reg;
                    document.getElementById("countryDropdown").textContent = "Default";
                    selectedCommune = "";
                    selectedDepartment = "";
                    selectedCountry = "";
                    loadMapData(geoJsonData,"", "", "", reg, selectedEquipment);
                });
                regionDropdown.appendChild(listItem);
            });

            const countryCenters = {
                "Benin": { lat: 9.5, lng: 2.5, zoom: 7 },
                "Burkina Faso": { lat: 12.4, lng: -1.5, zoom: 7 },
                "Ivory Coast": { lat: 7.5, lng: -5.5, zoom: 7 },
                "Guinea-Bissau": { lat: 9.5, lng: -13.7, zoom: 8 },
                "Mali": { lat: 12.6, lng: -8, zoom: 6 },
                "Niger": { lat: 17.6, lng: 8, zoom: 6 },
                "Senegal": { lat: 14.5, lng: -14, zoom: 7 },
                "Togo": { lat: 8.2, lng: 1.3, zoom: 7 },
                "Ghana": { lat: 7.5, lng: -0.5, zoom: 7 },
                "Cameroon": { lat: 6.5, lng: 13, zoom: 6 },
                "Chad": { lat: 15.5, lng: 18, zoom: 6 }
            };


        
            // Country Dropdown
            const countryDropdown = document.getElementById("country-select");
            countryDropdown.addEventListener("change", function () {
                const selectedCountry = this.value;
                loadMapData(geoJsonData, selectedCountry, "", "", "", selectedEquipment);  // Update the map and legend
            });
            countries.forEach(coun => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${coun}">${coun}</a>`;
                listItem.addEventListener("click", () => {
                    isDefaultView = false;  // Change the flag to false when a country is selected
                    selectedCountry = coun;
                    document.getElementById("communeDropdown").textContent = "Default";
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("regionDropdown").textContent = "Default";
                    document.getElementById("countryDropdown").textContent = coun;
                    selectedCommune = "";
                    selectedDepartment = "";
                    selectedRegion = "";

                    // Set map view to the selected country
                    if (countryCenters[coun]) {
                        const { lat, lng, zoom } = countryCenters[coun];
                        map.setView([lat, lng], zoom);
                    }

                    loadMapData(geoJsonData, coun, "", "", "", selectedEquipment);
                });
                countryDropdown.appendChild(listItem);
            });
            
            // Reset button event
            document.getElementById("resetButton").addEventListener("click", function() {
                isDefaultView = true; 
                loadMapData(geoJsonData, "", "", "", selectedEquipment);
                document.getElementById("countryDropdown").textContent = "Default";
                document.getElementById("communeDropdown").textContent = "Default";
                document.getElementById("departmentDropdown").textContent = "Default";
                document.getElementById("regionDropdown").textContent = "Default";
                selectedCountry = "";
                selectedCommune = "";
                selectedDepartment = "";
                selectedRegion = "";
            });

            // Initial load
            loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
            // document.body.removeChild(loadingSpinner);
        })
        .catch(error => {
            console.error('Error loading GeoJSON:', error);
            // Remove spinner in case of error, if it exists
            if (document.body.contains(loadingSpinner)) {
                document.body.removeChild(loadingSpinner);
            }
        });

    // Info Control
    const info = L.control();
    info.onAdd = function () {
        this.div = L.DomUtil.create("div", "info");
        this.update();
        return this.div;
    };

    // Updated hover info: show commune name and score from "ISIBF_base"
    info.update = function (props) {
        this.div.innerHTML = props
            ? `<h6>${props.ADM3_FR}</h6><br>Score: ${props.ISIBF_base}`
            : "Hover over";
    };
    info.addTo(map);

    let isDefaultView = true; 
    
    function loadMapData(geoJsonData, country, commune, department, region, selectedEquipment) {
        map.eachLayer(layer => {
            if (layer instanceof L.GeoJSON) {
                map.removeLayer(layer);
            }
        });
    
        // Filter GeoJSON data based on the selected commune, department, or region
        const filteredData = geoJsonData.features.filter(feature => {
            return (!country || feature.properties.ADM0_EN === country) && 
                   (!commune || feature.properties.ADM3_FR === commune) &&
                   (!department || feature.properties.ADM2_FR === department) &&
                   (!region || feature.properties.ADM1_FR === region);
        });
    
        const geoJsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
            onEachFeature: function (feature, layer) {
                layer.on({
                    mouseover: function (e) {
                        e.target.setStyle({ weight: 3, color: "white", fillOpacity: 1 });
                        info.update(feature.properties);
                    },
                    mouseout: function (e) {
                        geoJsonLayer.resetStyle(e.target);
                        info.update();
                    }
                });
            },
            style: function (feature) {
                const score = feature.properties[selectedEquipment] || 0;
                const country = feature.properties.Country;  // Corrected reference to country property
                const fillColor = getColor(score, country);
    
                return {
                    fillColor: fillColor, 
                    weight: 0.3,  // Default border weight
                    opacity: 0.3, // Border opacity
                    color: (feature.properties.ADM0_EN !== undefined) ? "#333333" : "transparent", // Darker border for country boundaries
                    fillOpacity: 0.9  // Make sure the polygons are opaque enough
                };
            }
        }).addTo(map);

        updateLegend(country);

        if (isDefaultView) {
            // Load UEMOA borders
            fetch(uemoaBordersFile)
                .then(response => response.json())
                .then(data => {
                    L.geoJSON(data, {
                        style: function () {
                            return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for UEMOA
                        }
                    }).addTo(map);
                })
                .catch(error => console.error('Error loading UEMOA borders:', error));
    
            // Load CEMAC borders
            fetch(cemacBordersFile)
                .then(response => response.json())
                .then(data => {
                    L.geoJSON(data, {
                        style: function () {
                            return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for CEMAC
                        }
                    }).addTo(map);
                })
                .catch(error => console.error('Error loading CEMAC borders:', error));
        }


    }
    
    const legend = L.control({ position: "bottomright" });
    function updateLegend(country) {
        // Remove the old legend if it exists
        if (legend) {
            legend.remove();
        }
    
        if (country) {
            // Add the new legend when a country is selected
            legend = L.control({ position: "bottomright" });
            legend.onAdd = function () {
                const div = L.DomUtil.create("div", "legend"),
                    grades = [1, 0.5, 0.1, 0.01, 0.001];  // Adjust grades as per your needs
    
                div.innerHTML += "<strong>Bank Branch Access Score</strong><br>";
                for (let i = 0; i < grades.length; i++) {
                    div.innerHTML += `<i style="background:${getColor(grades[i] + 1)}"></i> ${
                        grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "-0"}<br>`;
                }
                return div;
            };
            legend.addTo(map);
        }
    }


    function getColor(value, country) {
        // Color mapping based on country
        if (['benin', 'burkina', 'civ', 'guinee', 'mali', 'niger', 'senegal', 'togo'].includes(country)) {
            return value > 0.5 ? "#08519c" :  // Darkest
            value > 0.1 ? "#3182bd" :
            value > 0.01 ? "#6baed6" :
            value > 0.001 ? "#bdd7e7" :  // Lightest
            "#eff3ff";  // Lightest
     
        } else if (country === 'ghana') {
            return value > 0.5 ? "#880e4f" :  // Darkest
            value > 0.1 ? "#c2185b" :
            value > 0.01 ? "#d81b60" :
            value > 0.001 ? "#f768a1" :  // Lightest
            "#fbb4b9";  // Lightest
     
        } else if (['cameroun', 'tchad'].includes(country)) {
            return value > 0.5 ? "#00441b" :  // Darkest
            value > 0.1 ? "#006d2c" :
            value > 0.01 ? "#31a354" :
            value > 0.001 ? "#a1d99b" :  // Lightest
            "#e5f5e0";  // Lightest
     
        } else {
            return "#ffffff"; // Default color if no country matches
        }
    }

    document.getElementById("map-btn").addEventListener("click", function() {
        showContent("map-content");
    });

    function showContent(contentId) {
        document.getElementById("map-content").style.display = "none";
        document.getElementById(contentId).style.display = "flex";
    }



});
