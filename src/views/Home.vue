<template>
	<div id="home">
		<div class="map-container">
			<slovenian-map />
		</div>
	</div>
</template>

<script>
	import SlovenianMap from '../components/SlovenianMap.vue';

	export default {
		components: {
			SlovenianMap,
		},
	};
</script>

<style lang="scss" scoped>
	#home {
		margin: 0;
		width: 100%;
		height: 100%;
	}
	.map-container {
		width: 100%;
		height: 100%;
		background-color: lightgrey;
	}
</style>
