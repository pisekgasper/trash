<template>
	<svg id="map-svg"></svg>
	<custom-cursor></custom-cursor>
	<div id="overlay-box" v-if="showOverlay"></div>
</template>

<script>
	import * as d3 from 'd3';
	import * as topojson from 'topojson';
	import geoJsonOB from '../assets/geojson/OB_topo.json';

	import CustomCursor from './CustomCursor.vue'

	export default {
		components: {
			CustomCursor,
		},
		data() {
			return {
				svg: null,
				g: null,
				path: null,
				zoom: null,
				width: null,
				height: null,
				mainFill: null,
				borderFill: null,
			};
		},
		mounted() {
			document.getElementsByTagName('html')[0].classList.add('loaded');
			this.$nextTick().then(() => {this.draw()});
		},
		methods: {
			zoomed(event) {
				const {transform} = event;
				this.g.attr("transform", transform);
    			this.g.attr("stroke-width", 1 / transform.k);
			},
			clicked(event, d) {
				const [[x0, y0], [x1, y1]] = this.path.bounds(d);
				event.stopPropagation();
				this.regions.transition().style("fill", null);
				d3.select('#map-svg').transition().style("fill", "red");
				this.svg.transition().duration(750).call(
					this.zoom.transform,
					d3.zoomIdentity
						.translate(this.width / 2, this.height / 2)
						.scale(Math.min(8, 0.9 / Math.max((x1 - x0) / this.width, (y1 - y0) / this.height)))
						.translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
					d3.pointer(event, this.svg.node())
				);
			},
			draw() {
				this.svg = null;
				this.mainFill = getComputedStyle(document.documentElement).getPropertyValue('--bg-04');
				this.borderFill = getComputedStyle(document.documentElement).getPropertyValue('--accent');
				console.log(this.mainFill);
				let width = 1920;
				let height = 1080;
				this.svg = d3.select('#map-svg')
					.attr("viewBox", [0, 0, width, height]);

				var geoData = topojson.feature(geoJsonOB, geoJsonOB.objects.regions);

				var projection = d3
					.geoIdentity()
					.reflectY(true)
					.fitSize([width, height], geoData);
					
				var path = d3.geoPath().projection(projection);

				
				this.svg.append('g')
				.attr('class', 'regions')
				.on('mouseenter', function () {
					document.getElementById('cursor-container').style.display = 'block';
					document.getElementsByTagName('html')[0].classList.remove('show-cursor');
				})
				.on('mouseleave', function () {
					document.getElementById('cursor-container').style.display = 'none';
					document.getElementsByTagName('html')[0].classList.add('show-cursor');
				})
				.selectAll('path')
				.data(topojson.feature(geoJsonOB, geoJsonOB.objects.regions).features)
				.enter()
				.append('path')
				.attr('d', path)
				.attr('fill', this.mainFill)
				.on('mouseover', function (ev, d) {
					console.log(d.properties.OB_UIME);
					document.getElementById('overlay-box').querySelector('span').innerHTML = d.properties.OB_UIME;
					d3.select(this).attr('fill', getComputedStyle(document.documentElement).getPropertyValue('--bg-02'));
				})
				.on('mouseout', function() {
					d3.select(this).attr('fill', getComputedStyle(document.documentElement).getPropertyValue('--bg-04'));
				});

				// GLOW
				//Container for the gradients
				var defs = this.svg.append("defs");

				//Filter for the outside glow
				var filter = defs.append("filter")
					.attr("id","glow");
				filter.append("feGaussianBlur")
					.attr("stdDeviation","5")
					.attr("result","coloredBlur");
				var feMerge = filter.append("feMerge");
				feMerge.append("feMergeNode")
					.attr("in","coloredBlur");
				feMerge.append("feMergeNode")
					.attr("in","SourceGraphic");

				this.svg.append("path")
					.attr("class", "regional-borders")
					.on('mouseenter', function () {
						document.getElementById('cursor-container').style.display = 'block';
						document.getElementsByTagName('html')[0].classList.remove('show-cursor');
					})
					.on('mouseleave', function () {
						document.getElementById('cursor-container').style.display = 'none';
						document.getElementsByTagName('html')[0].classList.add('show-cursor');
					})
					.attr('fill', 'none')
					.attr('stroke', '#18d089')
					.attr("d", path(topojson.mesh(geoJsonOB, geoJsonOB.objects.regions)));
				d3.selectAll('path')
				.style("filter", "url(#glow)");
			}
		},
	};
</script>

<style lang="scss" scoped>
	#map-svg {
		background-color: transparent;
		max-height: 100%;
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
