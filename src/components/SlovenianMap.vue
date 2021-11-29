<template>
	<div id="map">
		ss
		<canvas id="map-canvas"></canvas>
	</div>
</template>

<script>
	import * as d3 from 'd3';
	import geoJsonSVN from '../assets/geojson/svn.json';
	import geoJsonSVNRegional from '../assets/geojson/svn_regional.json';

	console.log(geoJsonSVN);
	console.log(geoJsonSVNRegional);
	console.log(d3);

	export default {
		data() {},
		created() {
			this.createMap();
		},
		methods: {
			createMap() {
				var canvas = document.getElementById('map-canvas');

				// Actual width and height. No idea if clienWidth would be a better option..?
				var width = canvas.offsetWidth;
				var height = canvas.offsetHeight;

				// Set a projection for the map. Projection = transform a lat/long on a position on the 2d map.
				var projection = d3
					.geoNaturalEarth1()
					.scale(width / 1.3 / Math.PI)
					.translate([width / 2, height / 2]);

				// Get the 'context'
				var ctx = canvas.getContext('2d');

				// geographic path generator for given projection and canvas context
				const pathGenerator = d3.geoPath(projection, ctx);

				// Draw a background
				// ctx.fillStyle = '#ddd';
				// ctx.fillRect(0, 0, width, height);

				// initialize the path
				ctx.beginPath();

				// Got the positions of the path
				pathGenerator(geoJsonSVN);

				// Fill the paths
				ctx.fillStyle = '#999';
				ctx.fill();

				// Add stroke
				ctx.strokeStyle = '#69b3a2';
				ctx.stroke();
			},
		},
	};
</script>

<style lang="scss" scoped>
	#map {
		margin: auto;
		width: 100%;
	}
</style>
