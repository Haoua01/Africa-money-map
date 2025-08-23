document.addEventListener("DOMContentLoaded", async function () {
    let defaultZoom = 5;
    let smallScreenZoom = 4; 
    let currentZoom = window.innerWidth <= 480 ? smallScreenZoom : defaultZoom;
    const map = L.map("map").setView([14.5, -1], currentZoom);

    let legend;  // Declare legend outside of the event listener

    // Global variables to store both datasets 
    let geoJsonData = null; 
    let isochroneData = null; 
    let currentGeoJsonLayer = null; 
    let currentIsochroneLayer = null;
    let currentBorderLayer = null;
    const toggleSwitch = document.getElementById('isochrone-toggle');


    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB &copy; Openrouteservice",
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

    const geoJsonFile = "data/Indicators/Hybrid/scores_corrected.geojson"; 
    const isochroneFile = "data/Indicators/Fully_isochrone/isochrone_map.geojson";
    const uemoaBordersFile = "web_data/uemoa_borders.geojson"; 

    const beninBordersFile = "data/UEMOA/adm_shapefiles/borders/benin_borders.geojson";
    const burkinaBordersFile = "data/UEMOA/adm_shapefiles/borders/burkina_borders.geojson";
    const civBordersFile = "data/UEMOA/adm_shapefiles/borders/civ_borders.geojson";
    const guineeBordersFile = "data/UEMOA/adm_shapefiles/borders/guinee_borders.geojson";
    const maliBordersFile = "data/UEMOA/adm_shapefiles/borders/mali_borders.geojson";
    const nigerBordersFile = "data/UEMOA/adm_shapefiles/borders/niger_borders.geojson";
    const senegalBordersFile = "data/UEMOA/adm_shapefiles/borders/senegal_borders.geojson";
    const togoBordersFile = "data/UEMOA/adm_shapefiles/borders/togo_borders.geojson";


    const countryBorders = {
        "Benin": beninBordersFile,
        "Burkina Faso": burkinaBordersFile,
        "Ivory Coast": civBordersFile,
        "Guinea-Bissau": guineeBordersFile,
        "Mali": maliBordersFile,
        "Niger": nigerBordersFile,
        "Senegal": senegalBordersFile,
        "Togo": togoBordersFile
    };
    //const cemacBordersFile = "web_data/cemac_borders.geojson"; 
    //const ghanaBordersFile = "web_data/ghana_borders.geojson";
    //const nigeriaBordersFile = "web_data/nigeria_borders.geojson";

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


    // const cemacData = await fetch(cemacBordersFile).then(response => response.json());
    // const ghanaData = await fetch(ghanaBordersFile).then(response => response.json());
    // const nigeriaData = await fetch(nigeriaBordersFile).then(response => response.json());
    try {
        // Load all data simultaneously
        const [geoJsonResponse, isochroneResponse, uemoaResponse] = await Promise.all([
            fetch(geoJsonFile),
            fetch(isochroneFile),
            fetch(uemoaBordersFile)
        ]);

        // Parse all JSON data
        geoJsonData = await geoJsonResponse.json();
        isochroneData = await isochroneResponse.json();
        const uemoaData = await uemoaResponse.json();

        console.log('Both datasets loaded successfully');
        console.log('GeoJSON features:', geoJsonData.features.length);
        console.log('Isochrone features:', isochroneData.features.length);

        // Set up toggle switch handler
        toggleSwitch.addEventListener('change', () => {
            if (toggleSwitch.checked) {
                // Show isochrone layer
                if (currentIsochroneLayer) {
                    map.addLayer(currentIsochroneLayer);
                }
            } else {
                // Hide isochrone layer
                if (currentIsochroneLayer) {
                    map.removeLayer(currentIsochroneLayer);
                }
            }
        });

            let selectedEquipment = "ISIBF_base";
            let selectedCommune = "";
            let selectedDepartment = "";
            let selectedRegion = "";
            let selectedCountry = "";

            // Function to update map based on current selections and toggle state
            function updateMapDisplay() {
                if (!selectedCountry) {
                    // Handle default mode (no country selected - show all countries)
                    if (toggleSwitch.checked) {
                        // Show isochrone layer for all countries
                        console.log('Loading isochrone data for all countries');
                        loadIsochrone(geoJsonData, isochroneData, "", "", "", "", selectedEquipment);
                        document.querySelector('#map-content h1').textContent = `Area Covered By At Least One Bank Branch`;

                    } else {
                        // Show regular map data for all countries
                        console.log('Loading map data for all countries');
                        loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
                        document.querySelector('#map-content h1').textContent = `Spatial Accessibility to Bank Branches`;

                    }
                    
                    // Add UEMOA borders for default mode
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
                    
                    return;
                }
                
                const countryData = geoJsonData.features.filter(feature => {
                    return feature.properties.ADM0_EN === selectedCountry;
                });

                const isochroneCountryData = isochroneData.features.filter(feature => {
                    return feature.properties.ADM0_EN === selectedCountry;
                });

                // Filter data based on current selections (region, department, commune)
                let filteredData = countryData.filter(feature => {
                    return (!selectedRegion || feature.properties.ADM1_FR === selectedRegion) &&
                        (!selectedDepartment || feature.properties.ADM2_FR === selectedDepartment) &&
                        (!selectedCommune || feature.properties.ADM3_FR === selectedCommune);
                });
                let isochroneFilteredData = isochroneCountryData.filter(feature => {
                    return (!selectedRegion || feature.properties.ADM1_FR === selectedRegion) &&
                        (!selectedDepartment || feature.properties.ADM2_FR === selectedDepartment) &&
                        (!selectedCommune || feature.properties.ADM3_FR === selectedCommune);
                });

                toggleCommuneDropdown(selectedCountry);


                // Handle country-specific mode (existing logic)
                if (toggleSwitch.checked) {
                    console.log('Loading isochrone data');
                    // Update title based on current selections
                    let titleText = `Area Covered By At Least One Bank Branch`;
                    let locationText = "";

                    if (selectedCommune) {
                        locationText = `${selectedCommune} - ${selectedDepartment}, ${selectedRegion}, ${selectedCountry}`;
                    } else if (selectedDepartment) {
                        locationText = `${selectedDepartment} - ${selectedRegion}, ${selectedCountry}`;
                    } else if (selectedRegion) {
                        locationText = `${selectedRegion} - ${selectedCountry}`;
                    } else {
                        locationText = `${selectedCountry}`;
                    }

                    document.querySelector('#map-content h1').innerHTML = `
                        <span class="title-main">${titleText}</span><br>
                        ${locationText}
                    `;


                    document.getElementById("num-municipalities").innerHTML = '';
                    document.getElementById("total-bran").innerHTML = '';
                    document.getElementById("percent-pop").innerHTML = '';
                    document.getElementById("percent-area").innerHTML = '';
                    loadIsochrone(geoJsonData, isochroneData, selectedCountry, selectedRegion, selectedDepartment, selectedCommune, selectedEquipment);
                    updatePercentage(isochroneFilteredData, selectedCountry, filteredData);
                } else {
                    // Show regular map data
                    console.log('Loading map data');
                    
                    let titleText = `Spatial Accessibility to Bank Branches`;
                    let locationText = "";

                    if (selectedCommune) {
                        locationText = `${selectedCommune} - ${selectedDepartment}, ${selectedRegion}, ${selectedCountry}`;
                    } else if (selectedDepartment) {
                        locationText = `${selectedDepartment} - ${selectedRegion}, ${selectedCountry}`;
                    } else if (selectedRegion) {
                        locationText = `${selectedRegion} - ${selectedCountry}`;
                    } else {
                        locationText = `${selectedCountry}`;
                    }

                    document.querySelector('#map-content h1').innerHTML = `
                        <span class="title-main">${titleText}</span><br>
                        ${locationText}
                    `;
                    
                    document.getElementById("num-municipalities").innerHTML = '';
                    document.getElementById("total-bran").innerHTML = '';
                    document.getElementById("percent-pop").innerHTML = '';
                    document.getElementById("percent-area").innerHTML = '';
                    loadMapData(geoJsonData, selectedCountry, selectedRegion, selectedDepartment, selectedCommune, selectedEquipment);
                    updateStats(countryData, filteredData, selectedCountry);
                }
            }



                // Set up toggle switch handler ONCE - outside of any other event handlers
            toggleSwitch.addEventListener('change', () => {
                if (toggleSwitch.checked) {
                    // Show isochrone layer
                    if (currentIsochroneLayer) {
                        map.addLayer(currentIsochroneLayer);
                    }
                } else {
                    // Hide isochrone layer
                    if (currentIsochroneLayer) {
                        map.removeLayer(currentIsochroneLayer);
                    }
                }
                // Update the map display based on current toggle state
                updateMapDisplay();
                
            });


            // Extract unique countries from the GeoJSON data
            const countries = [...new Set(geoJsonData.features.map(f => f.properties.ADM0_EN))];
            countries.sort((a, b) => a.localeCompare(b));

            const countryCenters = {
                "Benin": { lat: 9.3, lng: 2.5, latSmall: 9.3, lngSmall: 2.5, zoom: 7, smallScreenZoom: 6 },
                "Burkina Faso": { lat: 12.4, lng: -1.5, latSmall: 12.4, lngSmall: -1.5, zoom: 7, smallScreenZoom: 5 },
                "Ivory Coast": { lat: 7.5, lng: -5.5, latSmall: 7.5, lngSmall: -5.5, zoom: 7, smallScreenZoom: 6 },
                "Guinea-Bissau": { lat: 11.5, lng: -15.7, latSmall: 11.5, lngSmall: -15.2, zoom: 8, smallScreenZoom: 7 },
                "Mali": {lat: 12.6, lng: -8, latSmall: 14.6, lngSmall: -6, zoom: 5, smallScreenZoom: 4 },
                "Niger": { lat: 17.6, lng: 8, latSmall: 13.6, lngSmall: 8, zoom: 6, smallScreenZoom: 4 },
                "Senegal": { lat: 14.5, lng: -14, latSmall: 14.5, lngSmall: -14.5, zoom: 7, smallScreenZoom: 6 },
                "Togo": { lat: 8.2, lng: 1.3, latSmall: 8.2, lngSmall: 0.9, zoom: 7, smallScreenZoom: 6 },
                //"Ghana": { latSmall: 7.5, lngSmall: -0.5, zoom: 7 },
                //"Cameroon": { latSmall: 6.5, lngSmall: 13, zoom: 6 },
                //"Chad": { latSmall: 15.5, lngSmall: 18, zoom: 5 },
                //"Nigeria": { latSmall: 9.1, lngSmall: 8.5, zoom: 6 },
            };



            // Country Dropdown
            const countryDropdown = document.getElementById("country-select");
            document.getElementById("commune-select").innerHTML = "";
            document.getElementById("department-select").innerHTML = "";
            document.getElementById("region-select").innerHTML = "";

            countries.forEach(coun => {
                updateBorders(coun);
                // Filter GeoJSON data based on the selected commune, department, or region
                const filteredCountryData = geoJsonData.features.filter(feature => {
                    return (!coun || feature.properties.ADM0_EN === coun)
                }); 
                const filteredIsochroneData = isochroneData.features.filter(feature => {
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
                    

                    
                    if (countryCenters[coun]) {
                        const { lat, lng, latSmall, lngSmall, zoom, smallScreenZoom } = countryCenters[coun];
                        if (window.innerWidth <= 480) {
                            map.setView([latSmall, lngSmall], smallScreenZoom);
                        } else {
                            map.setView([lat, lng], zoom);
                        }

                    }
                    


                    document.getElementById("num-municipalities").innerHTML = '';
                    document.getElementById("total-bran").innerHTML = '';
                    document.getElementById("percent-pop").innerHTML = '';
                    document.getElementById("percent-area").innerHTML = '';

                    updateMapDisplay();
                    //updateStats(filteredCountryData, filteredCountryData, coun);
                    //updatePercentage(filteredIsochroneData, coun, filteredCountryData);

                });

                countryDropdown.appendChild(listItem);
            });

            // Function to zoom to the bounds of filtered areas
            function zoomToFilteredArea(geoJsonData, country, region, department, commune) {
                // Filter features based on current selection
                const filteredFeatures = geoJsonData.features.filter(feature => {
                    return (!country || feature.properties.ADM0_EN === country) && 
                           (!region || feature.properties.ADM1_FR === region) &&
                           (!department || feature.properties.ADM2_FR === department) &&
                           (!commune || feature.properties.ADM3_FR === commune);
                });

                if (filteredFeatures.length === 0) {
                    console.warn('No features found for the selected filters');
                    return;
                }

                // Create a temporary GeoJSON layer to calculate bounds
                const tempLayer = L.geoJSON({
                    type: "FeatureCollection",
                    features: filteredFeatures
                });

                // Get the bounds and fit the map to them
                const bounds = tempLayer.getBounds();
                
                if (bounds.isValid()) {
                    // Add some padding to the bounds for better visual appearance
                    const paddingOptions = {
                        padding: [20, 20], // 20 pixels padding on all sides
                        maxZoom: commune ? 12 : department ? 10 : region ? 8 : 7 // Different max zoom levels based on selection
                    };
                    
                    map.fitBounds(bounds, paddingOptions);
                } else {
                    console.warn('Invalid bounds calculated for filtered features');
                }
            }


            // Populate region dropdown based on the selected country
            function populateRegionDropdown(filteredCountryData, country) {
                const regions = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country).map(f => f.properties.ADM1_FR))];
                regions.sort((a, b) => a.localeCompare(b));
                const regionDropdown = document.getElementById("region-select");

                // Add "Default" option first
                const defaultRegionItem = document.createElement("li");
                defaultRegionItem.innerHTML = `<a class="dropdown-item" href="#" data-value="">Default</a>`;
                defaultRegionItem.addEventListener("click", () => {
                    selectedRegion = "";
                    selectedDepartment = "";
                    selectedCommune = "";
                    
                    // Clear dependent dropdowns
                    document.getElementById("department-select").innerHTML = "";
                    document.getElementById("commune-select").innerHTML = "";
                    
                    // Update dropdown texts
                    document.getElementById("regionDropdown").textContent = "Default";
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("communeDropdown").textContent = "Default";
                    
                    // Zoom to country level
                    if (countryCenters[country]) {
                        const { lat, lng, latSmall, lngSmall, zoom, smallScreenZoom } = countryCenters[country];
                        if (window.innerWidth <= 480) {
                            map.setView([latSmall, lngSmall], smallScreenZoom);
                        } else {
                            map.setView([lat, lng], zoom);
                        }
                    }
                    
                    updateMapDisplay();
                });
                regionDropdown.appendChild(defaultRegionItem);

                regions.forEach(reg => {
                    const regionItem = document.createElement("li");
                    regionItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${reg}">${reg}</a>`;
                    regionItem.addEventListener("click", () => {
                        selectedRegion = reg;
                        
                        // Reset dependent selections
                        selectedDepartment = "";
                        selectedCommune = "";
                        
                        // Clear dependent dropdowns
                        document.getElementById("department-select").innerHTML = "";
                        document.getElementById("commune-select").innerHTML = "";
                        
                        // Update dropdown texts
                        document.getElementById("regionDropdown").textContent = reg;
                        document.getElementById("departmentDropdown").textContent = "Default";
                        document.getElementById("communeDropdown").textContent = "Default";
                        
                        // Populate next level dropdown
                        populateDepartmentDropdown(filteredCountryData, country, reg);
                        
                        zoomToFilteredArea(geoJsonData, country, reg, "", "");
                        updateMapDisplay();
                    });
                    regionDropdown.appendChild(regionItem);
                });
            }

            // Populate department dropdown based on the selected region and country
            function populateDepartmentDropdown(filteredCountryData, country, region) {
                const departments = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region).map(f => f.properties.ADM2_FR))];
                departments.sort((a, b) => a.localeCompare(b));
                const departmentDropdown = document.getElementById("department-select");

                // Add "Default" option first
                const defaultDepartmentItem = document.createElement("li");
                defaultDepartmentItem.innerHTML = `<a class="dropdown-item" href="#" data-value="">Default</a>`;
                defaultDepartmentItem.addEventListener("click", () => {
                    selectedDepartment = "";
                    selectedCommune = "";
                    
                    // Clear dependent dropdowns
                    document.getElementById("commune-select").innerHTML = "";
                    
                    // Update dropdown texts
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("communeDropdown").textContent = "Default";
                    
                    // Zoom to region level
                    zoomToFilteredArea(geoJsonData, country, region, "", "");
                    updateMapDisplay();
                });
                departmentDropdown.appendChild(defaultDepartmentItem);

                departments.forEach(dep => {
                    const departmentItem = document.createElement("li");
                    departmentItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${dep}">${dep}</a>`;
                    departmentItem.addEventListener("click", () => {
                        selectedDepartment = dep;
                        
                        // Reset dependent selections
                        selectedCommune = "";
                        
                        // Clear dependent dropdowns
                        document.getElementById("commune-select").innerHTML = "";
                        
                        // Update dropdown texts
                        document.getElementById("departmentDropdown").textContent = dep;
                        document.getElementById("communeDropdown").textContent = "Default";
                        
                        // Populate next level dropdown
                        populateCommuneDropdown(filteredCountryData, country, region, dep);
                        
                        zoomToFilteredArea(geoJsonData, country, region, dep, "");
                        updateMapDisplay();
                    });
                    departmentDropdown.appendChild(departmentItem);
                });
            }

            // Populate commune dropdown based on the selected department, region, and country
            function populateCommuneDropdown(filteredCountryData, country, region, department) {
                const communes = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region && f.properties.ADM2_FR === department).map(f => f.properties.ADM3_FR))];
                communes.sort((a, b) => a.localeCompare(b));
                const communeDropdown = document.getElementById("commune-select");

                // Add "Default" option first
                const defaultCommuneItem = document.createElement("li");
                defaultCommuneItem.innerHTML = `<a class="dropdown-item" href="#" data-value="">Default</a>`;
                defaultCommuneItem.addEventListener("click", () => {
                    selectedCommune = "";
                    
                    // Update dropdown texts
                    document.getElementById("communeDropdown").textContent = "Default";
                    
                    // Zoom to department level
                    zoomToFilteredArea(geoJsonData, country, region, department, "");
                    updateMapDisplay();
                });
                communeDropdown.appendChild(defaultCommuneItem);

                communes.forEach(comm => {
                    const communeItem = document.createElement("li");
                    communeItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${comm}">${comm}</a>`;
                    communeItem.addEventListener("click", () => {
                        selectedCommune = comm;
                        
                        // Update dropdown texts
                        document.getElementById("communeDropdown").textContent = comm;
                        
                        zoomToFilteredArea(geoJsonData, country, region, department, comm);
                        updateMapDisplay();
                    });
                    communeDropdown.appendChild(communeItem);
                });
            }

            // Reset button event
            document.getElementById("resetButton").addEventListener("click", function() {
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

                map.setView([14.5, -1], defaultZoom);

                loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
                document.querySelector('#map-content h1').textContent = 'Spatial Accessibility to Bank Branches';
                document.getElementById("countryDropdown").textContent = "Default";
                document.getElementById("communeDropdown").textContent = "Default";
                document.getElementById("departmentDropdown").textContent = "Default";
                document.getElementById("regionDropdown").textContent = "Default";
                selectedCountry = "";
                selectedCommune = "";
                selectedDepartment = "";
                selectedRegion = "";

                document.getElementById("num-municipalities").innerHTML = '';
                document.getElementById("total-bran").innerHTML = '';
                document.getElementById("percent-pop").innerHTML = '';
                document.getElementById("percent-area").innerHTML = '';

                // toggleswitch reset
                if (toggleSwitch) {
                    toggleSwitch.checked = false;
                }
            });

            // Load initial map data
            loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
 
            /*
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
            */
        } catch(error) {
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

    /*
    info.update = function (props) {
        this.div.innerHTML = props
            ? `<h6>${props.ADM3_FR}</h6><br>Score: ${props.ISIBF_base}`
            : "Hover over";
    };
    info.addTo(map);
    */

    // Function to show/hide commune dropdown based on selected country
    function toggleCommuneDropdown(selectedCountry) {
        const communeLabel = document.querySelector('label[for="commune-select"]');
        const communeDropdownContainer = communeLabel ? communeLabel.nextElementSibling : null;
        
        // Countries where commune dropdown should be hidden
        const hiddenCommuneCountries = ["Benin", "Guinea-Bissau"];
        
        if (communeLabel && communeDropdownContainer) {
            if (hiddenCommuneCountries.includes(selectedCountry)) {
                // Hide both label and dropdown
                communeLabel.style.display = 'none';
                communeDropdownContainer.style.display = 'none';
                
                // Reset commune selection
                const communeButton = document.getElementById('communeDropdown');
                if (communeButton) {
                    communeButton.textContent = 'Default';
                }
            } else {
                // Show both label and dropdown
                communeLabel.style.display = 'block';
                communeDropdownContainer.style.display = 'block';
            }
        }
    }


    
    function loadMapData(geoJsonData, country, region, department, commune, selectedEquipment) {
        map.eachLayer(layer => {
            if (layer instanceof L.GeoJSON) {
                map.removeLayer(layer);
            }
        });

        toggleCommuneDropdown(country)
    
        // Filter GeoJSON data based on the selected commune, department, or region
        const filteredData = geoJsonData.features.filter(feature => {
            return (!country || feature.properties.ADM0_EN === country) && 
                   (!commune || feature.properties.ADM3_FR === commune) &&
                   (!department || feature.properties.ADM2_FR === department) &&
                   (!region || feature.properties.ADM1_FR === region);
        });

        // Listen for changes in the country dropdown
        document.querySelectorAll('#country-select a').forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const country = this.textContent;
                // Update the dropdown button text (optional)
                document.getElementById('countryDropdown').textContent = country;
            });

            // Listen for changes in the region dropdown
            document.querySelectorAll('#region-select a').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const region = this.textContent;
                    // Update the dropdown button text (optional)
                    document.getElementById('regionDropdown').textContent = region;
                });

                // Listen for changes in the department dropdown
                document.querySelectorAll('#department-select a').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const department = this.textContent;
                        // Update the dropdown button text (optional)
                        document.getElementById('departmentDropdown').textContent = department;
                    });
                });
            });
        });


    
        const geoJsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
            onEachFeature: function (feature, layer) {

                layer.on({
                    mouseover: function(e) {
                        // Highlight polygon
                        e.target.setStyle({ weight: 1.5, color: "black", fillOpacity: 0.7 });

                        // Create tooltip with ADM3_FR
                        tooltip = L.tooltip({
                            permanent: false,
                            direction: 'top',
                            className: 'custom-tooltip',
                            opacity: 0.9
                        })
                        .setContent(e.target.feature.properties.ADM3_FR + ' : ' + e.target.feature.properties.ISIBF_base.toFixed(2)) // <-- show the name
                        .setLatLng(e.latlng);

                        // Add tooltip to map
                        tooltip.addTo(map);
                    },
                    mouseout: function(e) {
                        // Reset style
                        geoJsonLayer.resetStyle(e.target);

                        // Remove tooltip
                        if (tooltip) {
                            map.removeLayer(tooltip);
                            tooltip = null;
                        }
                    },
                    click: function (e) {
                        
                        // Highlight the clicked feature
                        e.target.setStyle({ weight: 2, color: "black", fillOpacity: 2 });

                        // Filter the data for the clicked feature (commune)
                        const clickedFeature = e.target.feature;
                        const country = clickedFeature.properties.ADM0_EN;
                        const region = clickedFeature.properties.ADM1_FR;
                        const department = clickedFeature.properties.ADM2_FR;
                        const commune = clickedFeature.properties.ADM3_FR;
                        
                        let titleText = `Spatial Accessibility to Bank Branches`;
                        let locationText = "";

                        if (commune) {
                            locationText = `${commune} - ${department}, ${region}, ${country}`;
                        } else if (department) {
                            locationText = `${department} - ${region}, ${country}`;
                        } else if (region) {
                            locationText = `${region} - ${country}`;
                        } else {
                            locationText = `${country}`;
                        }

                        document.querySelector('#map-content h1').innerHTML = `
                            <span class="title-main">${titleText}</span><br>
                            ${locationText}`;

                        // Filter the data for the clicked commune
                        const filteredCommuneData = geoJsonData.features.filter(f =>
                            f.properties.ADM0_EN === country &&
                            f.properties.ADM1_FR === region &&
                            f.properties.ADM2_FR === department &&
                            f.properties.ADM3_FR === commune
                        );

                        // Filter the data for the entire country
                        const filteredCountryData = geoJsonData.features.filter(f =>
                            f.properties.ADM0_EN === country
                        );

                        // Call updateStats with the filtered data
                        updateStats(filteredCountryData, filteredCommuneData, country);
                        document.getElementById("countryDropdown").textContent = country;
                        document.getElementById("regionDropdown").textContent = region;
                        document.getElementById("departmentDropdown").textContent = department;
                        document.getElementById("communeDropdown").textContent = commune;
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
                    color: (feature.properties.ADM0_EN !== undefined) ? "#abababff" : "transparent", // Darker border for country boundaries #abababff
                    fillOpacity: 0.9,  // Make sure the polygons are opaque enough
                    zIndex: 1
                };
            }
        }).addTo(map);

        updateLegend();
        updateBorders(country);

    }

    function updateBorders(country) {

        if (countryBorders[country]) {
            fetch(countryBorders[country])
                .then(response => response.json())
                .then(data => {
                    currentBorderLayer = L.geoJSON(data, {
                        style: function () {
                            return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style
                        }
                    }).addTo(map);
                })
                .catch(error => console.error('Error loading country borders:', error));
        }
    }


    function updateLegend(country) {
        if (legend) {
            legend.remove();  // Remove previous legend before adding a new one
        }

        legend = L.control({ position: "bottomright" });

        const grades = [1, 0.5, 0.2, 0.1, 0.01];

        legend.onAdd = function () {
            const div = L.DomUtil.create("div", "legend");

            div.innerHTML += "<strong>Scores of access</strong><br>";
            for (let i = 0; i < grades.length; i++) {
                div.innerHTML += `<i style="background:${getColor(grades[i], country)}"></i> ${
                    grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "-0"}<br>`;
            }

            return div;
        };

        legend.addTo(map);  // Add the new legend
        /*
         if (['Cameroon', 'Chad'].includes(country)) {
            legend = L.control({ position: "bottomright" });
    
            const grades = [1, 0.5, 0.1, 0.01, 0.001];
    
            legend.onAdd = function () {
                const div = L.DomUtil.create("div", "legend");
    
                div.innerHTML += "<strong>Score</strong><br>";
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
    
                div.innerHTML += "<strong>Score</strong><br>";
                for (let i = 0; i < grades.length; i++) {
                    div.innerHTML += `<i style="background:${getColor(grades[i], country)}"></i> ${
                        grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "-0"}<br>`;
                }
    
                return div;
            };
            legend.addTo(map);  // Add the new legend
        }
            */
    } 



    function getColor(value) {
        return value > 0.5 ? "#67000d" :  // Darkest
            value > 0.2 ? "#d32020" :
            value > 0.1 ? "#fb7050" :
            value > 0.01 ? "#fcbea5" :  // Lightest
            "#fff5f0";  // Lightest
        /*
        if (['Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'].includes(country)) {
            return value > 0.5 ? "#67000d" :  // Darkest
            value > 0.2 ? "#d32020" :
            value > 0.1 ? "#fb7050" :
            value > 0.01 ? "#fcbea5" :  // Lightest
            "#fff5f0";  // Lightest
     
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
        */
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

    const rgph = {
        "Benin": 2013,
        "Burkina Faso": 2019,
        "Mali": 2009,
        "Niger": 2012,
        "Ivory Coast": 2021,
        "Guinea-Bissau": 2009,
        "Senegal": 2023,
        "Togo": 2022,
        "Ghana": 2013,
        "Cameroon": 2013,
        "Chad": 2013,
        "Nigeria": 2013
    };

    // Function to update statistics dynamically based on filtered data
    function updateStats(filteredDataCountry, filteredData, country) {

        const popCountries = ['Nigeria', 'Cameroon', 'Ghana', 'Chad', 'Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'];
        if (popCountries.includes(country)) {
            const municipalityLabel = municipalities[country] || "Municipalities"; // Default fallback to "Municipalities"
            const rgphDate = rgph[country] || 0;

            // Calculate the total number of communes, branches, population, and area
            const totalCommunes = filteredData.length;
            const totalBranches = filteredData.reduce((sum, feature) => sum + (feature.properties.Total_bran || 0), 0);

            const totalPopulation = filteredData.reduce((sum, feature) => sum + (Number(feature.properties.Population) || 0), 0);

            const totalArea = filteredData.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);
            const totalAreaKm2 = (totalArea / 1000000).toFixed(0); // Convert to km²

            // Calculate total population and area for the entire country
            const totalCountryPopulation = filteredDataCountry.reduce((sum, feature) => sum + (Number(feature.properties.Population) || 0), 0);
            const totalCountryArea = filteredDataCountry.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);
            const totalCountryBranches = filteredDataCountry.reduce((sum, feature) => sum + (feature.properties.Total_bran || 0), 0);
    
            // Calculate the percentage of population and area for the filtered region
            const populationPercentage = totalCountryPopulation > 0 ? ((totalPopulation / totalCountryPopulation) * 100).toFixed(1) : 0;
            const areaPercentage = totalCountryArea > 0 ? ((totalArea / totalCountryArea) * 100).toFixed(1) : 0;
            const branchPercentage = totalCountryBranches > 0 ? ((totalBranches / totalCountryBranches) * 100).toFixed(1) : 0;
            
            // If only one commune is selected, display its name
            if (filteredData.length === 1) {
                const communeName = filteredData[0].properties.ADM3_FR;
                const communeScore = (filteredData[0].properties.ISIBF_base || 0).toFixed(2);
                console.log(`Score for ${communeName}: ${communeScore}`);
                document.getElementById("num-municipalities").innerHTML = `<span>Score: ${communeScore}</span>`;
            } else {
                // Otherwise, display the number of communes
                document.getElementById("num-municipalities").innerHTML = `<span>${totalCommunes}</span>${municipalityLabel}`;
            }
            /*
            document.getElementById("total-bran").innerHTML = `<span>${branchPercentage}%</span>of total bank branches`;
            document.getElementById("percent-pop").innerHTML = `<span>${populationPercentage}%</span>of total population`;
            document.getElementById("percent-area").innerHTML = `<span>${areaPercentage}%</span>of total area`;
            */
            document.getElementById("total-bran").innerHTML = `<span>${totalBranches}</span>Bank Branches`;
            document.getElementById("percent-pop").innerHTML = `<span>${totalPopulation}</span>Population (${rgphDate})`;
            document.getElementById("percent-area").innerHTML = `<span>${totalAreaKm2}</span>Area (km²)`;


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

    
    function loadIsochrone(geoJsonData, isochroneData, country, region, department, commune, selectedEquipment) {
        changeColorLayer(geoJsonData, country, region, department, commune, selectedEquipment);

    
        // Filter GeoJSON data based on the selected commune, department, or region
        const filteredData = isochroneData.features.filter(feature => {
            return (!country || feature.properties.ADM0_EN === country) && 
                   (!commune || feature.properties.ADM3_FR === commune) &&
                   (!department || feature.properties.ADM2_FR === department) &&
                   (!region || feature.properties.ADM1_FR === region);
        });

        // Listen for changes in the country dropdown
        document.querySelectorAll('#country-select a').forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const country = this.textContent;
                // Update the dropdown button text (optional)
                document.getElementById('countryDropdown').textContent = country;
            });

            // Listen for changes in the region dropdown
            document.querySelectorAll('#region-select a').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const region = this.textContent;
                    // Update the dropdown button text (optional)
                    document.getElementById('regionDropdown').textContent = region;
                });

                // Listen for changes in the department dropdown
                document.querySelectorAll('#department-select a').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const department = this.textContent;
                        // Update the dropdown button text (optional)
                        document.getElementById('departmentDropdown').textContent = department;
                    });
                });

                // Listen for changes in the commune dropdown
                document.querySelectorAll('#commune-select a').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const commune = this.textContent;
                        // Update the dropdown button text (optional)
                        document.getElementById('communeDropdown').textContent = commune;
                    });
                });

            });
        });



        
        const geoJsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
            onEachFeature: function (feature, layer) {

                layer.on({
                    mouseover: function(e) {
                        // Highlight polygon
                        e.target.setStyle({ weight: 1.5, color: "black", fillOpacity: 2 });
                        // Create tooltip at mouse position
                        tooltip = L.tooltip({
                            permanent: false,
                            direction: 'top',
                            className: 'custom-tooltip',
                            opacity: 0.9,
                        })
                    },
                    mouseout: function(e) {
                        // Reset style
                        geoJsonLayer.resetStyle(e.target);

                        // Remove tooltip
                        if (tooltip) {
                            map.removeLayer(tooltip);
                            tooltip = null;
                        }
                    },
                    click: function (e) {
                        
                        // Highlight the clicked feature
                        e.target.setStyle({ weight: 2, color: "black", fillOpacity: 2 });

                        // Filter the data for the clicked feature (commune)
                        const clickedFeature = e.target.feature;
                        const country = clickedFeature.properties.ADM0_EN;
                        const region = clickedFeature.properties.ADM1_FR;
                        const department = clickedFeature.properties.ADM2_FR;
                        const commune = clickedFeature.properties.ADM3_FR;
                        document.querySelector('#map-content h1').textContent = `Area Covered By At Least One Bank Branch in ${commune} - ${department}, ${region}, ${country}`;

                        // Filter the data for the clicked commune
                        const filteredCommuneData = geoJsonData.features.filter(f =>
                            f.properties.ADM0_EN === country &&
                            f.properties.ADM1_FR === region &&
                            f.properties.ADM2_FR === department &&
                            f.properties.ADM3_FR === commune
                        );

                        // Filter the data for the entire country
                        const filteredCountryData = geoJsonData.features.filter(f =>
                            f.properties.ADM0_EN === country
                        );


                        document.getElementById("countryDropdown").textContent = country;
                        document.getElementById("regionDropdown").textContent = region;
                        document.getElementById("departmentDropdown").textContent = department;
                        document.getElementById("communeDropdown").textContent = commune;
                    }

            });
            },
            style: function (feature) {
                const timeTravel = feature.properties.group_inde || 0;
                const country = feature.properties.ADM0_EN;  // Corrected reference to country property
                const fillColor = getIsochroneColor(timeTravel);

                return {
                    fillColor: fillColor, 
                    weight: 0.3,  // Default border weight
                    opacity: 0.1, // Border opacity
                    color: (feature.properties.ADM0_EN !== undefined) ? "#6d6b6ab7" : "transparent", // Darker border for country boundaries #abababff
                    fillOpacity: 3,  // Make sure the polygons are opaque enough
                    zIndex: 1000,
                };
            }
        }).addTo(map);



        updateLegendIsochrone();
        updateBorders(country);


    }

    function updateLegendIsochrone() {
        if (legend) {
            legend.remove();
        }
        
        legend = L.control({ position: "bottomright" });
        
        legend.onAdd = function () {
            const div = L.DomUtil.create("div", "legend");
            div.innerHTML += "<strong>Time Travels</strong><br>";
            div.innerHTML += `<i style="background:${getIsochroneColor(15)}"></i> 0-15 min<br>`;
            div.innerHTML += `<i style="background:${getIsochroneColor(30)}"></i> 15-30 min<br>`;
            div.innerHTML += `<i style="background:${getIsochroneColor(45)}"></i> 30-45 min<br>`;
            div.innerHTML += `<i style="background:${getIsochroneColor(60)}"></i> 45-60 min<br>`;
            div.innerHTML += `<i style="background:#6d6b6ab7"></i> >60 min<br>`;
            return div;
        };
        
        legend.addTo(map);
    }



    function getIsochroneColor(timeTravel) {
        // Color mapping based on country
        if (timeTravel) {
        return timeTravel === 15 ? "#bd0026" :  // Darkest
            timeTravel === 30 ? "#fd8d3c" :
            timeTravel === 45 ? "#fecc5c" :
            timeTravel === 60 ? "#ffffb2" :  // Lightest
            "#6d6b6ab7";  // Lightest
     
        } else {
            return "#6d6b6ab7"; // Default color if no country matches
        }
    }

    function updatePercentage(filteredIsochroneData, country, filteredData) {
        const popCountries = ['Nigeria', 'Cameroon', 'Ghana', 'Chad', 'Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'];

        if (popCountries.includes(country)) {

            const totalAdminArea = filteredData.reduce((sum, feature) => sum + (feature.properties.Area || 0), 0);

            // Calculate the total area for each isochrone group within the administrative unit
            const totalIsochrone15 = filteredIsochroneData.reduce(
                (sum, feature) => sum + ((feature.properties.group_inde === 15 ? feature.properties.area_iso : 0) || 0),
                0
            );
            const totalIsochrone30 = filteredIsochroneData.reduce(
                (sum, feature) => sum + ((feature.properties.group_inde === 30 ? feature.properties.area_iso : 0) || 0),
                0
            );
            const totalIsochrone45 = filteredIsochroneData.reduce(
                (sum, feature) => sum + ((feature.properties.group_inde === 45 ? feature.properties.area_iso : 0) || 0),
                0
            );
            const totalIsochrone60 = filteredIsochroneData.reduce(
                (sum, feature) => sum + ((feature.properties.group_inde === 60 ? feature.properties.area_iso : 0) || 0),
                0
            );

            // Calculate the percentage for each isochrone group
            const isochrone15 = ((totalIsochrone15 / totalAdminArea) * 100).toFixed(1);
            const isochrone30 = ((totalIsochrone30 / totalAdminArea) * 100).toFixed(1);
            const isochrone45 = ((totalIsochrone45 / totalAdminArea) * 100).toFixed(1);
            const isochrone60 = ((totalIsochrone60 / totalAdminArea) * 100).toFixed(1);

            // Update the HTML elements
            document.getElementById("num-municipalities").innerHTML = `<span>${isochrone15}%</span>within 0-15min`;
            document.getElementById("total-bran").innerHTML = `<span>${isochrone30}%</span>within 15-30min`;
            document.getElementById("percent-pop").innerHTML = `<span>${isochrone45}%</span>within 30-45min`;
            document.getElementById("percent-area").innerHTML = `<span>${isochrone60}%</span>within 45-60min`;
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


    function changeColorLayer(geoJsonData, country, region, department, commune, selectedEquipment) {
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
            style: function (feature) {
                return {
                    fillColor: "#abababff", 
                    weight: 0.3,  // Default border weight
                    opacity: 0.3, // Border opacity
                    color: (feature.properties.ADM0_EN !== undefined) ? "#abababff" : "transparent", // Darker border for country boundaries #abababff
                    fillOpacity: 0.9,  // Make sure the polygons are opaque enough
                    zIndex: 1
                };
            }
        }).addTo(map);
    }


    document.getElementById("map-btn").addEventListener("click", function() {
            showContent("map-content");
            loadMapData(geoJsonData, "", "", "", "", "ISIBF_base");
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
        });


    document.getElementById("conclusion-btn").addEventListener("click", function() {
        showContent("conclusion-content");
    });

    function showContent(contentId) {
        document.getElementById("map-content").style.display = "none";
        document.getElementById("conclusion-content").style.display = "none";
        document.getElementById(contentId).style.display = "flex";
        currentPage = contentId;
    }
});



