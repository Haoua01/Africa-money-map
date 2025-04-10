document.addEventListener("DOMContentLoaded", async function () {
    const map = L.map("map").setView([14.5, 3.5], 5);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
    }).addTo(map);

    const geoJsonFile = "web_data/communes_all.geojson"; 
    const uemoaBordersFile = "web_data/uemoa_borders.geojson"; 
    const cemacBordersFile = "web_data/cemac_borders.geojson"; 


    // Fetch GeoJSON data
    fetch(geoJsonFile)
        .then(response => response.json())
        .then(geoJsonData => {
            let selectedEquipment = "isibf_base";
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
            const communes = [...new Set(geoJsonData.features.map(f => f.properties.adm3_fr))];
            const departments = [...new Set(geoJsonData.features.map(f => f.properties.adm2_fr))];
            const regions = [...new Set(geoJsonData.features.map(f => f.properties.adm1_fr))];
            const countries = [...new Set(geoJsonData.features.map(f => f.properties.adm0_fr))];

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
                "benin": { lat: 9.5, lng: 2.5, zoom: 6 },
                "burkina": { lat: 12.4, lng: -1.5, zoom: 6 },
                "civ": { lat: 7.5, lng: -5.5, zoom: 6 },
                "guinee": { lat: 9.5, lng: -13.7, zoom: 6 },
                "mali": { lat: 12.6, lng: -8, zoom: 6 },
                "niger": { lat: 17.6, lng: 8, zoom: 6 },
                "senegal": { lat: 14.5, lng: -14, zoom: 6 },
                "togo": { lat: 8.2, lng: 1.3, zoom: 6 },
                "ghana": { lat: 7.5, lng: -0.5, zoom: 6 },
                "cameroun": { lat: 4.5, lng: 13, zoom: 6 },
                "tchad": { lat: 15.3, lng: 18, zoom: 6 }
            };
            

           // Country selection event
            const countryDropdown = document.getElementById("country-select");
            countries.forEach(coun => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${coun}">${coun}</a>`;
                listItem.addEventListener("click", () => {
                    selectedCountry = coun;
                    document.getElementById("communeDropdown").textContent = "Default";
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("regionDropdown").textContent = "Default";
                    document.getElementById("countryDropdown").textContent = coun;
                    selectedCommune = "";
                    selectedDepartment = "";
                    selectedRegion = "";

                    // Set map view to the selected country
                    if (countryCenters[coun.toLowerCase()]) {
                        const { lat, lng, zoom } = countryCenters[coun.toLowerCase()];
                        map.setView([lat, lng], zoom);
                    }

                    loadMapData(geoJsonData, coun, "", "", "", selectedEquipment);
                });
                countryDropdown.appendChild(listItem);
            });
            
            // Reset button event
            document.getElementById("resetButton").addEventListener("click", function() {
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
        })
        .catch(error => console.error('Error loading GeoJSON:', error));

    // Info Control
    const info = L.control();
    info.onAdd = function () {
        this.div = L.DomUtil.create("div", "info");
        this.update();
        return this.div;
    };

    // Updated hover info: show commune name and score from "isibf_base"
    info.update = function (props) {
        this.div.innerHTML = props
            ? `<h6>${props.adm3_fr}</h6><br>Score: ${props.isibf_base}`
            : "Hover over";
    };
    info.addTo(map);

    function loadMapData(geoJsonData, country, commune, department, region, selectedEquipment) {
        map.eachLayer(layer => {
            if (layer instanceof L.GeoJSON) {
                map.removeLayer(layer);
            }
        });
    
        // Filter GeoJSON data based on the selected commune, department, or region
        const filteredData = geoJsonData.features.filter(feature => {
            return (!country || feature.properties.adm0_fr === country) && 
                   (!commune || feature.properties.adm3_fr === commune) &&
                   (!department || feature.properties.adm2_fr === department) &&
                   (!region || feature.properties.adm1_fr === region);
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
                const country = feature.properties.country;  // Corrected reference to country property
                const fillColor = getColor(score, country);
    
                return {
                    fillColor: fillColor, 
                    weight: 0.3,  // Default border weight
                    opacity: 0.3, // Border opacity
                    color: (feature.properties.adm0_fr !== undefined) ? "#333333" : "transparent", // Darker border for country boundaries
                    fillOpacity: 0.9  // Make sure the polygons are opaque enough
                };
            }
        }).addTo(map);
    
        // Load UEMOA borders (and ensure they're on top of the polygons)
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
    
        // Load CEMAC borders (and ensure they're on top of the polygons)
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
