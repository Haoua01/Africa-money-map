document.addEventListener("DOMContentLoaded", async function () {
    const map = L.map("map").setView([14.5, 3.5], 5);

    const loadingSpinner = document.createElement("div");
    loadingSpinner.className = "loading-spinner"; // Set class for styling
    loadingSpinner.innerHTML = `
        <div class="spinner"></div>
        <span>Loading...</span>
    `;
    document.body.appendChild(loadingSpinner);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
    }).addTo(map);

    const geoJsonFile = "web_data/communes_all.geojson";
    const uemoaBordersFile = "web_data/uemoa_borders.geojson";
    const cemacBordersFile = "web_data/cemac_borders.geojson";


    let layersAdded = 0;  // Counter for added layers

    // Function to check if all layers are loaded
    function checkAllLayersAdded() {
        if (layersAdded >= 4) { // because base layer + 3 GeoJSON layers are added
            if (document.body.contains(loadingSpinner)) {
                document.body.removeChild(loadingSpinner); // Remove the spinner
            }
        }
    }

    // Track when each layer is added
    map.on('layeradd', function () {
        layersAdded++;
        checkAllLayersAdded();  // Check after every layer is added
    });

    // Fetch GeoJSON data
    try {
        const [geoJsonData, uemoaData, cemacData] = await Promise.all([
            fetch(geoJsonFile).then(response => response.json()),
            fetch(uemoaBordersFile).then(response => response.json()),
            fetch(cemacBordersFile).then(response => response.json())
        ]);

        let selectedEquipment = "ISIBF_base";
        let selectedCommune = "";
        let selectedDepartment = "";
        let selectedRegion = "";
        let selectedCountry = "";

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
                loadMapData(geoJsonData, "", "", "", comm, selectedEquipment);
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
                loadMapData(geoJsonData, "", reg, "", "", selectedEquipment);
            });
            regionDropdown.appendChild(listItem);
        });

        const countryCenters = {
            "Benin": { lat: 9.5, lng: 2.5, zoom: 7 },
            "Burkina Faso": { lat: 12.4, lng: -1.5, zoom: 7 },
            "Ivory Coast": { lat: 7.5, lng: -5.5, zoom: 7 },
            "Guinea-Bissau": { lat: 11.5, lng: -15.7, zoom: 8 },
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

        countries.forEach(coun => {
            const listItem = document.createElement("li");
            const legend = L.control({ position: "bottomright" });
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
            legend.onAdd = function () {
                const div = L.DomUtil.create("div", "legend"),
                grades = [1, 0.5, 0.1, 0.01, 0.001];

                div.innerHTML += "<strong>Bank Branch Score Access</strong><br>";
                for (let i = 0; i < grades.length; i++) {
                    div.innerHTML += `<i style="background:${getColor(grades[i] + 1)}"></i> ${
                        grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "+"}<br>`;
                }
                return div;
            };
        });
        countryDropdown.addEventListener("change", function () {
            const selectedCountry = this.value;
            loadMapData(geoJsonData, selectedCountry, "", "", "", selectedEquipment);  // Update the map and legend
        });

        // Reset button event
        document.getElementById("resetButton").addEventListener("click", function() {
            isDefaultView = true;
            loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
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

        // Add UEMOA and CEMAC borders
        L.geoJSON(uemoaData, {
            style: function () {
                return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for UEMOA
            }
        }).addTo(map);

        L.geoJSON(cemacData, {
            style: function () {
                return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for CEMAC
            }
        }).addTo(map);

    } catch (error) {
        console.error('Error loading GeoJSON:', error);
        // Remove spinner in case of error, if it exists
        if (document.body.contains(loadingSpinner)) {
            document.body.removeChild(loadingSpinner);
        }
    }

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

    function loadMapData(geoJsonData, country, region, department, commune, selectedEquipment) {
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
                const country = feature.properties.ADM0_EN;  // Corrected reference to country property
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

    let legend;  // Declare legend outside of the event listener

    function updateLegend(country) {
        if (legend) {
            legend.remove();  // Remove previous legend before adding a new one
        }

        if (country) {
            legend = L.control({ position: "bottomright" });

            const grades = [1, 0.5, 0.1, 0.01, 0.001];

            legend.onAdd = function () {
                const div = L.DomUtil.create("div", "legend");

                div.innerHTML += "<strong>Bank Branch Score Access</strong><br>";
                for (let i = 0; i < grades.length; i++) {
                    div.innerHTML += `<i style="background:${getColor(grades[i], country)}"></i> ${
                        grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "-0"}<br>`;
                }

                return div;
            };

            legend.addTo(map);  // Add the new legend

            layersAdded++; // Increment layer counter for GeoJSON layer

            checkAllLayersAdded(); // Check if all layers are added
        }
    }

    function getColor(value, country) {
        // Color mapping based on country
        if (['Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'].includes(country)) {
            return value > 0.5 ? "#08519c" :  // Darkest
            value > 0.1 ? "#3182bd" :
            value > 0.01 ? "#6baed6" :
            value > 0.001 ? "#bdd7e7" :  // Lightest
            "#eff3ff";  // Lightest

        } else if (country === 'Ghana') {
            return value > 0.5 ? "#880e4f" :  // Darkest
            value > 0.1 ? "#c2185b" :
            value > 0.01 ? "#d81b60" :
            value > 0.001 ? "#f768a1" :  // Lightest
            "#fbb4b9";  // Lightest

        } else if (['Cameroon', 'Chad'].includes(country)) {
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

    // Define the countries and their respective labels for municipalities
    const municipalities = {
        "Benin": "Communes",
        "Burkina Faso": "Communes",
        "Mali": "Communes",
        "Niger": "Communes",
        "Ivory Coast": "Sub-Prefectures",
        "Guinea-Bissau": "Sectors",
        "Senegal": "Arrondissements",
        "Togo": "Communes",
        "Ghana": "Districts",
        "Cameroon": "Arrondissements",
        "Chad": "Provinces",
    };

    // Function to update statistics dynamically based on filtered data
    function updateStats(filteredData, country) {
        const uemoaCountries = ['Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'];
        if (uemoaCountries.includes(country)) {
            const municipalityLabel = municipalities[country] || "Municipalities"; // Default fallback to "Municipalities"
    
            // Calculate the total number of communes, branches, population, and area
            const totalCommunes = filteredData.length;
            const totalBranches = filteredData.reduce((sum, feature) => sum + (feature.properties.Total_bran || 0), 0);
            const totalPopulation = filteredData.reduce((sum, feature) => sum + (feature.properties.Population || 0), 0);
            const totalArea = filteredData.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);
    
            // Calculate total population and area for the entire country
            const totalCountryPopulation = filteredData.reduce((sum, feature) => sum + (feature.properties.Population || 0), 0);
            const totalCountryArea = filteredData.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);
    
            // Calculate the percentage of population and area for the filtered region
            const populationPercentage = totalCountryPopulation > 0 ? ((totalPopulation / totalCountryPopulation) * 100).toFixed(2) : 0;
            const areaPercentage = totalCountryArea > 0 ? ((totalArea / totalCountryArea) * 100).toFixed(2) : 0;
    
            // Update the statistics in the HTML
            document.getElementById("num-municipalities").innerHTML = `<span style="font-size: 30px;">${totalCommunes}</span>${municipalityLabel}`;
            document.getElementById("total-bran").innerHTML = `<span style="font-size: 30px;">${totalBranches}</span>Branches`;
            document.getElementById("percent-pop").innerHTML = `<span style="font-size: 30px;">${populationPercentage}%</span>of ${country}'s population`;
            document.getElementById("percent-area").innerHTML = `<span style="font-size: 30px;">${areaPercentage}%</span>of ${country}'s area`;
        
        } else {
            // If the country is not in the UEMOA group, don't update stats
            console.log(`No stats update for ${country}.`);
        }
    }


});
