document.addEventListener("DOMContentLoaded", async function () {
    const map = L.map("map").setView([14.5, 3.5], 5);
    
    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: "&copy; OpenStreetMap contributors &copy; CartoDB",
    }).addTo(map);

    const sqlPromise = initSqlJs({ locateFile: file => `libs/sql-wasm.wasm` });
    const dbPromise = fetch("http://localhost:3000/data/communes_all.sqlite")
        .then(res => res.arrayBuffer())
        .then(buf => sqlPromise.then(SQL => new SQL.Database(new Uint8Array(buf))));



    dbPromise.then(db => {

        let selectedEquipment = "ISIBF_base";
        let selectedCommune = "";
        let selectedDepartment = "";
        let selectedRegion = "";

        const equipmentDropdown = document.getElementById("equipment-select");

        equipmentDropdown.querySelectorAll(".dropdown-item").forEach(item => {
            item.addEventListener("click", function () {
                selectedEquipment = this.getAttribute("data-value");
                document.getElementById("equipmentDropdown").textContent = this.textContent;
                loadMapData(db, selectedCommune, selectedDepartment, selectedRegion, selectedEquipment);
            });
        });

        const communes = db.exec("SELECT DISTINCT ADM3_FR FROM cemac_scores_communes_cameroun ORDER BY ADM0_FR ASC;")[0].values;
        console.log("Communes:", communes); 

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
                loadMapData(db, comm, "", "", selectedEquipment);
            });
            communeDropdown.appendChild(listItem);
        }
        );

        const departments = db.exec("SELECT DISTINCT ADM2_FR FROM cemac_scores_communes_cameroun ORDER BY ADM0_FR ASC;")[0].values;
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
                loadMapData(db, "", dep, "", selectedEquipment);
            });
            departmentDropdown.appendChild(listItem);
        });
    
        // Populate region dropdown
        const regions = db.exec("SELECT DISTINCT ADM1_FR FROM cemac_scores_communes_cameroun GROUP BY ADM0_FR;")[0].values;
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
                loadMapData(db, "", "", reg, selectedEquipment);
            });
            regionDropdown.appendChild(listItem);
        });


        document.getElementById("resetButton").addEventListener("click", function() {
            loadMapData(db, "", "", "", selectedEquipment);
            document.getElementById("communeDropdown").textContent = "Default";
            document.getElementById("departmentDropdown").textContent = "Default";
            document.getElementById("regionDropdown").textContent =  "Default";
            selectedCommune = "";
            selectedDepartment = "";
            selectedRegion = "";
        });
        

        loadMapData(db, "", "", "", selectedEquipment);
    });



    // Info Control
    const info = L.control();
    info.onAdd = function () {
        this.div = L.DomUtil.create("div", "info");
        this.update();
        return this.div;
    };
    info.update = function (props) {
        this.div.innerHTML = props
            ? `<h6>${props.name}</h6>
            <br>Score of access to bank branches: ${props.selectedEquipment}m`
            : "Hover over";
    };
    info.addTo(map);


    function loadMapData(db, commune, department, region, selectedEquipment) {
        map.eachLayer(layer => {
            if (layer instanceof L.GeoJSON) {
                map.removeLayer(layer);
            }
        });

        let query = "SELECT * FROM fusionn WHERE 1=1";
        if (commune) query += ` AND ADM3_FR = '${commune}'`;
        if (department) query += ` AND ADM2_FR = '${department}'`;
        if (region) query += ` AND ADM1_FR = '${region}'`;

        const results = db.exec(query)[0]?.values || [];

        const equipmentColumnIndexes = {
            "ISIBF_base": 8,
        };
    
        // Get the correct column index based on selectedEquipment
        const equipmentIndex = equipmentColumnIndexes[selectedEquipment];
    

        const geoJsonData = {
            type: "FeatureCollection",
            features: results.map(row => {
                const score = row[equipmentIndex] || 0;

                return {
                    type: "Feature",
                    properties: {name: row[2], selectedEquipment: score},
                    geometry: JSON.parse(row[1])
                };
            })
        };



        const geoJsonLayer = L.geoJSON(geoJsonData, {
            // layer.bindTooltip(`<strong>${feature.properties.name}</strong>: ${feature.properties.selectedEquipment}m`);

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
                    // click: function (e) {
                    //     map.fitBounds(e.target.getBounds());
                    // }
                });
            },
            style: function (feature) {
                return {
                    fillColor: getColor(feature.properties.selectedEquipment),
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














