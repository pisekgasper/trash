<template>
	<div id="nav">
		<router-link to="/">Home</router-link>
		<router-link to="/about">About</router-link>
	</div>
	<router-view />
</template>

<style lang="scss">
	@import './assets/css/reset.css';
	@import './assets/css/global.css';

	#app {
		font-family: Avenir, Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: var(--font-color);
		position: relative;
	}

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
</style>
