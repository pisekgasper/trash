<template>
  <svg id="map-svg"></svg>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson";
import geoJsonOB from "../assets/geojson/OB_topo.json";
// import anime from "animejs/lib/anime.es.js";
// import promiseAnime from "../helpers/animewaiter";

export default {
  data() {
    return {
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
    };
  },
  mounted() {
    document.getElementsByTagName("html")[0].classList.add("loaded");
    this.$nextTick().then(() => {
      this.draw();
    });
  },
  methods: {
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
      document.getElementById("cursor-container").style.display = "none";
      this.borderFill = getComputedStyle(
        document.documentElement
      ).getPropertyValue("--accent");

      if (this.regionClicked === d.properties.OB_ID) {
        this.reset();
        this.regionClicked = null;
      } else {
        this.regionClicked = d.properties.OB_ID;
        const element = d3.select("#map-svg g #ob" + d.properties.OB_ID);
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
          return "ob" + d.properties.OB_ID;
        })
        .on("mouseover", function (ev, d) {
          document
            .getElementById("overlay-box")
            .querySelector("span").innerHTML = d.properties.OB_UIME;
          d3.select(this).attr(
            "fill",
            getComputedStyle(document.documentElement).getPropertyValue(
              "--map-hover"
            )
          );
        })
        .on("mouseout", function () {
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
}

.regional-borders {
  pointer-events: none;
}

html:not(.loaded) #cursor-container .border,
html:not(.loaded) #cursor-container .dot {
  opacity: 0;
}

#overlay-box {
  position: fixed;
  z-index: 999;
  background-color: green;
  width: 100px;
  height: 2em;
  top: 0;
  left: 0;
}
</style>
