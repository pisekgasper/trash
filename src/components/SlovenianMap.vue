<template>
  <div class="filter-container">
    <div class="radio-group">
      <input
        type="radio"
        id="Import"
        value="import"
        v-model="radioModel"
        @change="updateMap"
      /><label for="Import">Uvoz</label
      ><input
        type="radio"
        id="Export"
        value="export"
        v-model="radioModel"
        @change="updateMap"
      /><label for="Export">Izvoz</label>
    </div>
    <span class="label">Leto</span>
    <select name="year" v-model="year" @change="updateMapYear">
      <option value="2021">2021</option>
      <option value="2020">2020</option>
      <option value="2019">2019</option>
      <option value="2018">2018</option>
      <option value="2017">2017</option>
    </select>
  </div>

  <svg id="map-svg"></svg>
  <div id="Overlay" v-if="showGraph" @click="hideGraph"></div>
  <div id="GraphBox" v-if="showGraph">
    <p class="heading">
      Količina {{ radioModel == "import" ? "uvoza" : "izvoza" }} po mesecih -
      {{ regionClickedName }}
    </p>
    <column-chart
      ytitle="Teža v kt (kilotona)"
      :suffix="' kilo ton'"
      :colors="[borderFill]"
      :data="radioModel == 'import' ? chartDataReceiver : chartDataSender"
    ></column-chart>
  </div>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson";
import geoJsonOB from "../assets/geojson/OB_topo.json";
import query from "../helpers/query";
// import anime from "animejs/lib/anime.es.js";
// import promiseAnime from "../helpers/animewaiter";

export default {
  data() {
    return {
      theme: "dark",
      svg: null,
      regions: null,
      g: null,
      path: null,
      zoom: null,
      width: null,
      height: null,
      mainFill: null,
      borderFill: null,
      regionClicked: null,
      regionClickedName: null,
      heatMap: true,
      year: "2021",
      radioModel: "import",
      methodEqual: false,
      municipalityDataExport: null,
      municipalityDataImport: null,
      colorsDark: [
        "#e4f1e1",
        "#b4d9cc",
        "#89c0b6",
        "#63a6a0",
        "#448c8a",
        "#287274",
        "#0d585f",
      ],
      colorsLight: [
        "#f3e0f7",
        "#e4c7f1",
        "#d1afe8",
        "#b998dd",
        "#9f82ce",
        "#826dba",
        "#63589f",
      ],
      showGraph: false,
      chartDataSender: null,
      chartDataReceiver: null,
      senderData: null,
      receiverData: null,
      finishedLoading: false,
    };
  },
  mounted() {
    document.getElementsByTagName("html")[0].classList.add("loaded");
    if (localStorage.municipalityDataExport) {
      this.municipalityDataExport = JSON.parse(
        localStorage.municipalityDataExport
      );
    }
    if (localStorage.municipalityDataImport) {
      this.municipalityDataImport = JSON.parse(
        localStorage.municipalityDataImport
      );
    }
    if (localStorage.senderData) {
      this.senderData = JSON.parse(localStorage.senderData);
    }
    if (localStorage.receiverData) {
      this.receiverData = JSON.parse(localStorage.receiverData);
    }
    this.$nextTick().then(() => {
      document
        .getElementById("switch")
        .getElementsByTagName("input")[0]
        .addEventListener("click", () => {
          setTimeout(() => {
            this.updateTheme();
            this.borderFill = getComputedStyle(
              document.documentElement
            ).getPropertyValue("--accent");
            this.reset();
            this.resetColors();
            this.generateHeatMap();
          }, 100);
        });
      this.draw();
      this.generateHeatMap();
    });
  },
  watch: {
    municipalityDataExport(newData) {
      localStorage.municipalityDataExport = JSON.stringify(newData);
    },
    municipalityDataImport(newData) {
      localStorage.municipalityDataImport = JSON.stringify(newData);
    },
    receiverData(newData) {
      localStorage.receiverData = JSON.stringify(newData);
    },
    senderData(newData) {
      localStorage.senderData = JSON.stringify(newData);
    },
  },
  methods: {
    updateTheme() {
      this.theme = document.documentElement.getAttribute("data-theme");
    },
    generateHeatMap() {
      this.finishedLoading = false;
      let sql =
        this.radioModel == "import"
          ? `SELECT e.obcina_prejem AS obcina, COALESCE(SUM(e.kol_kg), 0) AS kg FROM evl e WHERE DATE_PART('year', e.dat_oddaje) = '${this.year}' AND e.dat_prejem_zav IS NOT NULL GROUP BY e.obcina_prejem ORDER BY kg DESC;`
          : `SELECT e.obcina_oddaja AS obcina, COALESCE(SUM(e.kol_kg), 0) AS kg FROM evl e WHERE DATE_PART('year', e.dat_oddaje) = '${this.year}' AND e.dat_prejem_zav IS NOT NULL GROUP BY e.obcina_oddaja ORDER BY kg DESC;`;

      let deezNutz = this;

      if (this.radioModel == "import") {
        if (localStorage.municipalityDataImport) {
          this.municipalityDataImport = JSON.parse(
            localStorage.municipalityDataImport
          );
          let filteredd = this.municipalityDataImport.filter(
            (x) => parseFloat(x.kg) > 0 && x.obcina !== null
          );
          let filtered = filteredd.map(function (obj) {
            return { obcina: obj.obcina, kg: parseFloat(Math.log(obj.kg)) };
          });

          if (filtered.length === 0) {
            deezNutz.heatMap = false;
            return;
          }

          deezNutz.heatMap = true;

          d3.select(`#map-svg .regions`)
            .selectAll("path")
            .attr("fill", "white");

          if (deezNutz.methodEqual) {
            // method of equal distribution across bins
            let i = 0;
            let perBin = filtered.length / deezNutz.colorsDark.length;
            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? deezNutz.colorsLight[Math.floor(i / perBin)]
                  : deezNutz.colorsDark[Math.floor(i / perBin)]
              );
              i++;
            });
          } else {
            // method of non equal distribution
            let n = deezNutz.colorsDark.length;
            let max = parseFloat(filtered[0].kg);
            let min = parseFloat(filtered[filtered.length - 1].kg);
            let nBins = (max - min + 1) / n;
            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? deezNutz.colorsLight[Math.floor((element.kg - min) / nBins)]
                  : deezNutz.colorsDark[Math.floor((element.kg - min) / nBins)]
              );
            });
          }
          this.finishedLoading = true;
        } else {
          query(sql).then(function (response) {
            if (response === "Are you dumb?") {
              deezNutz.heatMap = false;
              console.log("You are dumb, sorry.");
            } else {
              deezNutz.municipalityDataImport = response;

              let filteredd = response.filter(
                (x) => parseFloat(x.kg) > 0 && x.obcina !== null
              );
              let filtered = filteredd.map(function (obj) {
                return { obcina: obj.obcina, kg: parseFloat(Math.log(obj.kg)) };
              });
              if (filtered.length === 0) {
                deezNutz.heatMap = false;
                return;
              }

              deezNutz.heatMap = true;

              d3.select(`#map-svg .regions`)
                .selectAll("path")
                .attr("fill", "white");

              if (deezNutz.methodEqual) {
                // method of equal distribution across bins
                let i = 0;
                let perBin = filtered.length / deezNutz.colorsDark.length;
                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? deezNutz.colorsLight[Math.floor(i / perBin)]
                      : deezNutz.colorsDark[Math.floor(i / perBin)]
                  );
                  i++;
                });
              } else {
                // method of non equal distribution
                let n = deezNutz.colorsDark.length;
                let max = parseFloat(filtered[0].kg);
                let min = parseFloat(filtered[filtered.length - 1].kg);
                let nBins = (max - min + 1) / n;

                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? deezNutz.colorsLight[
                          Math.floor((element.kg - min) / nBins)
                        ]
                      : deezNutz.colorsDark[
                          Math.floor((element.kg - min) / nBins)
                        ]
                  );
                });
              }
            }
            deezNutz.finishedLoading = true;
          });
        }
      } else {
        if (localStorage.municipalityDataExport) {
          this.municipalityDataExport = JSON.parse(
            localStorage.municipalityDataExport
          );
          let filteredd = this.municipalityDataExport.filter(
            (x) => parseFloat(x.kg) > 0 && x.obcina !== null
          );
          let filtered = filteredd.map(function (obj) {
            return { obcina: obj.obcina, kg: parseFloat(Math.log(obj.kg)) };
          });
          if (filtered.length === 0) {
            deezNutz.heatMap = false;
            return;
          }

          deezNutz.heatMap = true;

          d3.select(`#map-svg .regions`)
            .selectAll("path")
            .attr("fill", "white");

          if (deezNutz.methodEqual) {
            // method of equal distribution across bins
            let i = 0;
            let perBin = filtered.length / deezNutz.colorsDark.length;
            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? deezNutz.colorsLight[Math.floor(i / perBin)]
                  : deezNutz.colorsDark[Math.floor(i / perBin)]
              );
              i++;
            });
          } else {
            // method of non equal distribution
            let n = deezNutz.colorsDark.length;
            let max = parseFloat(filtered[0].kg);
            let min = parseFloat(filtered[filtered.length - 1].kg);
            let nBins = (max - min + 1) / n;

            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? deezNutz.colorsLight[Math.floor((element.kg - min) / nBins)]
                  : deezNutz.colorsDark[Math.floor((element.kg - min) / nBins)]
              );
            });
          }
          this.finishedLoading = true;
        } else {
          query(sql).then(function (response) {
            if (response === "Are you dumb?") {
              deezNutz.heatMap = false;
              console.log("You are dumb, sorry.");
            } else {
              deezNutz.municipalityDataExport = response;

              let filteredd = response.filter(
                (x) => parseFloat(x.kg) > 0 && x.obcina !== null
              );
              let filtered = filteredd.map(function (obj) {
                return { obcina: obj.obcina, kg: parseFloat(Math.log(obj.kg)) };
              });
              if (filtered.length === 0) {
                deezNutz.heatMap = false;
                return;
              }

              deezNutz.heatMap = true;

              d3.select(`#map-svg .regions`)
                .selectAll("path")
                .attr("fill", "white");

              if (deezNutz.methodEqual) {
                // method of equal distribution across bins
                let i = 0;
                let perBin = filtered.length / deezNutz.colorsDark.length;
                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? deezNutz.colorsLight[Math.floor(i / perBin)]
                      : deezNutz.colorsDark[Math.floor(i / perBin)]
                  );
                  i++;
                });
              } else {
                // method of non equal distribution
                let n = deezNutz.colorsDark.length;
                let max = parseFloat(filtered[0].kg);
                let min = parseFloat(filtered[filtered.length - 1].kg);
                let nBins = (max - min + 1) / n;

                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? deezNutz.colorsLight[
                          Math.floor((element.kg - min) / nBins)
                        ]
                      : deezNutz.colorsDark[
                          Math.floor((element.kg - min) / nBins)
                        ]
                  );
                });
              }
            }
            deezNutz.finishedLoading = true;
          });
        }
      }
    },
    updateMapYear() {
      localStorage.removeItem("municipalityDataExport");
      localStorage.removeItem("municipalityDataImport");
      localStorage.removeItem("receiverData");
      localStorage.removeItem("senderData");

      this.chartDataSender = null;
      this.chartDataReceiver = null;

      this.reset();
      this.resetColors();
      this.generateHeatMap();
    },
    updateMap() {
      this.reset();
      this.resetColors();
      this.generateHeatMap();
    },
    resetColors() {
      this.svg.select(".regional-borders").attr("stroke", this.borderFill);
      this.svg.select(".regions").selectAll("path").attr("fill", "transparent");
    },
    reset() {
      console.log("resetting");
      this.regions.transition().style("fill", null);
      this.svg
        .transition()
        .duration(750)
        .call(
          this.zoom.transform,
          d3.zoomIdentity,
          d3
            .zoomTransform(this.svg.node())
            .invert([this.width / 2, this.height / 2])
        );
    },
    clicked(ev, d) {
      console.log(d.properties);
      document.getElementById("cursor-container").style.display = "none";
      this.borderFill = getComputedStyle(
        document.documentElement
      ).getPropertyValue("--accent");

      if (this.regionClicked === d.properties.OB_MID) {
        this.reset();
        this.regionClicked = null;
        this.regionClickedName = null;
      } else {
        this.regionClicked = d.properties.OB_MID;
        this.regionClickedName = d.properties.OB_UIME;
        const element = d3.select("#map-svg g #ob" + d.properties.OB_MID);
        const bounds = element.node().getBBox();
        let x0 = bounds.x;
        let x1 = bounds.x + bounds.width;
        let y0 = bounds.y;
        let y1 = bounds.y + bounds.height;

        this.regions.transition().style(
          "fill",
          "transparent"
          // getComputedStyle(document.documentElement).getPropertyValue(
          //   "--bg-02"
          // )
        );
        element.transition().style("fill", this.borderFill);
        this.svg
          .transition()
          .duration(1000)
          .call(
            this.zoom.transform,
            d3.zoomIdentity
              .translate(this.width / 2, this.height / 2)
              .scale(
                Math.min(
                  8,
                  0.9 /
                    Math.max((x1 - x0) / this.width, (y1 - y0) / this.height)
                )
              )
              .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
            d3.pointer(ev, this.svg.node())
          )
          .on("end", this.drawGraph);
      }
    },
    drawGraph() {
      let deezNutz = this;

      let monthly_data = {};
      var months_slo = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "Maj",
        6: "Jun",
        7: "Jul",
        8: "Avg",
        9: "Sep",
        10: "Okt",
        11: "Nov",
        12: "Dec",
      };

      if (this.radioModel == "import") {
        if (localStorage.receiverData) {
          this.receiverData = JSON.parse(localStorage.receiverData);
          let found = this.receiverData.filter(
            (x) => x.obcina == deezNutz.regionClicked
          );

          found.forEach((el) => {
            monthly_data[months_slo[parseInt(el.mesec)]] =
              parseInt(el.sum) / 1000;
          });
          console.log(monthly_data);
          for (const [_, value] of Object.entries(months_slo)) {
            if (monthly_data[value] == null) {
              monthly_data[value] = 0;
              console.log(_);
            }
          }
          deezNutz.chartDataReceiver = monthly_data;
        } else {
          let sql = `SELECT obcina_prejem obcina, DATE_PART('month', dat_oddaje) AS mesec, sum(kol_kg) FROM evl WHERE DATE_PART('year', dat_oddaje) = '${this.year}' AND dat_prejem_zav IS NOT NULL GROUP BY obcina, mesec ORDER BY obcina, mesec;`;
          query(sql).then(function (response) {
            if (response === "Are you dumb?")
              console.log("You are dumb, sorry.");
            else {
              deezNutz.receiverData = response;
              let found = response.filter(
                (x) => x.obcina == deezNutz.regionClicked
              );

              found.forEach((el) => {
                monthly_data[months_slo[parseInt(el.mesec)]] =
                  parseInt(el.sum) / 1000;
              });
              console.log(monthly_data);
              for (const [_, value] of Object.entries(months_slo)) {
                if (monthly_data[value] == null) {
                  monthly_data[value] = 0;
                  console.log(_);
                }
              }
              deezNutz.chartDataReceiver = monthly_data;
            }
          });
        }
      } else {
        if (localStorage.senderData) {
          this.senderData = JSON.parse(localStorage.senderData);
          let found = this.senderData.filter(
            (x) => x.obcina == deezNutz.regionClicked
          );

          found.forEach((el) => {
            monthly_data[months_slo[parseInt(el.mesec)]] =
              parseInt(el.sum) / 1000;
          });
          console.log(monthly_data);
          for (const [_, value] of Object.entries(months_slo)) {
            if (monthly_data[value] == null) {
              monthly_data[value] = 0;
              console.log(_);
            }
          }
          deezNutz.chartDataSender = monthly_data;
        } else {
          let sql = `SELECT obcina_oddaja obcina, DATE_PART('month', dat_oddaje) AS mesec, sum(kol_kg) FROM evl WHERE DATE_PART('year', dat_oddaje) = '${this.year}' AND dat_prejem_zav IS NOT NULL GROUP BY obcina, mesec ORDER BY obcina, mesec;`;
          query(sql).then(function (response) {
            if (response === "Are you dumb?")
              console.log("You are dumb, sorry.");
            else {
              deezNutz.senderData = response;
              let found = response.filter(
                (x) => x.obcina == deezNutz.regionClicked
              );

              found.forEach((el) => {
                monthly_data[months_slo[parseInt(el.mesec)]] =
                  parseInt(el.sum) / 1000;
              });
              console.log(monthly_data);
              for (const [_, value] of Object.entries(months_slo)) {
                if (monthly_data[value] == null) {
                  monthly_data[value] = 0;
                  console.log(_);
                }
              }
              deezNutz.chartDataSender = monthly_data;
            }
          });
        }
      }

      this.showGraph = true;
    },
    hideGraph() {
      this.showGraph = false;
      this.reset();
    },
    handleZoom(e) {
      d3.select("#map-svg .regional-borders").attr("transform", e.transform);
      d3.select("#map-svg g").attr("transform", e.transform);
    },
    parseWeight(number) {
      let x = parseFloat(number);
      if (x < 1000) return { w: parseInt(x), unit: "kg" };
      else if (x < 1000000) return { w: parseInt(x / 1000), unit: "ton" };
      else if (x < 1000000000)
        return { w: parseInt(x / 1000000), unit: "kiloton" };
      else return { w: parseInt(x), unit: "kg" };
    },
    draw() {
      this.svg = null;
      // this.mainFill = getComputedStyle(
      //   document.documentElement
      // ).getPropertyValue("--bg-02");
      this.mainFill = "transparent";
      this.borderFill = getComputedStyle(
        document.documentElement
      ).getPropertyValue("--accent");

      this.width = 1920;
      this.height = 1080;
      this.svg = d3
        .select("#map-svg")
        .attr("viewBox", [0, 0, this.width, this.height]);

      var geoData = topojson.feature(geoJsonOB, geoJsonOB.objects.regions);

      var projection = d3
        .geoIdentity()
        .reflectY(true)
        .fitSize([this.width, this.height], geoData);

      this.path = d3.geoPath().projection(projection);

      this.zoom = d3
        .zoom()
        .scaleExtent([1, 5])
        .translateExtent([
          [0, 0],
          [this.width, this.height],
        ])
        .on("zoom", this.handleZoom);

      let deezNutz = this;

      this.svg
        .append("g")
        .attr("class", "regions")
        .on("mouseenter", function () {
          document.getElementById("cursor-container").classList.add("entered");
          document
            .getElementsByTagName("html")[0]
            .classList.remove("show-cursor");
          // promiseAnime({
          //   targets: "#overlay-box",
          //   opacity: [0, 1],
          //   scale: 1.0,
          //   translateX: "-100%",
          //   easing: "easeOutCirc",
          //   duration: 6000,
          // }).then(() => console.log(""));
          // anime({
          //   targets: "#overlay-box",
          //   opacity: [0, 1],
          //   scale: [0.0, 1.0],
          //   translateX: "-125%",
          //   easing: "easeOutCirc",
          //   duration: 500,
          // });
        })
        .on("mouseleave", function () {
          document
            .getElementById("cursor-container")
            .classList.remove("entered");
          document.getElementById("cursor-container").style.display = "none";
          document.getElementsByTagName("html")[0].classList.add("show-cursor");
          // document.getElementById("overlay-box").style.transform =
          //   "translateX(-50%)";
        })
        .on("mousedown", function () {
          document.getElementById("cursor-container").style.display = "none";
        })
        .on("mouseup", function () {
          document.getElementById("cursor-container").style.display = "block";
        })
        .selectAll("path")
        .data(topojson.feature(geoJsonOB, geoJsonOB.objects.regions).features)
        .enter()
        .append("path")
        .attr("d", this.path)
        .attr("fill", this.mainFill)
        .attr("id", function (d) {
          return "ob" + d.properties.OB_MID;
        })
        .on("mouseover", function (ev, d) {
          if (!deezNutz.finishedLoading) return;
          let overlay = document.getElementById("overlay-box");
          overlay.querySelector("span").innerHTML = d.properties.OB_UIME;
          overlay.getElementsByClassName("value")[0].innerHTML = "-";
          overlay.getElementsByClassName("description")[0].innerHTML =
            "Ni podatka";

          if (deezNutz.radioModel == "import") {
            if (deezNutz.municipalityDataImport !== undefined) {
              const obj = deezNutz.municipalityDataImport.find(
                (o) => o.obcina == d.properties.OB_MID
              );
              if (obj !== undefined) {
                let val = overlay.getElementsByClassName("value")[0];
                let description =
                  overlay.getElementsByClassName("description")[0];

                let weight = deezNutz.parseWeight(obj.kg);
                val.innerHTML = `${weight.w} ${weight.unit}`;
                description.innerHTML = `Količina uvoženih odpadkov`;
              }
            }
          } else {
            if (deezNutz.municipalityDataExport !== undefined) {
              const obj = deezNutz.municipalityDataExport.find(
                (o) => o.obcina == d.properties.OB_MID
              );
              if (obj !== undefined) {
                let val = overlay.getElementsByClassName("value")[0];
                let description =
                  overlay.getElementsByClassName("description")[0];

                let weight = deezNutz.parseWeight(obj.kg);
                val.innerHTML = `${weight.w} ${weight.unit}`;
                description.innerHTML = `Količina izvoženih odpadkov`;
              }
            }
          }

          if (!deezNutz.heatMap)
            d3.select(this).attr(
              "fill",
              getComputedStyle(document.documentElement).getPropertyValue(
                "--map-hover"
              )
            );
        })
        .on("mouseout", function () {
          if (!deezNutz.heatMap)
            d3.select(this).attr(
              "fill",
              "transparent"
              // getComputedStyle(document.documentElement).getPropertyValue(
              //   "--bg-02"
              // )
            );
        })
        .on("click", this.clicked);

      // GLOW
      //Container for the gradients
      var defs = this.svg.append("defs");

      //Filter for the outside glow
      var filter = defs.append("filter").attr("id", "glow");
      filter
        .append("feGaussianBlur")
        .attr("stdDeviation", "3.5")
        .attr("result", "coloredBlur");
      var feMerge = filter.append("feMerge");
      feMerge.append("feMergeNode").attr("in", "coloredBlur");
      feMerge.append("feMergeNode").attr("in", "SourceGraphic");

      this.svg
        .append("path")
        .attr("class", "regional-borders")
        .on("mouseenter", function () {
          document.getElementById("cursor-container").style.display = "block";
          document
            .getElementsByTagName("html")[0]
            .classList.remove("show-cursor");
          // document.getElementById("overlay-box").style.transform =
          //   "translate(-50%, -50%)";
        })
        .on("mouseleave", function () {
          document.getElementById("cursor-container").style.display = "none";
          document.getElementsByTagName("html")[0].classList.add("show-cursor");
        })
        .attr("fill", "none")
        .attr("stroke", this.borderFill)
        .style("filter", "url(#glow)")
        .attr(
          "d",
          this.path(topojson.mesh(geoJsonOB, geoJsonOB.objects.regions))
        );

      this.regions = d3.selectAll("#map-svg g path");
    },
  },
};
</script>

<style lang="scss" scoped>
#map-svg {
  background-color: transparent;
  max-height: 100%;
  border-radius: 4vh;
  margin-top: 3vh;
}

.regional-borders {
  pointer-events: none;
}

html:not(.loaded) #cursor-container .border,
html:not(.loaded) #cursor-container .dot {
  opacity: 0;
}

.filter-container {
  position: relative;
  display: inline-block;
  width: 100%;
}
.radio-group {
  position: static;
  vertical-align: middle;
  left: 0;
}
.label {
  margin-right: 1em;
  margin-left: 3em;
}
#GraphBox {
  position: absolute;
  left: 50%;
  top: 54%;
  width: 85%;
  height: 75%;
  transform: translate(-50%, -50%);
  border-radius: 4vh;
  background-color: var(--bg-03-not-transparent);
}
#Overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 4vh;
  // background-color: var(--blur-color);
  -webkit-backdrop-filter: blur(55px);
  backdrop-filter: blur(5px);
}
#GraphBox div {
  position: absolute;
  padding: 0 4rem;
  height: max-content;
  max-height: 65%;
}
#GraphBox p {
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
  margin-top: 2rem;
  padding-top: 2rem;
}
</style>
