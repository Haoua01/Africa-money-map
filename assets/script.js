document.addEventListener("DOMContentLoaded", async function () {
    const map = L.map("map").setView([14.5, 3.5], 5);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
    }).addTo(map);

    const geoJsonFile = "http://localhost:3000/data/communes2.geojson"; // Replace with the path to your GeoJSON file

    // Fetch GeoJSON data
    fetch(geoJsonFile)
        .then(response => response.json())
        .then(geoJsonData => {
            let selectedEquipment = "isibf_base";
            let selectedCommune = "";
            let selectedDepartment = "";
            let selectedRegion = "";

            const equipmentDropdown = document.getElementById("equipment-select");

            equipmentDropdown.querySelectorAll(".dropdown-item").forEach(item => {
                item.addEventListener("click", function () {
                    selectedEquipment = this.getAttribute("data-value");
                    document.getElementById("equipmentDropdown").textContent = this.textContent;
                    loadMapData(geoJsonData, selectedCommune, selectedDepartment, selectedRegion, selectedEquipment);
                });
            });

            // Extract unique communes, departments, and regions from the GeoJSON data
            const communes = [...new Set(geoJsonData.features.map(f => f.properties.adm3_fr))];
            const departments = [...new Set(geoJsonData.features.map(f => f.properties.adm2_fr))];
            const regions = [...new Set(geoJsonData.features.map(f => f.properties.adm1_fr))];

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
                    selectedDepartment = "";
                    selectedRegion = "";
                    loadMapData(geoJsonData, comm, "", "", selectedEquipment);
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
                    selectedRegion = "";
                    loadMapData(geoJsonData, "", dep, "", selectedEquipment);
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
                    selectedCommune = "";
                    selectedDepartment = "";
                    loadMapData(geoJsonData, "", "", reg, selectedEquipment);
                });
                regionDropdown.appendChild(listItem);
            });

            // Reset button event
            document.getElementById("resetButton").addEventListener("click", function() {
                loadMapData(geoJsonData, "", "", "", selectedEquipment);
                document.getElementById("communeDropdown").textContent = "Default";
                document.getElementById("departmentDropdown").textContent = "Default";
                document.getElementById("regionDropdown").textContent = "Default";
                selectedCommune = "";
                selectedDepartment = "";
                selectedRegion = "";
            });

            // Initial load
            loadMapData(geoJsonData, "", "", "", selectedEquipment);
        })
        .catch(error => console.error('Error loading GeoJSON:', error));

    // Info Control
    const info = L.control();
    info.onAdd = function () {
        this.div = L.DomUtil.create("div", "info");
        this.update();
        return this.div;
    };
    info.update = function (props) {
        this.div.innerHTML = props
            ? `<h6>${props.name}</h6><br>Score of access to bank branches: ${props.selectedEquipment}m`
            : "Hover over";
    };
    info.addTo(map);

    function loadMapData(geoJsonData, commune, department, region, selectedEquipment) {
        map.eachLayer(layer => {
            if (layer instanceof L.GeoJSON) {
                map.removeLayer(layer);
            }
        });

        // Filter GeoJSON data based on the selected commune, department, or region
        const filteredData = geoJsonData.features.filter(feature => {
            return (!commune || feature.properties.adm3_fr === commune) &&
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
                return {
                    fillColor: getColor(score),
                    weight: 0.5,
                    opacity: 0.4,
                    color: "lightgrey",
                    fillOpacity: 0.9
                };
            }
        }).addTo(map);
    }

    function getColor(value) {
        return value > 0.5 ? "#eff3ff" :
               value > 0.1 ? "#bdd7e7" :
               value > 0.01 ? "#6baed6" :
               value > 0.001 ? "#3182bd" :
               "#08519c";
    }

    document.getElementById("map-btn").addEventListener("click", function() {
        showContent("map-content");
    });

    function showContent(contentId) {
        document.getElementById("map-content").style.display = "none";
        document.getElementById(contentId).style.display = "flex";
    }
});
