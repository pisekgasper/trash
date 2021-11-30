<template>
	<!--<canvas id="map-canvas" width="960" height="600"></canvas>-->
	<svg id="map-svg" width="960" height="600"></svg>
</template>

<script>
	import * as d3 from 'd3';
	import * as topojson from 'topojson';
	import geoJsonSVN from '../assets/geojson/svn.json';
	import geoJsonSVNRegional from '../assets/geojson/svn_regional.json';
	import geoJsonOB from '../assets/geojson/OB_topo.json';

	console.log(geoJsonSVN);
	console.log(geoJsonSVNRegional);
	console.log(geoJsonOB);
	console.log(d3);

	export default {
		data() {
			return {};
		},
		mounted() {
			/*let canvas = document.getElementById('map-canvas');
			let width = canvas.offsetWidth;
			let height = canvas.offsetHeight;*/
			console.log(
				topojson.feature(geoJsonOB, geoJsonOB.objects.regions).features
			);
			var svg = d3.select('#map-svg');
			let width = 960;
			let height = 720;

			var geoData = topojson.feature(geoJsonOB, geoJsonOB.objects.regions);

			var projection = d3
				.geoIdentity()
				.reflectY(true)
				.fitSize([width, height], geoData);

			var path = d3.geoPath().projection(projection);

			svg.append('path').datum(geoData).attr('d', path);

			/*var projection = d3
				.geoMercator()
				.scale(100)
				.center([0, 70])
				.translate([width / 2, height / 2]);

			var ctx = canvas.getContext('2d');
			const pathGenerator = d3.geoPath(projection, ctx);

			ctx.fillStyle = 'yellow';
			ctx.fillRect(0, 0, width, height);

			ctx.beginPath();
			pathGenerator(geoJsonSVNRegional);

			ctx.fillStyle = 'red';
			ctx.fill;

			ctx.strokeStyle = '#69b3a2';
			ctx.stroke();*/
		},
		methods: {},
	};
</script>

<style lang="scss" scoped>
	.regions {
		fill: red;
	}
	.regional-borders {
		fill: none;
		stroke: green;
		stroke-width: 0.5px;
		stroke-linejoin: round;
		stroke-linecap: round;
		pointer-events: none;
	}
	.states :hover {
		fill: red;
	}

	.state-borders {
		fill: none;
		stroke: #fff;
		stroke-width: 0.5px;
		stroke-linejoin: round;
		stroke-linecap: round;
		pointer-events: none;
	}
</style>
