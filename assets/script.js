document.addEventListener("DOMContentLoaded", async function () {
    const map = L.map("map").setView([14.5, 3.5], 5);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
    }).addTo(map);

    L.control.fullscreen({
		position: 'topleft', // change the position of the button can be topleft, topright, bottomright or bottomleft, default topleft
		title: 'Show me the fullscreen !', // change the title of the button, default Full Screen
		titleCancel: 'Exit fullscreen mode', // change the title of the button when fullscreen is on, default Exit Full Screen
		content: null, // change the content of the button, can be HTML, default null
		forceSeparateButton: true, // force separate button to detach from zoom buttons, default false
		forcePseudoFullscreen: true, // force use of pseudo full screen even if full screen API is available, default false
		fullscreenElement: false // Dom element to render in full screen, false by default, fallback to map._container
	}).addTo(map);

    const geoJsonFile = "web_data/communes_all_pop_v2.geojson"; 
    const uemoaBordersFile = "web_data/uemoa_borders.geojson"; 
    const cemacBordersFile = "web_data/cemac_borders.geojson"; 
    const ghanaBordersFile = "web_data/ghana_borders.geojson";
    const nigeriaBordersFile = "web_data/nigeria_borders.geojson";

    // Create a loading spinner
    const loadingSpinner = document.createElement("div");
    loadingSpinner.className = "loading-spinner"; // Set class for styling
    loadingSpinner.innerHTML = `
        <div class="spinner"></div>
        <span>Loading...</span>
    `;
    document.body.appendChild(loadingSpinner);
    
    setTimeout(() => {
        if (document.body.contains(loadingSpinner)) {
            document.body.removeChild(loadingSpinner); // Remove spinner after delay
        }
    }, 3500);
    




            // const equipmentDropdown = document.getElementById("equipment-select");

            //equipmentDropdown.querySelectorAll(".dropdown-item").forEach(item => {
                //item.addEventListener("click", function () {
                    //selectedEquipment = this.getAttribute("data-value");
                    //document.getElementById("equipmentDropdown").textContent = this.textContent;
                    //loadMapData(geoJsonData, selectedCommune, selectedDepartment, selectedRegion, selectedCountry, selectedEquipment);
                //});
            //});

    // Fetch GeoJSON data
    // Fetch UEMOA and CEMAC borders
    const uemoaData = await fetch(uemoaBordersFile).then(response => response.json());
    const cemacData = await fetch(cemacBordersFile).then(response => response.json());
    const ghanaData = await fetch(ghanaBordersFile).then(response => response.json());
    const nigeriaData = await fetch(nigeriaBordersFile).then(response => response.json());
    fetch(geoJsonFile)
        .then(response => response.json())
        .then(geoJsonData => {
            let selectedEquipment = "ISIBF_base";
            let selectedCommune = "";
            let selectedDepartment = "";
            let selectedRegion = "";
            let selectedCountry = "";

            // Extract unique countries from the GeoJSON data
            const countries = [...new Set(geoJsonData.features.map(f => f.properties.ADM0_EN))];
            countries.sort((a, b) => a.localeCompare(b));

            const countryCenters = {
                "Benin": { lat: 9.3, lng: 2.5, zoom: 7 },
                "Burkina Faso": { lat: 12.4, lng: -1.5, zoom: 7 },
                "Ivory Coast": { lat: 7.5, lng: -5.5, zoom: 7 },
                "Guinea-Bissau": { lat: 11.5, lng: -15.7, zoom: 8 },
                "Mali": { lat: 12.6, lng: -8, zoom: 5 },
                "Niger": { lat: 17.6, lng: 8, zoom: 6 },
                "Senegal": { lat: 14.5, lng: -14, zoom: 7 },
                "Togo": { lat: 8.2, lng: 1.3, zoom: 7 },
                "Ghana": { lat: 7.5, lng: -0.5, zoom: 7 },
                "Cameroon": { lat: 6.5, lng: 13, zoom: 6 },
                "Chad": { lat: 15.5, lng: 18, zoom: 5 }, 
                "Nigeria": { lat: 9.1, lng: 8.5, zoom: 6 },
            };

            // Country Dropdown
            const countryDropdown = document.getElementById("country-select");
            document.getElementById("commune-select").innerHTML = "";
            document.getElementById("department-select").innerHTML = "";
            document.getElementById("region-select").innerHTML = "";

            countries.forEach(coun => {
                isDefaultView = false;
                // Filter GeoJSON data based on the selected commune, department, or region
                const filteredCountryData = geoJsonData.features.filter(feature => {
                    return (!coun || feature.properties.ADM0_EN === coun)
                }); 
                        const listItem = document.createElement("li");
                listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${coun}">${coun}</a>`;
                listItem.addEventListener("click", () => {
                    // Reset selected values
                    selectedCountry = coun;
                    selectedCommune = "";
                    selectedDepartment = "";
                    selectedRegion = "";

                    // Clear the dropdowns before populating them with new data
                    document.getElementById("region-select").innerHTML = "";
                    document.getElementById("department-select").innerHTML = "";
                    document.getElementById("commune-select").innerHTML = "";

                    
                    document.getElementById("countryDropdown").textContent = coun;
                    document.getElementById("regionDropdown").textContent = "";
                    document.getElementById("departmentDropdown").textContent = "";
                    document.getElementById("communeDropdown").textContent = "";



                    // Update the dropdowns based on selected country
                    populateRegionDropdown(filteredCountryData, coun);
                    

                    // Set map view to the selected country
                    if (countryCenters[coun]) {
                        const { lat, lng, zoom } = countryCenters[coun];
                        map.setView([lat, lng], zoom);
                    }


                    document.getElementById("num-municipalities").innerHTML = '';
                    document.getElementById("total-bran").innerHTML = '';
                    document.getElementById("percent-pop").innerHTML = '';
                    document.getElementById("percent-area").innerHTML = '';

                    // Load map data
                    loadMapData(geoJsonData, coun, "", "", "", selectedEquipment);
                    updateStats(filteredCountryData,filteredCountryData, coun);
                });

                countryDropdown.appendChild(listItem);
            });

            // Populate region dropdown based on the selected country
            function populateRegionDropdown(filteredCountryData, country) {
                const regions = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country).map(f => f.properties.ADM1_FR))];
                regions.sort((a, b) => a.localeCompare(b));
                const regionDropdown = document.getElementById("region-select");


                regions.forEach(reg => {
                    const filteredRegionData = geoJsonData.features.filter(feature => {
                        return (!country || feature.properties.ADM0_EN === country) && (!reg || feature.properties.ADM1_FR === reg)
                    }); 
                    const regionItem = document.createElement("li");
                    regionItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${reg}">${reg}</a>`;
                    regionItem.addEventListener("click", () => {
                        selectedRegion = reg;
                        populateDepartmentDropdown(filteredCountryData, country, reg);
                        document.getElementById("regionDropdown").textContent = reg;
                        document.getElementById("departmentDropdown").textContent = "";
                        document.getElementById("communeDropdown").textContent = "";
                        updateStats(filteredCountryData, filteredRegionData, country);
                        loadMapData(geoJsonData, country, reg, "", "", selectedEquipment);
                    });
                    regionDropdown.appendChild(regionItem);
                });
            }

            // Populate department dropdown based on the selected region and country
            function populateDepartmentDropdown(filteredCountryData, country, region) {
                const departments = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region).map(f => f.properties.ADM2_FR))];
                departments.sort((a, b) => a.localeCompare(b));
                const departmentDropdown = document.getElementById("department-select");

                departments.forEach(dep => {
                    //extract the corresponding region for the department
                        const filteredDepartmentData = geoJsonData.features.filter(feature => {
                        return (!country || feature.properties.ADM0_EN === country) && 
                        (!region || feature.properties.ADM1_FR === region) && 
                        (!dep || feature.properties.ADM2_FR === dep)
                    });
                    const departmentItem = document.createElement("li");
                    departmentItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${dep}">${dep}</a>`;
                    departmentItem.addEventListener("click", () => {
                        selectedDepartment = dep;
                        populateCommuneDropdown(filteredCountryData, country, region, dep);
                        document.getElementById("departmentDropdown").textContent = dep;
                        document.getElementById("regionDropdown").textContent = region;
                        document.getElementById("communeDropdown").textContent = "";
                        updateStats(filteredCountryData, filteredDepartmentData, country);
                        loadMapData(geoJsonData, country, region, dep, "", selectedEquipment);
                    });
                    departmentDropdown.appendChild(departmentItem);
                });
            }

            // Populate commune dropdown based on the selected department, region, and country
            function populateCommuneDropdown(filteredCountryData, country, region, department) {
                const communes = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region && f.properties.ADM2_FR === department).map(f => f.properties.ADM3_FR))];
                communes.sort((a, b) => a.localeCompare(b));
                const communeDropdown = document.getElementById("commune-select");

                communes.forEach(comm => {
                    const filteredCommuneData = geoJsonData.features.filter(feature => {
                        return (!country || feature.properties.ADM0_EN === country) &&
                        (!region || feature.properties.ADM1_FR === region) &&
                        (!department || feature.properties.ADM2_FR === department) &&
                        (!comm || feature.properties.ADM3_FR === comm)
                    });
                    const communeItem = document.createElement("li");
                    communeItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${comm}">${comm}</a>`;
                    communeItem.addEventListener("click", () => {
                        selectedCommune = comm;
                        document.getElementById("communeDropdown").textContent = comm;
                        document.getElementById("departmentDropdown").textContent = department;
                        document.getElementById("regionDropdown").textContent = region;
                        updateStats(filteredCountryData, filteredCommuneData, country);
                        loadMapData(geoJsonData, country, region, department, comm, selectedEquipment);
                    });
                    communeDropdown.appendChild(communeItem);
                });
            }

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
                map.setView([14.5, 3.5], 5);

                document.getElementById("num-municipalities").innerHTML = '';
                document.getElementById("total-bran").innerHTML = '';
                document.getElementById("percent-pop").innerHTML = '';
                document.getElementById("percent-area").innerHTML = '';
            });

            loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
            
            // Add UEMOA and CEMAC borders
            L.geoJSON(uemoaData, {
                style: function () {
                    return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for UEMOA
                }
            }).addTo(map)
            
            L.geoJSON(cemacData, {
                style: function () {
                    return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for CEMAC
                }
            }).addTo(map)
            
            L.geoJSON(ghanaData, {
                style: function () {
                    return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for Ghana
                }
            }).addTo(map)

            L.geoJSON(nigeriaData, {
                style: function () {
                    return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style for Nigeria
                }
            }).addTo(map)
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
    
        if (['Cameroon', 'Chad', 'Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'].includes(country)) {
            legend = L.control({ position: "bottomright" });
    
            const grades = [1, 0.5, 0.2, 0.1, 0.01];
    
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
        } 
        else if (['Cameroon', 'Chad'].includes(country)) {
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
        } else if (['Ghana', 'Nigeria'].includes(country)) {
            legend = L.control({ position: "bottomright" });
    
            const grades = [1, 0.5, 0.2, 0.1, 0.01];
    
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
        }
    } 



    function getColor(value, country) {
        // Color mapping based on country
        if (['Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'].includes(country)) {
            return value > 0.5 ? "#08519c" :  // Darkest
            value > 0.2 ? "#3182bd" :
            value > 0.1 ? "#6baed6" :
            value > 0.01 ? "#bdd7e7" :  // Lightest
            "#eff3ff";  // Lightest
     
        } else if (['Ghana', 'Nigeria'].includes(country)) {
            return value > 0.5 ? "#880e4f" :  // Darkest
            value > 0.2 ? "#c2185b" :
            value > 0.1 ? "#d81b60" :
            value > 0.01 ? "#f768a1" :  // Lightest
            "#ffeff3";  // Lightest
     
        } else if (['Cameroon', 'Chad'].includes(country)) {
            return value > 0.5 ? "#00441b" :  // Darkest
            value > 0.1 ? "#006d2c" :
            value > 0.01 ? "#31a354" :
            value > 0.001 ? "#a1d99b" :  // Lightest
            "#f3ffef";  // Lightest
     
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
        "Nigeria": "Local Government Areas"
    };

    // Function to update statistics dynamically based on filtered data
    function updateStats(filteredDataCountry, filteredData, country) {

        const popCountries = ['Nigeria', 'Cameroon', 'Ghana', 'Chad', 'Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'];
        if (popCountries.includes(country)) {
            const municipalityLabel = municipalities[country] || "Municipalities"; // Default fallback to "Municipalities"
    
            // Calculate the total number of communes, branches, population, and area
            const totalCommunes = filteredData.length;
            const totalBranches = filteredData.reduce((sum, feature) => sum + (feature.properties.Total_bran || 0), 0);

            const totalPopulation = filteredData.reduce((sum, feature) => sum + (Number(feature.properties.Population) || 0), 0);

            const totalArea = filteredData.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);
    
            // Calculate total population and area for the entire country
            const totalCountryPopulation = filteredDataCountry.reduce((sum, feature) => sum + (Number(feature.properties.Population) || 0), 0);
            const totalCountryArea = filteredDataCountry.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);
            const totalCountryBranches = filteredDataCountry.reduce((sum, feature) => sum + (feature.properties.Total_bran || 0), 0);
    
            // Calculate the percentage of population and area for the filtered region
            const populationPercentage = totalCountryPopulation > 0 ? ((totalPopulation / totalCountryPopulation) * 100).toFixed(1) : 0;
            const areaPercentage = totalCountryArea > 0 ? ((totalArea / totalCountryArea) * 100).toFixed(1) : 0;
            const branchPercentage = totalCountryBranches > 0 ? ((totalBranches / totalCountryBranches) * 100).toFixed(1) : 0;
    
            // Update the statistics in the HTML
            document.getElementById("num-municipalities").innerHTML = `<span>${totalCommunes}</span>${municipalityLabel}`;
            document.getElementById("total-bran").innerHTML = `<span>${branchPercentage}%</span>Bank Branches`;
            document.getElementById("percent-pop").innerHTML = `<span>${populationPercentage}%</span>Population`;
            document.getElementById("percent-area").innerHTML = `<span>${areaPercentage}%</span>Area`;
        
        } else {
            // If the country is not in the UEMOA group, don't update stats
            console.log(`No stats update for ${country}.`);
            // Clear the contents of the statistics divs
            document.getElementById("num-municipalities").innerHTML = '';
            document.getElementById("total-bran").innerHTML = '';
            document.getElementById("percent-pop").innerHTML = '';
            document.getElementById("percent-area").innerHTML = '';
            }
    }

});
