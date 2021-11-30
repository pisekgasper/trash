<template>
	<div class="about">
		<div class="query-container">
			<textarea v-model="param" />
			<button v-on:click="query(param)">Query</button>
		</div>
		<div class="spinner-container">
			<trash-spinner v-if="loading"></trash-spinner>
		</div>
		<div class="container-table100" v-if="!loading">
			<div class="wrap-table100">
				<div class="table100">
					<table>
						<thead>
							<tr class="table100-head">
								<th
									v-for="(header, i) in tableHeaders"
									v-bind:key="'key' + i"
									v-bind:class="'column' + (i + 1)"
								>
									{{ header.column_name }}
								</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(row, index) in result" v-bind:key="index">
								<td
									v-for="(col, name, i) in row"
									v-bind:key="'key' + (index + i)"
									v-bind:class="'column' + (i + 1)"
								>
									{{ col }}
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import http from '../http-common';
	import TrashSpinner from '../components/TrashSpinner.vue';

	export default {
		components: {
			TrashSpinner,
		},
		data() {
			return {
				tableHeaders: [],
				result: [],
				loading: false,
				param: '',
				mediaQuery: null,
			};
		},
		mounted() {
			this.mediaQuery = window.matchMedia('(max-width: 992px)');
			this.mediaQuery.addEventListener('change', this.handleTabletChange);
			this.handleTabletChange(this.mediaQuery);
		},
		methods: {
			query(param) {
				this.loading = true;
				const tbl = param
					.substring(param.toUpperCase().indexOf('FROM') + 5)
					.split(' ')[0];
				const columnNames =
					"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" +
					tbl +
					"' ORDER BY ORDINAL_POSITION";
				http
					.get('/trash', { params: { q: columnNames } })
					.then((response) => {
						//console.log(response);
						this.tableHeaders = response.data;
					})
					.catch((e) => {
						console.log(e);
						this.loading = false;
					});
				http
					.get('/trash', { params: { q: param } })
					.then((response) => {
						//console.log(response);
						this.result = response.data;
						this.loading = false;
					})
					.catch((e) => {
						console.log(e);
						this.loading = false;
					});
				this.handleTabletChange(this.mediaQuery);
			},
			handleTabletChange(e) {
				if (e.matches) {
					let tbody = document.getElementsByTagName('tbody')[0];
					if (tbody == undefined) return;
					let trs = tbody.getElementsByTagName('tr');
					for (let i = 0; i < trs.length; i++) {
						let tds = trs[i].querySelectorAll('td');
						for (let j = 0; j < tds.length; j++) {
							let td = trs[i].querySelectorAll('td')[j];
							if (td != null) {
								let span = document.createElement('span');
								span.innerHTML = Object.assign({}, this.tableHeaders[j])[
									'column_name'
								];
								span.style.float = 'left';
								span.style.paddingLeft = '15px';
								td.parentNode.insertBefore(span, td);
							}
						}
					}
				} else {
					let tbody = document.getElementsByTagName('tbody')[0];
					if (tbody == undefined) return;
					let trs = tbody.getElementsByTagName('tr');
					for (let i = 0; i < trs.length; i++) {
						let tds = trs[i].querySelectorAll('td');
						for (let j = 0; j < tds.length; j++) {
							let td = trs[i].querySelectorAll('td')[j];
							if (td != null) {
								let parent = td.parentNode;
								let spans = parent.getElementsByTagName('span');
								if (spans != null && spans != undefined) {
									for (let j = 0; j < spans.length; j++) spans[j].remove();
								}
							}
						}
					}
				}
			},
		},
	};
</script>

<style lang="scss" scoped>
	@import '../assets/css/table.css';

	.spinner-container {
		width: 100%;
		padding: 10px 0;
	}

	.query-container {
		position: relative;
		width: 100%;
		height: min-content;
		align-items: center;

		& textarea {
			margin: 10px auto;
			display: block;
			width: 50%;
			resize: vertical;
		}
		& button {
			margin: auto;
			display: block;
			width: 50%;
		}
	}
</style>
