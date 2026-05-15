<script lang="ts">
	import { onMount } from 'svelte';
	import * as echarts from 'echarts';
	import { statsService } from '$lib/stores/domain/stats.svelte';
	// Cambiamos a la nueva fuente de verdad
	import { investmentStore } from '$lib/stores/domain/investments.svelte';

	// Definición de tipos para evitar errores de ECharts
	interface SunburstNode {
		name: string;
		value?: number;
		itemStyle: {
			color: string;
			opacity?: number;
		};
		children?: SunburstNode[];
	}

	interface AllocationNode {
		name: string;
		value?: number;
		children?: AllocationNode[];
	}

	let chartEl: HTMLDivElement | null = null;
	let chart: echarts.ECharts | null = null;

	// Cálculo del total invertido para el badge superior
	const totalInvested = $derived(
		statsService.distributionData.investments?.cash_ratio.invested ?? 0
	);

	// Procesamos los datos con tipado explícito y usando el store
	const sunburstData = $derived(() => {
		const allocation = statsService.distributionData.investments?.allocation || [];
		const investmentNode = allocation.find((item) => item.name === 'Inversión');
		if (!investmentNode) return [] as SunburstNode[];

		return (investmentNode.children ?? []).map((cat: AllocationNode): SunburstNode => {
			// Usamos los colores definidos en el store
			const baseColor = investmentStore.categoryColors[cat.name] || '#64748b';

			return {
				name: cat.name,
				itemStyle: { color: baseColor },
				children: cat.children?.map(
					(asset: AllocationNode, index: number): SunburstNode => ({
						// Usamos la función de alias del store
						name: investmentStore.getShortName(asset.name),
						value: asset.value,
						itemStyle: {
							color: baseColor,
							opacity: Math.max(0.4, 0.9 - index * 0.1)
						}
					})
				)
			};
		});
	});

	onMount(() => {
		const handleResize = () => chart?.resize();
		window.addEventListener('resize', handleResize);
		return () => {
			window.removeEventListener('resize', handleResize);
			chart?.dispose();
		};
	});

	$effect(() => {
		// Al llamar a sunburstData(), el efecto se volverá a ejecutar si cambias 
		// colores o reglas en el investmentStore.
		if (!chartEl || sunburstData().length === 0) return;
		if (!chart) chart = echarts.init(chartEl);
		updateChart();
	});

	function updateChart() {
		if (!chart) return;

		const option: echarts.EChartsOption = {
			backgroundColor: 'transparent',
			tooltip: {
				trigger: 'item',
				backgroundColor: 'rgba(23, 23, 23, 0.95)',
				borderWidth: 0,
				borderRadius: 12,
				textStyle: { color: '#fff', fontSize: 11 },
				formatter: (params: any) => {
					// Forzamos el formato español es-ES
					const val = params.value.toLocaleString('es-ES', { 
						minimumFractionDigits: 2,
						maximumFractionDigits: 2 
					});
					return `
                        <div style="padding: 4px;">
                            <span style="opacity: 0.5; font-size: 9px; text-transform: uppercase;">Activo</span><br/>
                            <b style="font-size: 13px;">${params.name}</b><br/>
                            <span style="color: ${params.color}; font-weight: 900;">${val}€</span>
                        </div>
                    `;
				},
				confine: true
			},
			series: [
				{
					type: 'sunburst',
					data: sunburstData(),
					radius: ['15%', '90%'],
					sort: 'desc',
					emphasis: { focus: 'ancestor' },
					levels: [
						{},
						{
							r0: '20%',
							r: '48%',
							itemStyle: { borderRadius: 8, borderWidth: 2, borderColor: '#111' },
							label: { rotate: 'tangential', fontSize: 10, fontWeight: 900, color: '#fff' }
						},
						{
							r0: '52%',
							r: '82%',
							itemStyle: { borderRadius: 6, borderWidth: 2, borderColor: '#111' },
							label: {
								position: 'outside',
								fontSize: 10,
								color: 'rgba(255,255,255,0.6)',
								fontWeight: 700
							}
						}
					]
				}
			]
		};

		chart.setOption(option);
	}
</script>

<div class="kaira-panel relative rounded-[32px] p-5">
	<div class="mb-4 flex items-start justify-between px-2">
		<div class="flex flex-col gap-1">
			<h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Cartera</h2>
			<p class="text-xs font-bold text-white/80 italic">Distribución por Activo</p>
		</div>

		<div class="flex flex-col items-end">
			<span class="text-[9px] font-black tracking-widest uppercase opacity-30">Total Invertido</span>
			<span class="text-lg font-black tracking-tighter text-white">
				{totalInvested.toLocaleString('es-ES', { 
					minimumFractionDigits: 2,
					maximumFractionDigits: 2 
				})}<span class="ml-0.5 text-xs opacity-40">€</span>
			</span>
		</div>
	</div>

	{#if sunburstData().length > 0}
		<div bind:this={chartEl} class="h-72 w-full"></div>

		<div class="mt-4 grid grid-cols-2 gap-2 border-t border-white/5 pt-4">
			{#each sunburstData() as cat}
				<div class="flex items-center gap-2">
					<div
						class="h-1.5 w-1.5 rounded-full"
						style="background-color: {cat.itemStyle.color}"
					></div>
					<span class="text-[9px] font-black tracking-tighter text-white/50 uppercase">
						{cat.name}
					</span>
				</div>
			{/each}
		</div>
	{:else}
		<div class="flex h-72 w-full items-center justify-center opacity-20">
			<p class="text-[10px] font-black tracking-widest uppercase italic">Sin datos de inversión</p>
		</div>
	{/if}
</div>
