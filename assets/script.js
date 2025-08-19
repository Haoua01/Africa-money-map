document.addEventListener("DOMContentLoaded", async function () {
    let defaultZoom = 5;
    let smallScreenZoom = 4; 
    let currentZoom = window.innerWidth <= 480 ? smallScreenZoom : defaultZoom;
    const map = L.map("map").setView([14.5, -1], currentZoom);


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

    const geoJsonFile = "data/Indicators/Hybrid/hybrid_scores.geojson"; 
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
    const uemoaData = await fetch(uemoaBordersFile).then(response => response.json());

    const isochroneData = await fetch(isochroneFile).then(response => response.json());
    
    // const cemacData = await fetch(cemacBordersFile).then(response => response.json());
    // const ghanaData = await fetch(ghanaBordersFile).then(response => response.json());
    // const nigeriaData = await fetch(nigeriaBordersFile).then(response => response.json());
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
                "Benin": { lat: 9.3, lng: 2.5, latSmall: 7.3, lngSmall: 2.5, zoom: 7, smallScreenZoom: 6 },
                "Burkina Faso": { lat: 12.4, lng: -1.5, latSmall: 11.4, lngSmall: -1.5, zoom: 7, smallScreenZoom: 6 },
                "Ivory Coast": { lat: 7.5, lng: -5.5, latSmall: 5.5, lngSmall: -5.5, zoom: 7, smallScreenZoom: 6 },
                "Guinea-Bissau": { lat: 11.5, lng: -15.7, latSmall: 10.5, lngSmall: -15.2, zoom: 8, smallScreenZoom: 7 },
                "Mali": {lat: 12.6, lng: -8, latSmall: 12.6, lngSmall: -4, zoom: 5, smallScreenZoom: 5 },
                "Niger": { lat: 17.6, lng: 8, latSmall: 13.6, lngSmall: 8, zoom: 6, smallScreenZoom: 5 },
                "Senegal": { lat: 14.5, lng: -14, latSmall: 12.5, lngSmall: -15, zoom: 7, smallScreenZoom: 6 },
                "Togo": { lat: 8.2, lng: 1.3, latSmall: 6.8, lngSmall: 1.3, zoom: 7, smallScreenZoom: 6 },
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

                    // Load map data
                    loadMapData(geoJsonData, coun, "", "", "", selectedEquipment);
                    updateStats(filteredCountryData,filteredCountryData, coun);
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
                        zoomToFilteredArea(geoJsonData, country, reg, "", "");
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
                        zoomToFilteredArea(geoJsonData, country, region, dep, "");
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
                        zoomToFilteredArea(geoJsonData, country, region, department, comm);

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
    
                loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
                document.querySelector('#map-content h1').textContent = 'Spatial Access to Bank Branches';
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
            });

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

    /*
    info.update = function (props) {
        this.div.innerHTML = props
            ? `<h6>${props.ADM3_FR}</h6><br>Score: ${props.ISIBF_base}`
            : "Hover over";
    };
    info.addTo(map);
    */

    
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

        // Listen for changes in the country dropdown
        document.querySelectorAll('#country-select a').forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const country = this.textContent;
                // Update the h1 text
                document.querySelector('#map-content h1').textContent = `Spatial Access to Bank Branches in ${country}`;
                // Update the dropdown button text (optional)
                document.getElementById('countryDropdown').textContent = country;
            });

            // Listen for changes in the region dropdown
            document.querySelectorAll('#region-select a').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const region = this.textContent;
                    // Update the h1 text
                    document.querySelector('#map-content h1').textContent = `Spatial Access to Bank Branches in ${region}, ${country}`;
                    // Update the dropdown button text (optional)
                    document.getElementById('regionDropdown').textContent = region;
                });

                // Listen for changes in the department dropdown
                document.querySelectorAll('#department-select a').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const department = this.textContent;
                        // Update the h1 text
                        document.querySelector('#map-content h1').textContent = `Spatial Access to Bank Branches in ${department}, ${region}, ${country}`;
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
                        document.querySelector('#map-content h1').textContent = `Spatial Access to Bank Branches in ${country}`;

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
                    fillOpacity: 0.9  // Make sure the polygons are opaque enough
                };
            }
        }).addTo(map);

        updateLegend(country);
        updateBorders(country);

    }

    function updateBorders(country) {

        if (countryBorders[country]) {
            fetch(countryBorders[country])
                .then(response => response.json())
                .then(data => {
                    L.geoJSON(data, {
                        style: function () {
                            return { color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }; // Border style
                        }
                    }).addTo(map);
                })
                .catch(error => console.error('Error loading country borders:', error));
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
            
            // If only one commune is selected, display its name
            if (filteredData.length === 1) {
                const communeName = filteredData[0].properties.ADM3_FR;
                const communeScore = (filteredData[0].properties.ISIBF_base || 0).toFixed(2);
                console.log(`Score for ${communeName}: ${communeScore}`);
                document.getElementById("num-municipalities").innerHTML = `<span>${communeName}</span><span>Score: ${communeScore}</span>`;
            } else {
                // Otherwise, display the number of communes
                document.getElementById("num-municipalities").innerHTML = `<span>${totalCommunes}</span>${municipalityLabel}`;
            }
            // Update the statistics in the HTML
            document.getElementById("total-bran").innerHTML = `<span>${branchPercentage}%</span>of total bank branches`;
            document.getElementById("percent-pop").innerHTML = `<span>${populationPercentage}%</span>of total population`;
            document.getElementById("percent-area").innerHTML = `<span>${areaPercentage}%</span>of total area`;

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