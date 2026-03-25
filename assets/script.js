document.addEventListener("DOMContentLoaded", async function () {

    // ═══════════════════════════════════════════════════════════════
    // SECTION 1 – MAIN MAP (Isochrone Coverage)
    // ═══════════════════════════════════════════════════════════════

    let defaultZoom = 5;
    let smallScreenZoom = 4;
    let currentZoom = window.innerWidth <= 480 ? smallScreenZoom : defaultZoom;
    const map = L.map("map").setView([14.5, -1], currentZoom);

    let legend;

    // Global variables
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
        position: 'topleft',
        title: 'Show me the fullscreen !',
        titleCancel: 'Exit fullscreen mode',
        content: null,
        forceSeparateButton: true,
        forcePseudoFullscreen: true,
        fullscreenElement: false
    }).addTo(map);

    const geoJsonFile = "data/Indicators/Hybrid/scores_corrected.geojson";
    const isochroneFile = "data/Indicators/Fully_isochrone/isochrone_map.geojson";
    const uemoaBordersFile = "web_data/uemoa_borders.geojson";

    const beninBordersFile    = "data/UEMOA/adm_shapefiles/borders/benin_borders.geojson";
    const burkinaBordersFile  = "data/UEMOA/adm_shapefiles/borders/burkina_borders.geojson";
    const civBordersFile      = "data/UEMOA/adm_shapefiles/borders/civ_borders.geojson";
    const guineeBordersFile   = "data/UEMOA/adm_shapefiles/borders/guinee_borders.geojson";
    const maliBordersFile     = "data/UEMOA/adm_shapefiles/borders/mali_borders.geojson";
    const nigerBordersFile    = "data/UEMOA/adm_shapefiles/borders/niger_borders.geojson";
    const senegalBordersFile  = "data/UEMOA/adm_shapefiles/borders/senegal_borders.geojson";
    const togoBordersFile     = "data/UEMOA/adm_shapefiles/borders/togo_borders.geojson";
    const ghanaBordersFile    = "web_data/ghana_borders.geojson";
    const nigeriaBordersFile  = "web_data/nigeria_borders.geojson";
    const cameroonBordersFile = "web_data/cameroun_borders.geojson";
    const chadBordersFile     = "web_data/tchad_borders.geojson";


    const countryBorders = {
        "Benin":        beninBordersFile,
        "Burkina Faso": burkinaBordersFile,
        "Ivory Coast":  civBordersFile,
        "Guinea-Bissau":guineeBordersFile,
        "Mali":         maliBordersFile,
        "Niger":        nigerBordersFile,
        "Senegal":      senegalBordersFile,
        "Togo":         togoBordersFile,
        "Ghana":        ghanaBordersFile,
        "Nigeria":      nigeriaBordersFile,
        "Cameroon":     cameroonBordersFile,
        "Chad":         chadBordersFile
    };

    // Loading spinner
    const loadingSpinner = document.createElement("div");
    loadingSpinner.className = "loading-spinner";
    loadingSpinner.innerHTML = `<div class="spinner"></div><span>Please wait for map to load...</span>`;
    document.body.appendChild(loadingSpinner);

    setTimeout(() => {
        if (document.body.contains(loadingSpinner)) {
            document.body.removeChild(loadingSpinner);
        }
    }, 3500);

    try {
        const [geoJsonResponse, isochroneResponse, uemoaResponse] = await Promise.all([
            fetch(geoJsonFile),
            fetch(isochroneFile),
            fetch(uemoaBordersFile)
        ]);

        geoJsonData    = await geoJsonResponse.json();
        isochroneData  = await isochroneResponse.json();
        const uemoaData = await uemoaResponse.json();

        console.log('Both datasets loaded successfully');

        // Toggle switch – initial binding (show/hide layer only)
        toggleSwitch.addEventListener('change', () => {
            if (toggleSwitch.checked) {
                if (currentIsochroneLayer) map.addLayer(currentIsochroneLayer);
            } else {
                if (currentIsochroneLayer) map.removeLayer(currentIsochroneLayer);
            }
        });

        let selectedEquipment = "ISIBF_base";
        let selectedCommune   = "";
        let selectedDepartment = "";
        let selectedRegion    = "";
        let selectedCountry   = "";

        // ── updateMapDisplay ──────────────────────────────────────
        function updateMapDisplay() {
            if (!selectedCountry) {
                if (toggleSwitch.checked) {
                    loadIsochrone(geoJsonData, isochroneData, "", "", "", "", selectedEquipment);
                    document.querySelector('#map-content h1').textContent = `Area Covered By At Least One Bank Branch`;
                } else {
                    loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
                    document.querySelector('#map-content h1').textContent = `Spatial Accessibility to Bank Branches`;
                }
                fetch(uemoaBordersFile)
                    .then(r => r.json())
                    .then(data => {
                        L.geoJSON(data, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(map);
                    })
                    .catch(err => console.error('Error loading UEMOA borders:', err));
                return;
            }

            const countryData = geoJsonData.features.filter(f => f.properties.ADM0_EN === selectedCountry);
            const isochroneCountryData = isochroneData.features.filter(f => f.properties.ADM0_EN === selectedCountry);

            let filteredData = countryData.filter(f =>
                (!selectedRegion     || f.properties.ADM1_FR === selectedRegion) &&
                (!selectedDepartment || f.properties.ADM2_FR === selectedDepartment) &&
                (!selectedCommune    || f.properties.ADM3_FR === selectedCommune)
            );
            let isochroneFilteredData = isochroneCountryData.filter(f =>
                (!selectedRegion     || f.properties.ADM1_FR === selectedRegion) &&
                (!selectedDepartment || f.properties.ADM2_FR === selectedDepartment) &&
                (!selectedCommune    || f.properties.ADM3_FR === selectedCommune)
            );

            toggleCommuneDropdown(selectedCountry);

            const makeLocationText = () => {
                if (selectedCommune)    return `${selectedCommune} - ${selectedDepartment}, ${selectedRegion}, ${selectedCountry}`;
                if (selectedDepartment) return `${selectedDepartment} - ${selectedRegion}, ${selectedCountry}`;
                if (selectedRegion)     return `${selectedRegion} - ${selectedCountry}`;
                return selectedCountry;
            };

            if (toggleSwitch.checked) {
                document.querySelector('#map-content h1').innerHTML =
                    `<span class="title-main">Area Covered By At Least One Bank Branch</span><br>${makeLocationText()}`;
                document.getElementById("num-municipalities").innerHTML = '';
                document.getElementById("total-bran").innerHTML = '';
                document.getElementById("percent-pop").innerHTML = '';
                document.getElementById("percent-area").innerHTML = '';
                loadIsochrone(geoJsonData, isochroneData, selectedCountry, selectedRegion, selectedDepartment, selectedCommune, selectedEquipment);
                updatePercentage(isochroneFilteredData, selectedCountry, filteredData);
            } else {
                document.querySelector('#map-content h1').innerHTML =
                    `<span class="title-main">Spatial Accessibility to Bank Branches</span><br>${makeLocationText()}`;
                document.getElementById("num-municipalities").innerHTML = '';
                document.getElementById("total-bran").innerHTML = '';
                document.getElementById("percent-pop").innerHTML = '';
                document.getElementById("percent-area").innerHTML = '';
                loadMapData(geoJsonData, selectedCountry, selectedRegion, selectedDepartment, selectedCommune, selectedEquipment);
                updateStats(countryData, filteredData, selectedCountry);
            }
        }

        // Toggle switch – also calls updateMapDisplay
        toggleSwitch.addEventListener('change', () => { updateMapDisplay(); });

        // ── Country dropdown ──────────────────────────────────────
        const countries = [...new Set(geoJsonData.features.map(f => f.properties.ADM0_EN))].sort((a, b) => a.localeCompare(b));

        const countryCenters = {
            "Benin":        { lat: 9.3,  lng: 2.5,  latSmall: 9.3,  lngSmall: 2.5,   zoom: 7, smallScreenZoom: 6 },
            "Burkina Faso": { lat: 12.4, lng: -1.5, latSmall: 12.4, lngSmall: -1.5,  zoom: 7, smallScreenZoom: 5 },
            "Ivory Coast":  { lat: 7.5,  lng: -5.5, latSmall: 7.5,  lngSmall: -5.5,  zoom: 7, smallScreenZoom: 6 },
            "Guinea-Bissau":{ lat: 11.5, lng:-15.7, latSmall: 11.5, lngSmall:-15.2,  zoom: 8, smallScreenZoom: 7 },
            "Mali":         { lat: 12.6, lng: -8,   latSmall: 14.6, lngSmall: -6,    zoom: 5, smallScreenZoom: 4 },
            "Niger":        { lat: 17.6, lng: 8,    latSmall: 13.6, lngSmall: 8,     zoom: 6, smallScreenZoom: 4 },
            "Senegal":      { lat: 14.5, lng:-14,   latSmall: 14.5, lngSmall:-14.5,  zoom: 7, smallScreenZoom: 6 },
            "Togo":         { lat: 8.2,  lng: 1.3,  latSmall: 8.2,  lngSmall: 0.9,   zoom: 7, smallScreenZoom: 6 }
        };

        const countryDropdown = document.getElementById("country-select");
        document.getElementById("commune-select").innerHTML    = "";
        document.getElementById("department-select").innerHTML = "";
        document.getElementById("region-select").innerHTML     = "";

        countries.forEach(coun => {
            updateBorders(coun);
            const filteredCountryData   = geoJsonData.features.filter(f => f.properties.ADM0_EN === coun);
            const filteredIsochroneData = isochroneData.features.filter(f => f.properties.ADM0_EN === coun);

            const listItem = document.createElement("li");
            listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${coun}">${coun}</a>`;
            listItem.addEventListener("click", () => {
                selectedCountry    = coun;
                selectedCommune    = "";
                selectedDepartment = "";
                selectedRegion     = "";

                document.getElementById("region-select").innerHTML    = "";
                document.getElementById("department-select").innerHTML = "";
                document.getElementById("commune-select").innerHTML    = "";

                document.getElementById("countryDropdown").textContent    = coun;
                document.getElementById("regionDropdown").textContent     = "";
                document.getElementById("departmentDropdown").textContent = "";
                document.getElementById("communeDropdown").textContent    = "";

                populateRegionDropdown(filteredCountryData, coun);

                if (countryCenters[coun]) {
                    const { lat, lng, latSmall, lngSmall, zoom, smallScreenZoom } = countryCenters[coun];
                    map.setView(window.innerWidth <= 480 ? [latSmall, lngSmall] : [lat, lng], window.innerWidth <= 480 ? smallScreenZoom : zoom);
                }

                document.getElementById("num-municipalities").innerHTML = '';
                document.getElementById("total-bran").innerHTML         = '';
                document.getElementById("percent-pop").innerHTML        = '';
                document.getElementById("percent-area").innerHTML       = '';

                updateMapDisplay();
            });

            countryDropdown.appendChild(listItem);
        });

        // ── Zoom helper ───────────────────────────────────────────
        function zoomToFilteredArea(geoJsonData, country, region, department, commune) {
            const filteredFeatures = geoJsonData.features.filter(f =>
                (!country    || f.properties.ADM0_EN === country) &&
                (!region     || f.properties.ADM1_FR === region) &&
                (!department || f.properties.ADM2_FR === department) &&
                (!commune    || f.properties.ADM3_FR === commune)
            );
            if (!filteredFeatures.length) return;
            const bounds = L.geoJSON({ type: "FeatureCollection", features: filteredFeatures }).getBounds();
            if (bounds.isValid()) {
                map.fitBounds(bounds, {
                    padding: [20, 20],
                    maxZoom: commune ? 12 : department ? 10 : region ? 8 : 7
                });
            }
        }

        // ── Region dropdown ───────────────────────────────────────
        function populateRegionDropdown(filteredCountryData, country) {
            const regions = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country).map(f => f.properties.ADM1_FR))].sort((a, b) => a.localeCompare(b));
            const regionDropdown = document.getElementById("region-select");

            const defaultItem = document.createElement("li");
            defaultItem.innerHTML = `<a class="dropdown-item" href="#">Default</a>`;
            defaultItem.addEventListener("click", () => {
                selectedRegion = ""; selectedDepartment = ""; selectedCommune = "";
                document.getElementById("department-select").innerHTML = "";
                document.getElementById("commune-select").innerHTML    = "";
                document.getElementById("regionDropdown").textContent     = "Default";
                document.getElementById("departmentDropdown").textContent = "Default";
                document.getElementById("communeDropdown").textContent    = "Default";
                if (countryCenters[country]) {
                    const { lat, lng, latSmall, lngSmall, zoom, smallScreenZoom } = countryCenters[country];
                    map.setView(window.innerWidth <= 480 ? [latSmall, lngSmall] : [lat, lng], window.innerWidth <= 480 ? smallScreenZoom : zoom);
                }
                updateMapDisplay();
            });
            regionDropdown.appendChild(defaultItem);

            regions.forEach(reg => {
                const regionItem = document.createElement("li");
                regionItem.innerHTML = `<a class="dropdown-item" href="#">${reg}</a>`;
                regionItem.addEventListener("click", () => {
                    selectedRegion = reg; selectedDepartment = ""; selectedCommune = "";
                    document.getElementById("department-select").innerHTML = "";
                    document.getElementById("commune-select").innerHTML    = "";
                    document.getElementById("regionDropdown").textContent     = reg;
                    document.getElementById("departmentDropdown").textContent = "Default";
                    document.getElementById("communeDropdown").textContent    = "Default";
                    populateDepartmentDropdown(filteredCountryData, country, reg);
                    zoomToFilteredArea(geoJsonData, country, reg, "", "");
                    updateMapDisplay();
                });
                regionDropdown.appendChild(regionItem);
            });
        }

        // ── Department dropdown ───────────────────────────────────
        function populateDepartmentDropdown(filteredCountryData, country, region) {
            const departments = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region).map(f => f.properties.ADM2_FR))].sort((a, b) => a.localeCompare(b));
            const departmentDropdown = document.getElementById("department-select");

            const defaultItem = document.createElement("li");
            defaultItem.innerHTML = `<a class="dropdown-item" href="#">Default</a>`;
            defaultItem.addEventListener("click", () => {
                selectedDepartment = ""; selectedCommune = "";
                document.getElementById("commune-select").innerHTML    = "";
                document.getElementById("departmentDropdown").textContent = "Default";
                document.getElementById("communeDropdown").textContent    = "Default";
                zoomToFilteredArea(geoJsonData, country, region, "", "");
                updateMapDisplay();
            });
            departmentDropdown.appendChild(defaultItem);

            departments.forEach(dep => {
                const depItem = document.createElement("li");
                depItem.innerHTML = `<a class="dropdown-item" href="#">${dep}</a>`;
                depItem.addEventListener("click", () => {
                    selectedDepartment = dep; selectedCommune = "";
                    document.getElementById("commune-select").innerHTML    = "";
                    document.getElementById("departmentDropdown").textContent = dep;
                    document.getElementById("communeDropdown").textContent    = "Default";
                    populateCommuneDropdown(filteredCountryData, country, region, dep);
                    zoomToFilteredArea(geoJsonData, country, region, dep, "");
                    updateMapDisplay();
                });
                departmentDropdown.appendChild(depItem);
            });
        }

        // ── Commune dropdown ──────────────────────────────────────
        function populateCommuneDropdown(filteredCountryData, country, region, department) {
            const communes = [...new Set(geoJsonData.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region && f.properties.ADM2_FR === department).map(f => f.properties.ADM3_FR))].sort((a, b) => a.localeCompare(b));
            const communeDropdown = document.getElementById("commune-select");

            const defaultItem = document.createElement("li");
            defaultItem.innerHTML = `<a class="dropdown-item" href="#">Default</a>`;
            defaultItem.addEventListener("click", () => {
                selectedCommune = "";
                document.getElementById("communeDropdown").textContent = "Default";
                zoomToFilteredArea(geoJsonData, country, region, department, "");
                updateMapDisplay();
            });
            communeDropdown.appendChild(defaultItem);

            communes.forEach(comm => {
                const commItem = document.createElement("li");
                commItem.innerHTML = `<a class="dropdown-item" href="#">${comm}</a>`;
                commItem.addEventListener("click", () => {
                    selectedCommune = comm;
                    document.getElementById("communeDropdown").textContent = comm;
                    zoomToFilteredArea(geoJsonData, country, region, department, comm);
                    updateMapDisplay();
                });
                communeDropdown.appendChild(commItem);
            });
        }

        // ── Reset button (main map) ───────────────────────────────
        document.getElementById("resetButton").addEventListener("click", function () {
            fetch(uemoaBordersFile)
                .then(r => r.json())
                .then(data => { L.geoJSON(data, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(map); })
                .catch(err => console.error('Error loading UEMOA borders:', err));

            map.setView([14.5, -1], defaultZoom);
            loadMapData(geoJsonData, "", "", "", "", selectedEquipment);
            document.querySelector('#map-content h1').textContent = 'Spatial Accessibility to Bank Branches';
            document.getElementById("countryDropdown").textContent    = "Default";
            document.getElementById("communeDropdown").textContent    = "Default";
            document.getElementById("departmentDropdown").textContent = "Default";
            document.getElementById("regionDropdown").textContent     = "Default";
            selectedCountry = ""; selectedCommune = ""; selectedDepartment = ""; selectedRegion = "";
            document.getElementById("num-municipalities").innerHTML = '';
            document.getElementById("total-bran").innerHTML         = '';
            document.getElementById("percent-pop").innerHTML        = '';
            document.getElementById("percent-area").innerHTML       = '';
            if (toggleSwitch) toggleSwitch.checked = false;
        });

        // Load initial map data
        loadMapData(geoJsonData, "", "", "", "", selectedEquipment);

        // Add UEMOA border on load
        L.geoJSON(uemoaData, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(map);

    } catch (error) {
        console.error('Error loading GeoJSON:', error);
        if (document.body.contains(loadingSpinner)) document.body.removeChild(loadingSpinner);
    }

    // ── Info control ──────────────────────────────────────────────
    const info = L.control();
    info.onAdd = function () {
        this.div = L.DomUtil.create("div", "info");
        this.update();
        return this.div;
    };

    // ── toggleCommuneDropdown ─────────────────────────────────────
    function toggleCommuneDropdown(selectedCountry) {
        const communeLabel            = document.querySelector('label[for="commune-select"]');
        const communeDropdownContainer = communeLabel ? communeLabel.nextElementSibling : null;
        const hiddenCommuneCountries  = ["Benin", "Guinea-Bissau"];
        if (communeLabel && communeDropdownContainer) {
            const hidden = hiddenCommuneCountries.includes(selectedCountry);
            communeLabel.style.display             = hidden ? 'none' : 'block';
            communeDropdownContainer.style.display = hidden ? 'none' : 'block';
            if (hidden) document.getElementById('communeDropdown').textContent = 'Default';
        }
    }

    // ── loadMapData ───────────────────────────────────────────────
    function loadMapData(geoJsonData, country, region, department, commune, selectedEquipment) {
        map.eachLayer(layer => { if (layer instanceof L.GeoJSON) map.removeLayer(layer); });
        toggleCommuneDropdown(country);

        const filteredData = geoJsonData.features.filter(f =>
            (!country    || f.properties.ADM0_EN === country) &&
            (!commune    || f.properties.ADM3_FR === commune) &&
            (!department || f.properties.ADM2_FR === department) &&
            (!region     || f.properties.ADM1_FR === region)
        );

        let tooltip = null;
        const geoJsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
            onEachFeature: function (feature, layer) {
                layer.on({
                    mouseover: function (e) {
                        e.target.setStyle({ weight: 1.5, color: "black", fillOpacity: 0.7 });
                        tooltip = L.tooltip({ permanent: false, direction: 'top', className: 'custom-tooltip', opacity: 0.9 })
                            .setContent(e.target.feature.properties.ADM3_FR + ' : ' + (e.target.feature.properties.ISIBF_base || 0).toFixed(2))
                            .setLatLng(e.latlng);
                        tooltip.addTo(map);
                    },
                    mouseout: function (e) {
                        geoJsonLayer.resetStyle(e.target);
                        if (tooltip) { map.removeLayer(tooltip); tooltip = null; }
                    },
                    click: function (e) {
                        e.target.setStyle({ weight: 2, color: "black", fillOpacity: 2 });
                        const p = e.target.feature.properties;
                        const loc = p.ADM3_FR ? `${p.ADM3_FR} - ${p.ADM2_FR}, ${p.ADM1_FR}, ${p.ADM0_EN}` : p.ADM0_EN;
                        document.querySelector('#map-content h1').innerHTML = `<span class="title-main">Spatial Accessibility to Bank Branches</span><br>${loc}`;
                        const cData = geoJsonData.features.filter(f => f.properties.ADM0_EN === p.ADM0_EN);
                        const fData = geoJsonData.features.filter(f => f.properties.ADM0_EN === p.ADM0_EN && f.properties.ADM1_FR === p.ADM1_FR && f.properties.ADM2_FR === p.ADM2_FR && f.properties.ADM3_FR === p.ADM3_FR);
                        updateStats(cData, fData, p.ADM0_EN);
                        document.getElementById("countryDropdown").textContent    = p.ADM0_EN;
                        document.getElementById("regionDropdown").textContent     = p.ADM1_FR;
                        document.getElementById("departmentDropdown").textContent = p.ADM2_FR;
                        document.getElementById("communeDropdown").textContent    = p.ADM3_FR;
                    }
                });
            },
            style: function (feature) {
                const score     = feature.properties[selectedEquipment] || 0;
                const fillColor = getColor(score);
                return { fillColor, weight: 0.3, opacity: 0.3, color: "#abababff", fillOpacity: 0.9, zIndex: 1 };
            }
        }).addTo(map);

        updateLegend();
        updateBorders(country);
    }

    // ── updateBorders ─────────────────────────────────────────────
    function updateBorders(country) {
        if (countryBorders[country]) {
            fetch(countryBorders[country])
                .then(r => r.json())
                .then(data => {
                    currentBorderLayer = L.geoJSON(data, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(map);
                })
                .catch(err => console.error('Error loading country borders:', err));
        }
    }

    // ── updateLegend ──────────────────────────────────────────────
    function updateLegend() {
        if (legend) legend.remove();
        legend = L.control({ position: "bottomright" });
        const grades = [1, 0.5, 0.2, 0.1, 0.01];
        legend.onAdd = function () {
            const div = L.DomUtil.create("div", "legend");
            div.innerHTML += "<strong>Scores of access</strong><br>";
            for (let i = 0; i < grades.length; i++) {
                div.innerHTML += `<i style="background:${getColor(grades[i])}"></i> ${grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "-0"}<br>`;
            }
            return div;
        };
        legend.addTo(map);
    }

    // ── getColor ──────────────────────────────────────────────────
    function getColor(value) {
        return value > 0.5  ? "#67000d" :
               value > 0.2  ? "#d32020" :
               value > 0.1  ? "#fb7050" :
               value > 0.01 ? "#fcbea5" :
                              "#fff5f0";
    }

    // ── municipalities / rgph ─────────────────────────────────────
    const municipalities = {
        "Benin": "Communes", "Burkina Faso": "Communes", "Mali": "Communes", "Niger": "Communes",
        "Ivory Coast": "Sub-Prefectures", "Guinea-Bissau": "Sectors", "Senegal": "Arrondissements",
        "Togo": "Communes", "Ghana": "Districts", "Cameroon": "Arrondissements",
        "Chad": "Provinces", "Nigeria": "Local Government Areas"
    };
    const rgph = {
        "Benin": 2013, "Burkina Faso": 2019, "Mali": 2009, "Niger": 2012,
        "Ivory Coast": 2021, "Guinea-Bissau": 2009, "Senegal": 2023, "Togo": 2022,
        "Ghana": 2021, "Cameroon": 2005, "Chad": 2009, "Nigeria": 2022
    };

    // ── updateStats ───────────────────────────────────────────────
    function updateStats(filteredDataCountry, filteredData, country) {
        const popCountries = ['Nigeria','Cameroon','Ghana','Chad','Benin','Burkina Faso','Ivory Coast','Guinea-Bissau','Mali','Niger','Senegal','Togo'];
        if (!popCountries.includes(country)) {
            document.getElementById("num-municipalities").innerHTML = '';
            document.getElementById("total-bran").innerHTML         = '';
            document.getElementById("percent-pop").innerHTML        = '';
            document.getElementById("percent-area").innerHTML       = '';
            return;
        }
        const municipalityLabel = municipalities[country] || "Municipalities";
        const rgphDate          = rgph[country] || 0;
        const totalCommunes     = filteredData.length;
        const totalBranches     = filteredData.reduce((s, f) => s + (f.properties.Total_bran || 0), 0);
        const totalPopulation   = filteredData.reduce((s, f) => s + (Number(f.properties.Population) || 0), 0);
        const totalArea         = filteredData.reduce((s, f) => s + (f.properties.Area || 0), 0);
        const totalAreaKm2      = totalArea / 1000000;
        const totalCountryPop   = filteredDataCountry.reduce((s, f) => s + (Number(f.properties.Population) || 0), 0);
        const totalCountryArea  = filteredDataCountry.reduce((s, f) => s + (f.properties.Area || 0), 0);
        const totalCountryBran  = filteredDataCountry.reduce((s, f) => s + (f.properties.Total_bran || 0), 0);
        const populationPct     = totalCountryPop  > 0 ? ((totalPopulation / totalCountryPop)  * 100).toFixed(1) : 0;
        const areaPct           = totalCountryArea > 0 ? ((totalArea / totalCountryArea) * 100).toFixed(1) : 0;
        const branchPct         = totalCountryBran > 0 ? ((totalBranches / totalCountryBran) * 100).toFixed(1) : 0;

        if (filteredData.length === 1) {
            const communeScore = (filteredData[0].properties.ISIBF_base || 0).toFixed(2);
            document.getElementById("num-municipalities").innerHTML = `<span>Score: ${communeScore}</span>`;
        } else {
            document.getElementById("num-municipalities").innerHTML = `<span>${totalCommunes}</span>${municipalityLabel}`;
        }
        document.getElementById("total-bran").innerHTML   = `<span>${totalBranches}</span>Bank Branches`;
        document.getElementById("percent-pop").innerHTML  = `<span>${totalPopulation.toLocaleString('fr-FR')}</span>Population (${rgphDate})`;
        document.getElementById("percent-area").innerHTML = `<span>${totalAreaKm2.toLocaleString('fr-FR', { maximumFractionDigits: 0 })}</span>Area (km²)`;
    }

    // ── loadIsochrone ─────────────────────────────────────────────
    function loadIsochrone(geoJsonData, isochroneData, country, region, department, commune, selectedEquipment) {
        changeColorLayer(geoJsonData, country, region, department, commune, selectedEquipment);

        const filteredData = isochroneData.features.filter(f =>
            (!country    || f.properties.ADM0_EN === country) &&
            (!commune    || f.properties.ADM3_FR === commune) &&
            (!department || f.properties.ADM2_FR === department) &&
            (!region     || f.properties.ADM1_FR === region)
        );

        let tooltip = null;
        const geoJsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
            onEachFeature: function (feature, layer) {
                layer.on({
                    mouseover: function (e) { e.target.setStyle({ weight: 1.5, color: "black", fillOpacity: 2 }); },
                    mouseout:  function (e) {
                        geoJsonLayer.resetStyle(e.target);
                        if (tooltip) { map.removeLayer(tooltip); tooltip = null; }
                    },
                    click: function (e) {
                        e.target.setStyle({ weight: 2, color: "black", fillOpacity: 2 });
                        const p = e.target.feature.properties;
                        document.querySelector('#map-content h1').textContent = `Area Covered By At Least One Bank Branch in ${p.ADM3_FR} - ${p.ADM2_FR}, ${p.ADM1_FR}, ${p.ADM0_EN}`;
                        document.getElementById("countryDropdown").textContent    = p.ADM0_EN;
                        document.getElementById("regionDropdown").textContent     = p.ADM1_FR;
                        document.getElementById("departmentDropdown").textContent = p.ADM2_FR;
                        document.getElementById("communeDropdown").textContent    = p.ADM3_FR;
                    }
                });
            },
            style: function (feature) {
                const timeTravel = feature.properties.group_inde || 0;
                return {
                    fillColor: getIsochroneColor(timeTravel),
                    weight: 0.3, opacity: 0.1,
                    color: "#6d6b6ab7",
                    fillOpacity: 3, zIndex: 1000
                };
            }
        }).addTo(map);

        updateLegendIsochrone();
        updateBorders(country);
    }

    function updateLegendIsochrone() {
        if (legend) legend.remove();
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
        if (!timeTravel) return "#6d6b6ab7";
        return timeTravel === 15 ? "#bd0026" :
               timeTravel === 30 ? "#fd8d3c" :
               timeTravel === 45 ? "#fecc5c" :
               timeTravel === 60 ? "#ffffb2" :
                                   "#6d6b6ab7";
    }

    function updatePercentage(filteredIsochroneData, country, filteredData) {
        const popCountries = ['Nigeria','Cameroon','Ghana','Chad','Benin','Burkina Faso','Ivory Coast','Guinea-Bissau','Mali','Niger','Senegal','Togo'];
        if (!popCountries.includes(country)) {
            document.getElementById("num-municipalities").innerHTML = '';
            document.getElementById("total-bran").innerHTML         = '';
            document.getElementById("percent-pop").innerHTML        = '';
            document.getElementById("percent-area").innerHTML       = '';
            return;
        }
        const totalAdminArea = filteredData.reduce((s, f) => s + (f.properties.Area || 0), 0);
        const sum = (g) => filteredIsochroneData.reduce((s, f) => s + ((f.properties.group_inde === g ? f.properties.area_iso : 0) || 0), 0);
        const pct = (v) => ((v / totalAdminArea) * 100).toFixed(1);
        document.getElementById("num-municipalities").innerHTML = `<span>${pct(sum(15))}%</span>within 0-15min`;
        document.getElementById("total-bran").innerHTML         = `<span>${pct(sum(30))}%</span>within 15-30min`;
        document.getElementById("percent-pop").innerHTML        = `<span>${pct(sum(45))}%</span>within 30-45min`;
        document.getElementById("percent-area").innerHTML       = `<span>${pct(sum(60))}%</span>within 45-60min`;
    }

    function changeColorLayer(geoJsonData, country, region, department, commune) {
        map.eachLayer(layer => { if (layer instanceof L.GeoJSON) map.removeLayer(layer); });
        const filteredData = geoJsonData.features.filter(f =>
            (!country    || f.properties.ADM0_EN === country) &&
            (!commune    || f.properties.ADM3_FR === commune) &&
            (!department || f.properties.ADM2_FR === department) &&
            (!region     || f.properties.ADM1_FR === region)
        );
        L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
            style: () => ({ fillColor: "#abababff", weight: 0.3, opacity: 0.3, color: "#abababff", fillOpacity: 0.9, zIndex: 1 })
        }).addTo(map);
    }


    // ═══════════════════════════════════════════════════════════════
    // SECTION 2 – FCA MAP (Floating Catchment Area)
    // ═══════════════════════════════════════════════════════════════

    let mapFCA = null;
    let fcaInitialized = false;

    document.getElementById("map-fca-btn").addEventListener("click", function () {
        showContent("map-fca-content");
        if (!fcaInitialized) {
            initializeFCAMap();
            fcaInitialized = true;
        } else {
            setTimeout(() => { if (mapFCA) mapFCA.invalidateSize(); }, 100);
        }
    });

    async function initializeFCAMap() {
        try {
            let defaultZoomFCA   = 5;
            let smallScreenZoomFCA = 4;
            let currentZoomFCA   = window.innerWidth <= 480 ? smallScreenZoomFCA : defaultZoomFCA;
            mapFCA = L.map("map-fca").setView([14.5, 3.5], currentZoomFCA);

            L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
                attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
            }).addTo(mapFCA);

            L.control.fullscreen({
                position: 'topleft', title: 'Show me the fullscreen !',
                titleCancel: 'Exit fullscreen mode', content: null,
                forceSeparateButton: true, forcePseudoFullscreen: true, fullscreenElement: false
            }).addTo(mapFCA);

            // Loading spinner for FCA
            const fcaSpinner = document.createElement("div");
            fcaSpinner.className = "loading-spinner";
            fcaSpinner.innerHTML = `<div class="spinner"></div><span>Loading FCA Map...</span>`;
            document.body.appendChild(fcaSpinner);

            const FCAFile         = "web_data/communes_all_pop_v2.geojson";
            const uemoaFileFCA    = "web_data/uemoa_borders.geojson";
            const cemacFileFCA    = "web_data/cemac_borders.geojson";
            const ghanaFileFCA    = "web_data/ghana_borders.geojson";
            const nigeriaFileFCA  = "web_data/nigeria_borders.geojson";




            const [fcaResponse, uemoaRes, cemacRes, ghanaRes, nigeriaRes] = await Promise.all([
                fetch(FCAFile),
                fetch(uemoaFileFCA),
                fetch(cemacFileFCA),
                fetch(ghanaFileFCA),
                fetch(nigeriaFileFCA),
            ]);


       

            const geoJsonDataFCA = await fcaResponse.json();
            const uemoaData      = await uemoaRes.json();
            const cemacData      = await cemacRes.json();
            const ghanaData      = await ghanaRes.json();
            const nigeriaData    = await nigeriaRes.json();

            

            if (document.body.contains(fcaSpinner)) document.body.removeChild(fcaSpinner);

            console.log('FCA data loaded successfully');

            setupFCAMapFunctionality(geoJsonDataFCA, uemoaData, cemacData, ghanaData, nigeriaData);

        } catch (error) {
            console.error('Error loading FCA map:', error);
        }
    }



    // ── Info Control for FCA ──────────────────────────────────────
    const infoFCA = L.control();
    infoFCA.onAdd = function () {
        this.div = L.DomUtil.create("div", "info");
        this.update();
        return this.div;
    };

    // ── updateBorders ─────────────────────────────────────────────
    function updateBordersFCA(country) {
        if (countryBorders[country]) {
            fetch(countryBorders[country])
                .then(r => r.json())
                .then(data => {
                    currentBorderLayer = L.geoJSON(data, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
                })
                .catch(err => console.error('Error loading country borders:', err));
        }
    }

    function setupFCAMapFunctionality(geoJsonDataFCA, uemoaData, cemacData, ghanaData, nigeriaData, cameroonData, chadData) {
        let legendFCA = null;
        let selectedEquipmentFCA = "ISIBF_base";
        let selectedCommuneFCA   = "";
        let selectedDepartmentFCA = "";
        let selectedRegionFCA    = "";
        let selectedCountryFCA   = "";

        infoFCA.update = function (props) {
            this.div.innerHTML = props
                ? `<h6>${props.ADM3_FR}</h6><br>Score: ${props.ISIBF_base}`
                : "Hover over";
        };
        infoFCA.addTo(mapFCA);

        const countryCentersFCA = {
            "Benin":        { lat: 9.3,  lng: 2.5,  latSmall: 9.3,  lngSmall: 2.5,   zoom: 7, smallScreenZoom: 6 },
            "Burkina Faso": { lat: 12.4, lng: -1.5, latSmall: 12.4, lngSmall: -1.5,  zoom: 7, smallScreenZoom: 5 },
            "Ivory Coast":  { lat: 7.5,  lng: -5.5, latSmall: 7.5,  lngSmall: -5.5,  zoom: 7, smallScreenZoom: 6 },
            "Guinea-Bissau":{ lat: 11.5, lng:-15.7, latSmall: 11.5, lngSmall:-15.2,  zoom: 8, smallScreenZoom: 7 },
            "Mali":         { lat: 12.6, lng: -8,   latSmall: 14.6, lngSmall: -6,    zoom: 5, smallScreenZoom: 4 },
            "Niger":        { lat: 17.6, lng: 8,    latSmall: 13.6, lngSmall: 8,     zoom: 6, smallScreenZoom: 4 },
            "Senegal":      { lat: 14.5, lng:-14,   latSmall: 14.5, lngSmall:-14.5,  zoom: 7, smallScreenZoom: 6 },
            "Togo":         { lat: 8.2,  lng: 1.3,  latSmall: 8.2,  lngSmall: 0.9,   zoom: 7, smallScreenZoom: 6 },
            "Ghana":        { lat: 7.5,  lng: -0.5, latSmall: 7.5,  lngSmall: -0.5,  zoom: 7, smallScreenZoom: 6 },
            "Cameroon":     { lat: 6.5,  lng: 13,   latSmall: 6.5,  lngSmall: 13,    zoom: 6, smallScreenZoom: 5 },
            "Chad":         { lat: 15.5, lng: 18,   latSmall: 15.5, lngSmall: 18,    zoom: 5, smallScreenZoom: 4 },
            "Nigeria":      { lat: 9.1,  lng: 8.5,  latSmall: 9.1,  lngSmall: 8.5,   zoom: 6, smallScreenZoom: 5 }
        };

        const municipalitiesFCA = {
            "Benin": "Communes", "Burkina Faso": "Communes", "Mali": "Communes", "Niger": "Communes",
            "Ivory Coast": "Sub-Prefectures", "Guinea-Bissau": "Sectors", "Senegal": "Arrondissements",
            "Togo": "Communes", "Ghana": "Districts", "Cameroon": "Arrondissements",
            "Chad": "Provinces", "Nigeria": "Local Government Areas"
        };

        // Initial load
        loadMapDataFCA(geoJsonDataFCA, "", "", "", "", selectedEquipmentFCA);
        updateStatsFCA([], [], "");

        // Add borders
        L.geoJSON(uemoaData,   { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
        L.geoJSON(cemacData,   { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
        L.geoJSON(ghanaData,   { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
        L.geoJSON(nigeriaData, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);

        // Countries list for FCA
        const countriesFCA = [...new Set(geoJsonDataFCA.features.map(f => f.properties.ADM0_EN))].sort((a, b) => a.localeCompare(b));
        const countryDropdownFCA = document.getElementById("country-select-fca");
        document.getElementById("commune-select-fca").innerHTML    = "";
        document.getElementById("department-select-fca").innerHTML = "";
        document.getElementById("region-select-fca").innerHTML     = "";

        countriesFCA.forEach(coun => {
            updateBordersFCA(coun);
            const filteredCountryData = geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === coun);
            const listItem = document.createElement("li");
            listItem.innerHTML = `<a class="dropdown-item" href="#" data-value="${coun}">${coun}</a>`;
            listItem.addEventListener("click", () => {
                selectedCountryFCA    = coun;
                selectedCommuneFCA    = "";
                selectedDepartmentFCA = "";
                selectedRegionFCA     = "";

                document.getElementById("region-select-fca").innerHTML    = "";
                document.getElementById("department-select-fca").innerHTML = "";
                document.getElementById("commune-select-fca").innerHTML    = "";

                document.getElementById("countryDropdownFCA").textContent    = coun;
                document.getElementById("regionDropdownFCA").textContent     = "";
                document.getElementById("departmentDropdownFCA").textContent = "";
                document.getElementById("communeDropdownFCA").textContent    = "";

                populateRegionDropdownFCA(filteredCountryData, coun);

                if (countryCentersFCA[coun]) {
                    const { lat, lng, latSmall, lngSmall, zoom, smallScreenZoom } = countryCentersFCA[coun];
                    mapFCA.setView(window.innerWidth <= 480 ? [latSmall, lngSmall] : [lat, lng], window.innerWidth <= 480 ? smallScreenZoom : zoom);
                }

                document.getElementById("num-municipalities-fca").innerHTML = '';
                document.getElementById("total-bran-fca").innerHTML         = '';
                document.getElementById("percent-pop-fca").innerHTML        = '';
                document.getElementById("percent-area-fca").innerHTML       = '';

                loadMapDataFCA(geoJsonDataFCA, coun, "", "", "", selectedEquipmentFCA);
                updateStatsFCA(filteredCountryData, filteredCountryData, coun);
            });
            countryDropdownFCA.appendChild(listItem);
        });

        // ── FCA zoom helper ───────────────────────────────────────
        function zoomToFilteredAreaFCA(country, region, department, commune) {
            const filteredFeatures = geoJsonDataFCA.features.filter(f =>
                (!country    || f.properties.ADM0_EN === country) &&
                (!region     || f.properties.ADM1_FR === region) &&
                (!department || f.properties.ADM2_FR === department) &&
                (!commune    || f.properties.ADM3_FR === commune)
            );
            if (!filteredFeatures.length) return;
            const bounds = L.geoJSON({ type: "FeatureCollection", features: filteredFeatures }).getBounds();
            if (bounds.isValid()) {
                mapFCA.fitBounds(bounds, {
                    padding: [20, 20],
                    maxZoom: commune ? 12 : department ? 10 : region ? 8 : 7
                });
            }
        }

        // ── FCA Region dropdown ───────────────────────────────────
        function populateRegionDropdownFCA(filteredCountryData, country) {
            const regions = [...new Set(geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === country).map(f => f.properties.ADM1_FR))].sort((a, b) => a.localeCompare(b));
            const regionDropdown = document.getElementById("region-select-fca");

            regions.forEach(reg => {
                const filteredRegionData = geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === reg);
                const regionItem = document.createElement("li");
                regionItem.innerHTML = `<a class="dropdown-item" href="#">${reg}</a>`;
                regionItem.addEventListener("click", () => {
                    selectedRegionFCA = reg;
                    populateDepartmentDropdownFCA(filteredCountryData, country, reg);
                    document.getElementById("regionDropdownFCA").textContent     = reg;
                    document.getElementById("departmentDropdownFCA").textContent = "";
                    document.getElementById("communeDropdownFCA").textContent    = "";
                    if (countryCentersFCA[country]) {
                        const { lat, lng, latSmall, lngSmall, zoom, smallScreenZoom } = countryCentersFCA[country];
                        mapFCA.setView(window.innerWidth <= 480 ? [latSmall, lngSmall] : [lat, lng], window.innerWidth <= 480 ? smallScreenZoom : zoom);
                    }
                    zoomToFilteredAreaFCA(country, reg, "", "");
                    updateStatsFCA(filteredCountryData, filteredRegionData, country);
                    loadMapDataFCA(geoJsonDataFCA, country, reg, "", "", selectedEquipmentFCA);
                });
                regionDropdown.appendChild(regionItem);
            });
        }

        // ── FCA Department dropdown ───────────────────────────────
        function populateDepartmentDropdownFCA(filteredCountryData, country, region) {
            const departments = [...new Set(geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region).map(f => f.properties.ADM2_FR))].sort((a, b) => a.localeCompare(b));
            const departmentDropdown = document.getElementById("department-select-fca");
            departmentDropdown.innerHTML = "";

            departments.forEach(dep => {
                const filteredDepartmentData = geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region && f.properties.ADM2_FR === dep);
                const depItem = document.createElement("li");
                depItem.innerHTML = `<a class="dropdown-item" href="#">${dep}</a>`;
                depItem.addEventListener("click", () => {
                    selectedDepartmentFCA = dep;
                    populateCommuneDropdownFCA(filteredCountryData, country, region, dep);
                    document.getElementById("departmentDropdownFCA").textContent = dep;
                    document.getElementById("regionDropdownFCA").textContent     = region;
                    document.getElementById("communeDropdownFCA").textContent    = "";
                    zoomToFilteredAreaFCA(country, region, dep, "");
                    updateStatsFCA(filteredCountryData, filteredDepartmentData, country);
                    loadMapDataFCA(geoJsonDataFCA, country, region, dep, "", selectedEquipmentFCA);
                });
                departmentDropdown.appendChild(depItem);
            });
        }

        // ── FCA Commune dropdown ──────────────────────────────────
        function populateCommuneDropdownFCA(filteredCountryData, country, region, department) {
            const communes = [...new Set(geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region && f.properties.ADM2_FR === department).map(f => f.properties.ADM3_FR))].sort((a, b) => a.localeCompare(b));
            const communeDropdown = document.getElementById("commune-select-fca");
            communeDropdown.innerHTML = "";

            communes.forEach(comm => {
                const filteredCommuneData = geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === country && f.properties.ADM1_FR === region && f.properties.ADM2_FR === department && f.properties.ADM3_FR === comm);
                const commItem = document.createElement("li");
                commItem.innerHTML = `<a class="dropdown-item" href="#">${comm}</a>`;
                commItem.addEventListener("click", () => {
                    selectedCommuneFCA = comm;
                    document.getElementById("communeDropdownFCA").textContent    = comm;
                    document.getElementById("departmentDropdownFCA").textContent = department;
                    document.getElementById("regionDropdownFCA").textContent     = region;
                    updateStatsFCA(filteredCountryData, filteredCommuneData, country);
                    zoomToFilteredAreaFCA(country, region, department, comm);
                    loadMapDataFCA(geoJsonDataFCA, country, region, department, comm, selectedEquipmentFCA);
                });
                communeDropdown.appendChild(commItem);
            });
        }

        // ── Reset button (FCA) ────────────────────────────────────
        document.getElementById("resetButtonFCA").addEventListener("click", function () {
            selectedCountryFCA    = ""; selectedCommuneFCA = "";
            selectedDepartmentFCA = ""; selectedRegionFCA  = "";
            document.getElementById("countryDropdownFCA").textContent    = "Default";
            document.getElementById("communeDropdownFCA").textContent    = "Default";
            document.getElementById("departmentDropdownFCA").textContent = "Default";
            document.getElementById("regionDropdownFCA").textContent     = "Default";
            mapFCA.setView([14.5, 3.5], 5);
            document.getElementById("num-municipalities-fca").innerHTML = '';
            document.getElementById("total-bran-fca").innerHTML         = '';
            document.getElementById("percent-pop-fca").innerHTML        = '';
            document.getElementById("percent-area-fca").innerHTML       = '';
            loadMapDataFCA(geoJsonDataFCA, "", "", "", "", selectedEquipmentFCA);
            L.geoJSON(uemoaData,   { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
            L.geoJSON(cemacData,   { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
            L.geoJSON(ghanaData,   { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
            L.geoJSON(nigeriaData, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(mapFCA);
        });

        // ── loadMapDataFCA ────────────────────────────────────────
        function loadMapDataFCA(geoJsonDataFCA, country, region, department, commune, selectedEquipment) {
            mapFCA.eachLayer(layer => { if (layer instanceof L.GeoJSON) mapFCA.removeLayer(layer); });

            const filteredData = geoJsonDataFCA.features.filter(f =>
                (!country    || f.properties.ADM0_EN === country) &&
                (!commune    || f.properties.ADM3_FR === commune) &&
                (!department || f.properties.ADM2_FR === department) &&
                (!region     || f.properties.ADM1_FR === region)
            );

            let tooltipFCA = null;
            const geoJsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredData }, {
                onEachFeature: function (feature, layer) {
                    layer.on({
                        mouseover: function (e) {
                            e.target.setStyle({ weight: 1.5, color: "black", fillOpacity: 0.7 });
                            const score = (e.target.feature.properties.ISIBF_base || 0).toFixed(2);
                            tooltipFCA = L.tooltip({ permanent: false, direction: 'top', className: 'custom-tooltip', opacity: 0.9 })
                                .setContent(e.target.feature.properties.ADM3_FR + ' : ' + score)
                                .setLatLng(e.latlng);
                            tooltipFCA.addTo(mapFCA);
                        },
                        mouseout: function (e) {
                            geoJsonLayer.resetStyle(e.target);
                            if (tooltipFCA) { mapFCA.removeLayer(tooltipFCA); tooltipFCA = null; }
                        },
                        click: function (e) {
                            e.target.setStyle({ weight: 2, color: "black", fillOpacity: 2 });
                            const p = e.target.feature.properties;
                            const loc = p.ADM3_FR ? `${p.ADM3_FR} - ${p.ADM2_FR}, ${p.ADM1_FR}, ${p.ADM0_EN}` : p.ADM0_EN;
                            document.querySelector('#map-fca-content h1').innerHTML = `<span class="title-main">Spatial Accessibility to Bank Branches (FCA)</span><br>${loc}`;
                            const cData = geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === p.ADM0_EN);
                            const fData = geoJsonDataFCA.features.filter(f => f.properties.ADM0_EN === p.ADM0_EN && f.properties.ADM1_FR === p.ADM1_FR && f.properties.ADM2_FR === p.ADM2_FR && f.properties.ADM3_FR === p.ADM3_FR);
                            updateStatsFCA(cData, fData, p.ADM0_EN);
                            document.getElementById("countryDropdownFCA").textContent    = p.ADM0_EN;
                            document.getElementById("regionDropdownFCA").textContent     = p.ADM1_FR;
                            document.getElementById("departmentDropdownFCA").textContent = p.ADM2_FR;
                            document.getElementById("communeDropdownFCA").textContent    = p.ADM3_FR;
                        }
                    });
                },
                style: function (feature) {
                    const score     = feature.properties[selectedEquipment] || 0;
                    const country   = feature.properties.ADM0_EN;
                    const fillColor = getColorFCA(score, country);
                    return { fillColor, weight: 0.3, opacity: 0.3, color: "#abababff", fillOpacity: 0.9, zIndex: 1 };
                }
            }).addTo(mapFCA);

            updateLegendFCA(country);
            updateBordersFCA(country);
        }

        // ── FCA Legend ────────────────────────────────────────────
        function updateLegendFCA(country) {
            if (legendFCA) legendFCA.remove();

            const uemoaCountries = ['Benin','Burkina Faso','Ivory Coast','Guinea-Bissau','Mali','Niger','Senegal','Togo'];
            const ghNgCountries  = ['Ghana','Nigeria'];
            const cemacCountries = ['Cameroon','Chad'];

            if ([...uemoaCountries, ...ghNgCountries, ...cemacCountries].includes(country)) {
                legendFCA = L.control({ position: "bottomright" });
                const grades = uemoaCountries.includes(country) || cemacCountries.includes(country)
                    ? [1, 0.5, 0.1, 0.01, 0.001]
                    : [1, 0.5, 0.2, 0.1, 0.01];

                legendFCA.onAdd = function () {
                    const div = L.DomUtil.create("div", "legend");
                    div.innerHTML += "<strong>Bank Branch Score Access</strong><br>";
                    for (let i = 0; i < grades.length; i++) {
                        div.innerHTML += `<i style="background:${getColorFCA(grades[i], country)}"></i> ${grades[i]}${grades[i + 1] ? `–${grades[i + 1]}` : "-0"}<br>`;
                    }
                    return div;
                };
                legendFCA.addTo(mapFCA);
            }
        }

        // ── getColorFCA ───────────────────────────────────────────
        function getColorFCA(value, country) {
            const uemoa = ['Benin','Burkina Faso','Ivory Coast','Guinea-Bissau','Mali','Niger','Senegal','Togo'];
            const ghNg  = ['Ghana','Nigeria'];
            const cemac = ['Cameroon','Chad'];
            if (uemoa.includes(country)) {
                return value > 0.5   ? "#08519c" :
                       value > 0.1   ? "#3182bd" :
                       value > 0.01  ? "#6baed6" :
                       value > 0.001 ? "#bdd7e7" :
                                       "#eff3ff";
            } else if (ghNg.includes(country)) {
                return value > 0.5  ? "#880e4f" :
                       value > 0.2  ? "#c2185b" :
                       value > 0.1  ? "#d81b60" :
                       value > 0.01 ? "#f768a1" :
                                      "#ffeff3";
            } else if (cemac.includes(country)) {
                return value > 0.5   ? "#00441b" :
                       value > 0.1   ? "#006d2c" :
                       value > 0.01  ? "#31a354" :
                       value > 0.001 ? "#a1d99b" :
                                       "#f3ffef";
            }
            return "#ffffff";
        }

        // ── updateStatsFCA ────────────────────────────────────────
        function updateStatsFCA(filteredDataCountry, filteredData, country) {
            const popCountries = ['Nigeria','Cameroon','Ghana','Chad','Benin','Burkina Faso','Ivory Coast','Guinea-Bissau','Mali','Niger','Senegal','Togo'];
            if (!popCountries.includes(country)) {
                document.getElementById("num-municipalities-fca").innerHTML = '';
                document.getElementById("total-bran-fca").innerHTML         = '';
                document.getElementById("percent-pop-fca").innerHTML        = '';
                document.getElementById("percent-area-fca").innerHTML       = '';
                return;
            }
            const municipalityLabel  = municipalitiesFCA[country] || "Municipalities";
            const totalCommunes      = filteredData.length;
            const totalBranches      = filteredData.reduce((s, f) => s + (f.properties.Total_bran || 0), 0);
            const totalPopulation    = filteredData.reduce((s, f) => s + (Number(f.properties.Population) || 0), 0);
            const totalArea          = filteredData.reduce((s, f) => s + (f.properties.Area || 0), 0);
            const totalCountryPop    = filteredDataCountry.reduce((s, f) => s + (Number(f.properties.Population) || 0), 0);
            const totalCountryArea   = filteredDataCountry.reduce((s, f) => s + (f.properties.Area || 0), 0);
            const totalCountryBran   = filteredDataCountry.reduce((s, f) => s + (f.properties.Total_bran || 0), 0);
            const populationPct      = totalCountryPop  > 0 ? ((totalPopulation / totalCountryPop)  * 100).toFixed(1) : 0;
            const areaPct            = totalCountryArea > 0 ? ((totalArea / totalCountryArea) * 100).toFixed(1) : 0;
            const branchPct          = totalCountryBran > 0 ? ((totalBranches / totalCountryBran) * 100).toFixed(1) : 0;

            document.getElementById("num-municipalities-fca").innerHTML = `<span>${totalCommunes}</span>${municipalityLabel}`;
            document.getElementById("total-bran-fca").innerHTML         = `<span>${branchPct}%</span>Bank Branches`;
            document.getElementById("percent-pop-fca").innerHTML        = `<span>${populationPct}%</span>Population`;
            document.getElementById("percent-area-fca").innerHTML       = `<span>${areaPct}%</span>Area`;
        }
    }


    // ═══════════════════════════════════════════════════════════════
    // SECTION 3 – NAVIGATION (shared showContent)
    // ═══════════════════════════════════════════════════════════════

    function showContent(contentId) {
        document.getElementById("map-content").style.display     = "none";
        document.getElementById("map-fca-content").style.display = "none";
        document.getElementById("conclusion-content").style.display = "none";
        document.getElementById(contentId).style.display = "flex";

        // Show the correct sidebar filters panel
        document.getElementById("map-filters").style.display = (contentId === "map-content")     ? "block" : "none";
        document.getElementById("fca-filters").style.display = (contentId === "map-fca-content") ? "block" : "none";

        // Invalidate map size when switching to a map view
        if (contentId === "map-content") {
            setTimeout(() => { map.invalidateSize(); }, 100);
        }
        if (contentId === "map-fca-content" && mapFCA) {
            setTimeout(() => { mapFCA.invalidateSize(); }, 100);
        }
    }

    document.getElementById("map-btn").addEventListener("click", function () {
        showContent("map-content");
        if (geoJsonData) {
            loadMapData(geoJsonData, "", "", "", "", "ISIBF_base");
            fetch(uemoaBordersFile)
                .then(r => r.json())
                .then(data => { L.geoJSON(data, { style: () => ({ color: "#000", weight: 1, fillOpacity: 0, zIndex: 10 }) }).addTo(map); })
                .catch(err => console.error('Error loading UEMOA borders:', err));
        }
    });

    document.getElementById("conclusion-btn").addEventListener("click", function () {
        showContent("conclusion-content");
    });
});