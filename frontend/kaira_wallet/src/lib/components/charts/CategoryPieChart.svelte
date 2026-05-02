<script lang="ts">
	import { onMount } from 'svelte';
	import * as echarts from 'echarts';
	import { statsService } from '$lib/stores/stats.svelte';

	let chartEl: HTMLDivElement;
	let chart: echarts.ECharts;

	// Colores Kaira consistentes para el gráfico y la leyenda manual
	const kairaPalette = [
		'#f43f5e',
		'#10b981',
		'#0ea5e9',
		'#f59e0b',
		'#8b5cf6',
		'#64748b',
		'#ec4899',
		'#06b6d4'
	];

	let categories = $derived(() =>
		(statsService.distributionData.expenses || [])
			.map((c) => ({
				name: c.name,
				value: Number(c.value || 0)
			}))
			.sort((a, b) => b.value - a.value)
	);

	onMount(() => {
		chart = echarts.init(chartEl);
		window.addEventListener('resize', () => chart?.resize());
	});

	$effect(() => {
		if (categories().length > 0) updateChart();
	});

	function updateChart() {
		if (!chart) return;
		chart.setOption({
			backgroundColor: 'transparent',
			color: kairaPalette,
			tooltip: {
				trigger: 'item',
				backgroundColor: 'rgba(23, 23, 23, 0.9)',
				borderWidth: 0,
				textStyle: { color: '#fff', fontSize: 11 },
				formatter: '{b}<br/><b>{c}€</b> ({d}%)',
				confine: true
			},
			series: [
				{
					type: 'pie',
					radius: ['65%', '85%'],
					avoidLabelOverlap: true,
					padAngle: 1,
					itemStyle: { borderRadius: 8, borderColor: 'transparent', borderWidth: 2 },
					label: { show: false, position: 'center' },
					emphasis: {
						label: { show: true, fontSize: 14, fontWeight: '900', color: '#fff', formatter: '{d}%' }
					},
					data: categories()
				}
			]
		});
	}
</script>

<div class="kaira-panel rounded-[32px] p-5">
	<h2 class="mb-4 px-4 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
		Distribución Mensual
	</h2>
	{#if categories().length > 0}
		<!-- Contenedor del Gráfico -->
		<div bind:this={chartEl} class="h-56 w-full"></div>

		<!-- Leyenda Dinámica Completa -->
		<div class="mt-6 grid grid-cols-2 gap-x-4 gap-y-3 border-t border-white/5 pt-5">
			{#each categories() as cat, i}
				<div class="flex items-center justify-between gap-2 overflow-hidden">
					<div class="flex items-center gap-2 overflow-hidden">
						<!-- El color se asigna según el índice de la paleta -->
						<div
							class="h-2 w-2 shrink-0 rounded-full"
							style="background-color: {kairaPalette[i % kairaPalette.length]}"
						></div>
						<span class="truncate text-[10px] font-bold tracking-tight text-white/70 uppercase">
							{cat.name}
						</span>
					</div>
					<span class="text-[10px] font-black text-white/40">
						{cat.value.toLocaleString('es-ES', { minimumFractionDigits: 2 })}€
					</span>
				</div>
			{/each}
		</div>
	{:else}
		<div class="flex h-64 items-center justify-center opacity-20">
			<p class="text-[10px] font-black tracking-widest uppercase">Sin datos</p>
		</div>
	{/if}
</div>
