<template>
  <div class="filter-container">
    <select name="year" v-model="year" @change="updateMap">
      <option value="2021">2021</option>
      <option value="2020">2020</option>
      <option value="2019">2019</option>
      <option value="2018">2018</option>
      <option value="2017">2017</option>
    </select>

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
  </div>

  <svg id="map-svg"></svg>
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
      heatMap: true,
      year: "2021",
      radioModel: "import",
      methodEqual: true,
      municipalityDataExport: null,
      municipalityDataImport: null,
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
      console.log("updating export");
      localStorage.municipalityDataExport = JSON.stringify(newData);
    },
    municipalityDataImport(newData) {
      console.log("updating import");

      localStorage.municipalityDataImport = JSON.stringify(newData);
    },
  },
  methods: {
    updateTheme() {
      this.theme = document.documentElement.getAttribute("data-theme");
    },
    generateHeatMap() {
      let colors = [
        "#e4f1e1",
        "#b4d9cc",
        "#89c0b6",
        "#63a6a0",
        "#448c8a",
        "#287274",
        "#0d585f",
      ];
      let colors_light = [
        "#f3e0f7",
        "#e4c7f1",
        "#d1afe8",
        "#b998dd",
        "#9f82ce",
        "#826dba",
        "#63589f",
      ];
      let colors_reversed = colors.reverse();
      let colors_light_reversed = colors_light.reverse();

      var sql =
        this.radioModel == "import"
          ? `SELECT e.obcina_prejem AS obcina, COALESCE(SUM(e.kol_kg), 0) AS kg FROM evl e WHERE DATE_PART('year', e.dat_oddaje) = '${this.year}' AND e.dat_prejem_zav IS NOT NULL GROUP BY e.obcina_prejem ORDER BY kg DESC;`
          : `SELECT e.obcina_oddaja AS obcina, COALESCE(SUM(e.kol_kg), 0) AS kg FROM evl e WHERE DATE_PART('year', e.dat_oddaje) = '${this.year}' AND e.dat_prejem_zav IS NOT NULL GROUP BY e.obcina_oddaja ORDER BY kg DESC;`;

      let deezNutz = this;

      if (this.radioModel == "import") {
        if (localStorage.municipalityDataImport) {
          this.municipalityDataImport = JSON.parse(
            localStorage.municipalityDataImport
          );
          let filtered = this.municipalityDataImport.filter(
            (x) => parseFloat(x.kg) > 0 && x.obcina !== null
          );

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
            let perBin = filtered.length / colors.length;
            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? colors_light_reversed[Math.floor(i / perBin)]
                  : colors_reversed[Math.floor(i / perBin)]
              );
              i++;
            });
          } else {
            // method of non equal distribution
            let n = colors.length;
            let max = parseFloat(filtered[0].kg);
            let min = parseFloat(filtered[filtered.length - 1].kg);
            let nBins = (max - min + 1) / n;

            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? colors_light[Math.floor((element.kg - min) / nBins)]
                  : colors[Math.floor((element.kg - min) / nBins)]
              );
            });
          }
        } else {
          query(sql).then(function (response) {
            if (response === "Are you dumb?") {
              deezNutz.heatMap = false;
              console.log("You are dumb, sorry.");
            } else {
              console.log("filtering");

              deezNutz.municipalityDataImport = response;

              let filtered = response.filter(
                (x) => parseFloat(x.kg) > 0 && x.obcina !== null
              );
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
                let perBin = filtered.length / colors.length;
                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? colors_light_reversed[Math.floor(i / perBin)]
                      : colors_reversed[Math.floor(i / perBin)]
                  );
                  i++;
                });
              } else {
                // method of non equal distribution
                let n = colors.length;
                let max = parseFloat(filtered[0].kg);
                let min = parseFloat(filtered[filtered.length - 1].kg);
                let nBins = (max - min + 1) / n;

                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? colors_light[Math.floor((element.kg - min) / nBins)]
                      : colors[Math.floor((element.kg - min) / nBins)]
                  );
                });
              }
            }
          });
        }
      } else {
        if (localStorage.municipalityDataExport) {
          this.municipalityDataExport = JSON.parse(
            localStorage.municipalityDataExport
          );
          let filtered = this.municipalityDataExport.filter(
            (x) => parseFloat(x.kg) > 0 && x.obcina !== null
          );
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
            let perBin = filtered.length / colors.length;
            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? colors_light_reversed[Math.floor(i / perBin)]
                  : colors_reversed[Math.floor(i / perBin)]
              );
              i++;
            });
          } else {
            // method of non equal distribution
            let n = colors.length;
            let max = parseFloat(filtered[0].kg);
            let min = parseFloat(filtered[filtered.length - 1].kg);
            let nBins = (max - min + 1) / n;

            filtered.forEach((element) => {
              d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                "fill",
                deezNutz.theme == "light"
                  ? colors_light[Math.floor((element.kg - min) / nBins)]
                  : colors[Math.floor((element.kg - min) / nBins)]
              );
            });
          }
        } else {
          query(sql).then(function (response) {
            if (response === "Are you dumb?") {
              deezNutz.heatMap = false;
              console.log("You are dumb, sorry.");
            } else {
              console.log("filtering");

              deezNutz.municipalityDataExport = response;

              let filtered = response.filter(
                (x) => parseFloat(x.kg) > 0 && x.obcina !== null
              );
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
                let perBin = filtered.length / colors.length;
                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? colors_light_reversed[Math.floor(i / perBin)]
                      : colors_reversed[Math.floor(i / perBin)]
                  );
                  i++;
                });
              } else {
                // method of non equal distribution
                let n = colors.length;
                let max = parseFloat(filtered[0].kg);
                let min = parseFloat(filtered[filtered.length - 1].kg);
                let nBins = (max - min + 1) / n;

                filtered.forEach((element) => {
                  d3.select(`#map-svg .regions #ob${element.obcina}`).attr(
                    "fill",
                    deezNutz.theme == "light"
                      ? colors_light[Math.floor((element.kg - min) / nBins)]
                      : colors[Math.floor((element.kg - min) / nBins)]
                  );
                });
              }
            }
          });
        }
      }
    },
    updateMap() {
      this.resetColors();
      this.generateHeatMap();
    },
    resetColors() {
      this.svg.select(".regional-borders").attr("stroke", this.borderFill);
      this.svg.select(".regions").selectAll("path").attr("fill", "transparent");
    },
    reset() {
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
      } else {
        this.regionClicked = d.properties.OB_MID;
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
          .duration(750)
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
          );
      }
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
          let overlay = document.getElementById("overlay-box");
          overlay.querySelector("span").innerHTML = d.properties.OB_UIME;

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
  display: block;
  width: 100%;
}
.radio-group {
  position: absolute;
}
</style>
