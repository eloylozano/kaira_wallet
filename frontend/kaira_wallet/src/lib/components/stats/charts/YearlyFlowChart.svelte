<script lang="ts">
	import { onMount } from 'svelte';
	import * as echarts from 'echarts';
	import { statsService } from '$lib/stores/domain/stats.svelte';
	import { settingsStore } from '$lib/stores/domain/settings.svelte';

	let chartEl: HTMLDivElement | undefined = $state();
	let chart: echarts.ECharts | undefined;

	const monthLabels = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];

	const fmt = (n: number) =>
		n.toLocaleString('es-ES', {
			style: 'currency',
			currency: 'EUR',
			maximumFractionDigits: 0
		});

	let chartData = $derived(() => {
		const raw = statsService.monthlyBreakdown ?? [];
		const base = Array.from({ length: 12 }, (_, i) => ({
			month: i,
			income: 0,
			expense: 0,
			invest: 0
		}));

		for (const row of raw) {
			if (!row?.month) continue;
			const parts = row.month.split('-');
			const m = Number(parts[1]) - 1;
			if (isNaN(m) || m < 0 || m > 11) continue;

			base[m] = {
				month: m,
				income: Number(row.income || 0),
				expense: Number(row.expense || 0),
				invest: Number(row.invest || 0)
			};
		}
		return base;
	});

	let budget = $derived(() => Number(settingsStore.monthlyBudget || 0));

	onMount(() => {
		const resizeHandler = () => chart?.resize();
		window.addEventListener('resize', resizeHandler);
		return () => {
			window.removeEventListener('resize', resizeHandler);
			chart?.dispose();
		};
	});

	$effect(() => {
		if (chartEl && chartData()) {
			if (!chart) chart = echarts.init(chartEl);
			updateChart();
		}
	});

	function updateChart() {
		if (!chart) return;

		const data = chartData();
		const incomes = data.map(d => d.income);
		const expenses = data.map(d => d.expense);
		const invests = data.map(d => d.invest);

		const option = {
			backgroundColor: 'transparent',
			tooltip: {
				trigger: 'axis',
				backgroundColor: 'rgba(10, 10, 10, 0.95)',
				borderWidth: 1,
				borderColor: 'rgba(255,255,255,0.1)',
				borderRadius: 16,
				padding: 12,
				textStyle: { color: '#fff' },
				axisPointer: { type: 'none' },
				formatter: (params: any) => {
					let html = `<div style="min-width: 120px;">`;
					html += `<div style="font-size: 10px; text-transform: uppercase; opacity: 0.5; font-weight: 900; letter-spacing: 0.1em; margin-bottom: 6px;">${params[0].axisValueLabel}</div>`;
					
					params.forEach((p: any) => {
						if (p.value > 0) {
							html += `<div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; margin-top: 3px;">`;
							html += `<span style="color: ${p.color}; font-weight: 700;">${p.seriesName}:</span>`;
							html += `<span style="font-weight: 900; margin-left: 8px;">${fmt(p.value)}</span>`;
							html += `</div>`;
						}
					});
					html += `</div>`;
					return html;
				}
			},
			// Grid más ajustado para aprovechar mejor el espacio vertical y horizontal
			grid: { top: '12%', left: '4%', right: '8%', bottom: '12%', containLabel: true },
			xAxis: {
				type: 'category',
				data: monthLabels,
				axisLabel: {
					color: 'rgba(255,255,255,0.3)',
					fontSize: 10,
					fontWeight: '900',
					margin: 12
				},
				axisLine: { show: false },
				axisTick: { show: false }
			},
			yAxis: {
				type: 'value',
				splitLine: { 
					lineStyle: { color: 'rgba(255,255,255,0.04)', type: 'dashed' } 
				},
				axisLabel: {
					color: 'rgba(255,255,255,0.3)',
					fontSize: 9,
					fontWeight: '700'
				}
			},
			series: [
				{
					name: 'Ingresos',
					type: 'bar',
					data: incomes,
					itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] },
					barGap: '20%',
					barMaxWidth: 8
				},
				{
					name: 'Gastos',
					type: 'bar',
					data: expenses,
					itemStyle: { color: '#f43f5e', borderRadius: [4, 4, 0, 0] },
					barMaxWidth: 8
				},
				{
					name: 'Inversión',
					type: 'bar',
					data: invests,
					itemStyle: { color: '#38bdf8', borderRadius: [4, 4, 0, 0] },
					barMaxWidth: 8
				},
				{
					name: 'Meta',
					type: 'line',
					data: [],
					markLine: {
						silent: true,
						symbol: 'none',
						lineStyle: {
							type: 'dashed',
							color: 'rgba(250, 204, 21, 0.5)',
							width: 1
						},
						label: {
							formatter: `Meta\n${budget()}€`,
							position: 'end',
							color: 'rgba(250, 204, 21, 0.7)',
							fontSize: 9,
							fontWeight: 'bold',
							lineHeight: 12
						},
						data: [{ yAxis: budget() }]
					}
				}
			]
		};

		chart.setOption(option, true);
	}
</script>

<!-- Cambiado de h-64 a h-80 y optimizado el padding interno -->
<div class="glass-panel relative flex h-80 flex-col rounded-[32px] border border-white/10 bg-white/5 pt-5 pb-3 px-4">
	<p class="text-center text-[8px] font-black tracking-widest uppercase opacity-40">
		Flujo Anual {statsService.selectedYear}
	</p>

	<div bind:this={chartEl} class="relative mt-2 h-full w-full"></div>
</div>