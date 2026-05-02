<script lang="ts">
	import { onMount } from 'svelte';
	import * as echarts from 'echarts';
	import { statsService } from '$lib/stores/stats.svelte';

	let chartEl: HTMLDivElement | undefined = $state();
	let chart: echarts.ECharts | undefined;

	// Aplanamos los datos: extraemos los hijos de "Inversión" para el gráfico
	let flatData = $derived.by(() => {
		const allocation = statsService.distributionData.investments?.allocation || [];
		// Buscamos el nodo de "Inversión" y sacamos sus hijos
		const investmentNode = allocation.find((item) => item.name === 'Inversión');
		return investmentNode?.children || [];
	});

	onMount(() => {
		if (!chartEl) return;
		chart = echarts.init(chartEl);
		window.addEventListener('resize', () => chart?.resize());
		return () => chart?.dispose();
	});

	$effect(() => {
		if (chart && flatData.length > 0) {
			updateChart();
		}
	});

	function updateChart() {
		if (!chart) return;

		const option = {
			backgroundColor: 'transparent',
			tooltip: {
				backgroundColor: 'rgba(15, 15, 15, 0.8)',
				backdropFilter: 'blur(8px)',
				borderWidth: 0,
				borderRadius: 16,
				textStyle: { color: '#fff', fontSize: 12 },
				formatter: (params: any) => {
					const val = params.value.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });
					return `<div class="p-1">
                        <span style="font-size: 10px; text-transform: uppercase; opacity: 0.5; font-weight: 800;">${params.name}</span><br/>
                        <span style="font-size: 14px; font-weight: 900; font-style: italic;">${val} (${params.percent}%)</span>
                    </div>`;
				}
			},
			series: [
				{
					type: 'pie',
					radius: ['40%', '70%'],
					center: ['50%', '50%'],
					itemStyle: {
						borderRadius: 12
					},
					padAngle: 2,
					label: {
						show: true,
						position: 'outside',
						formatter: '{b}\n{d}%',
						color: 'rgba(255,255,255,0.6)',
						fontSize: 11,
						fontWeight: 'bold'
					},
					labelLine: {
						lineStyle: { color: 'rgba(255,255,255,0.2)' }
					},
					data: flatData,
					color: ['#0ea5e9', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b']
				}
			]
		};

		chart.setOption(option);
	}
</script>

<div class="kaira-panel p-6">
	<div class="mb-2 flex flex-col gap-1">
		<h3 class="text-[10px] font-black tracking-[0.2em] text-white/30 uppercase">Distribución</h3>
		<p class="text-[14px] font-black text-white/90 italic">Cartera de Activos</p>
	</div>

	<div class="relative h-[300px] w-full">
		{#if flatData.length > 0}
			<div bind:this={chartEl} class="h-full w-full"></div>
		{:else}
			<div
				class="flex h-full w-full items-center justify-center rounded-[24px] border border-dashed border-white/10 bg-white/[0.02]"
			>
				<p class="text-[10px] font-black tracking-widest text-white/20 uppercase italic">
					Sin activos
				</p>
			</div>
		{/if}
	</div>
</div>

<style>
	@reference "tailwindcss";
	.kaira-panel {
		@apply rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl;
	}
</style>
