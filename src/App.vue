<template>
	<!--<div id="nav">
		<router-link to="/">Home</router-link>
		<router-link to="/about">About</router-link>
	</div>
	<router-view />-->
	<div id="content">
		<aside class="sidebar">
			<div class="theme-switcher-container">
				<theme-switcher></theme-switcher>
			</div>
		</aside>
  		<main class="main">
			<div class="row">
				<div class="graph-container shadow-02">
					<div class="heading">
						<div>GRAPH 1</div>
					</div>
					<div class="graph-content">
					</div>
				</div>
				<div class="graph-container shadow-02" @click="expand">
					<div class="heading">
						<div>GRAPH 2</div>
						<!--<div class="close-icon" @click="close">
						<svg xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
							style=" fill: white;"><path d="M 4.9902344 3.9902344 A 1.0001 1.0001 0 0 0 4.2929688 5.7070312 L 10.585938 12 L 4.2929688 18.292969 A 1.0001 1.0001 0 1 0 5.7070312 19.707031 L 12 13.414062 L 18.292969 19.707031 A 1.0001 1.0001 0 1 0 19.707031 18.292969 L 13.414062 12 L 19.707031 5.7070312 A 1.0001 1.0001 0 0 0 18.980469 3.9902344 A 1.0001 1.0001 0 0 0 18.292969 4.2929688 L 12 10.585938 L 5.7070312 4.2929688 A 1.0001 1.0001 0 0 0 4.9902344 3.9902344 z"></path></svg>
					</div>-->
					</div>
					<div class="graph-content" @click="expand">
					</div>
				</div>
				<div class="graph-container shadow-02" @click="expand">
					<div class="heading">
						<div>GRAPH 3</div>
					</div>
					<div class="graph-content">
					</div>
				</div>
			</div>
			<div class="row">
				<div class="graph-container shadow-02" @click="expand" style="flex: 1">
					<div class="heading">
						<div>DATA 4</div>
					</div>
					<div class="graph-content">
					</div>
				</div>
				<div id="regions-map" class="graph-container shadow-02" @click="expand" style="flex: 2">
					<div class="heading">
						<div>Zemljevid občin</div>
					</div>
					<div class="graph-content">
						<slovenian-map></slovenian-map>
					</div>
				</div>
			</div>
		</main>
	</div>
</template>

<script>
import SlovenianMap from './components/SlovenianMap.vue';
import ThemeSwitcher from './components/ThemeSwitch.vue';

export default {
	data() {
		return {
			dashGrid: null,
		};
	},
	components: {
		ThemeSwitcher,
		SlovenianMap,
	},
	mounted() {
		document.documentElement.classList.add('show-cursor');
		document.documentElement.setAttribute('data-theme', 'dark');
		this.dashGrid = document.querySelector('.main');
		this.expandedGraph = this.dashGrid.querySelector('#expanded-graph');
		this.showExpanded = false;
	},
	methods: {
	
	},
}
</script>

<style lang="scss">
	@import './assets/css/reset.css';
	@import './assets/css/global.css';

	#nav {
		padding: 30px;

		a {
			font-weight: bold;
			color: var(--font-color);

			&.router-link-exact-active {
				color: var(--primary-color);
			}
		}
	}

	#content {
		margin: 0 !important;
		position: relative;
		height: 100vh;
		overflow: hidden;
		background-color: transparent;
		display: grid;
		grid-template-areas: "sidebar main";
		grid-template-columns: minmax(150px, 20%) 1fr;
  		grid-template-rows: 1fr;
	}

	.theme-switcher-container {
		position: absolute;
		left: 50%;
		bottom: 20px;
		transform: translateX(-50%);
		height: min-content;
	}

	.sidebar {
		grid-area: sidebar;
		position: relative;
		background-color: var(--bg-01);
	}
	.main {
		position: relative;
		background-color: transparent;
		margin: 20px;
		display: flex;
		flex-flow: column nowrap;
		gap: 20px;
		justify-content: space-between;
	}
	.main .row {
		display: flex;
		flex-flow: row nowrap;
		gap: 20px;
	}
	.main .row:nth-child(1) {
		flex: 1;		
	}
	.main .row:nth-child(2) {
		flex: 3;
	}

	.graph-container {
		flex: 1;
		overflow: hidden;
		position: relative;
		background-color: var(--bg-02);
		display: flex;
		flex-direction: column;
		flex-wrap: nowrap;
		border-radius: 15px;
	}
	.graph-container .heading {
		width: 100%;
		text-decoration: uppercase;
		pointer-events: none;
		position: relative;
	}
	.graph-container .heading div:nth-child(1) {
		width: max-content;
		margin: 5% 10%;
		font-weight: bold;
		pointer-events: none;
	}
	.graph-container .graph-content {
		flex-grow: 1;
		max-height: 100%;
		max-width: 100%;
		overflow: hidden;
		text-align: center;
		padding: 0px 20px 20px 20px;
	}
</style>
