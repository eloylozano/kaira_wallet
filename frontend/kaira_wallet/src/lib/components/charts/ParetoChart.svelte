<script lang="ts">
	import { onMount } from 'svelte';
	import * as echarts from 'echarts';
	import { statsService } from '$lib/stores/stats.svelte';

	let chartEl: HTMLDivElement | undefined = $state();
	let chart: echarts.ECharts | undefined;

	const barColor = '#f43f5e';
	const lineColor = '#10b981';

	// Usamos el snippet de data directamente para mayor claridad
	let paretoData = $derived(statsService.distributionData.pareto || []);

	onMount(() => {
		const resizeHandler = () => chart?.resize();
		window.addEventListener('resize', resizeHandler);

		return () => {
			window.removeEventListener('resize', resizeHandler);
			chart?.dispose(); // Limpieza crucial
		};
	});

	$effect(() => {
		// Accedemos a paretoData de forma reactiva
		const data = paretoData;

		if (chartEl && data.length > 0) {
			if (!chart) {
				chart = echarts.init(chartEl);
			}
			updateChart(data);

			// Pequeño delay para asegurar que el DOM no sea 'hidden'
			// al calcular las dimensiones
			setTimeout(() => chart?.resize(), 0);
		}
	});

	function updateChart(data: any[]) {
		if (!chart) return;
		const isMobile = window.innerWidth < 768;
		const names = data.map((d) => d.name);
		const amounts = data.map((d) => d.amount);
		const percents = data.map((d) => d.percent);

		chart.setOption({
			backgroundColor: 'transparent',
			tooltip: {
				trigger: 'axis',
				backgroundColor: 'rgba(23, 23, 23, 0.95)',
				borderWidth: 0,
				borderRadius: 12,
				padding: 12,
				textStyle: { color: '#fff', fontSize: 12 },
				confine: true,
				axisPointer: {
					type: 'shadow',
					shadowStyle: { color: 'rgba(255, 255, 255, 0.03)' }
				},
				formatter: (params: any) => {
					const [bar, line] = params;
					return `
                        <div style="min-width: 140px; display: flex; flex-direction: column; gap: 6px;">
                            <b style="color: rgba(255,255,255,0.5); text-transform: uppercase; font-size: 10px; letter-spacing: 0.05em;">${bar.name}</b>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: rgba(255,255,255,0.7); font-size: 11px;">Gasto:</span>
                                <b style="font-size: 12px;">${bar.value.toLocaleString('es-ES', { minimumFractionDigits: 2 })}€</b>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: rgba(255,255,255,0.7); font-size: 11px;">Acumulado:</span>
                                <b style="color:${lineColor}; font-size: 12px;">${line.value}%</b>
                            </div>
                        </div>`;
				}
			},
			grid: { top: '15%', left: '4%', right: '4%', bottom: '12%', containLabel: true },
			xAxis: {
				type: 'category',
				data: names,
				axisLabel: {
					color: 'rgba(255,255,255,0.4)',
					fontSize: 9, // Un pelín más pequeño para ayudar al espacio
					fontWeight: '500',
					interval: 0,
					// Rotación inteligente: 45 grados en móvil, o si hay muchos datos
					rotate: isMobile || names.length > 5 ? 45 : 0,
					// Alineación vertical/horizontal para que el texto nazca desde la marca
					align: isMobile ? 'right' : 'center',
					verticalAlign: isMobile ? 'middle' : 'top',
					// Recorte de texto para que no se pisen
					formatter: (v: string) => {
						const limit = isMobile ? 8 : 12;
						return v.length > limit ? v.slice(0, limit) + '..' : v;
					}
				},
				axisLine: { show: false },
				axisTick: { show: false }
			},
			yAxis: [
				{
					type: 'value',
					splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } },
					axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 10 }
				},
				{
					type: 'value',
					max: 100,
					splitLine: { show: false },
					axisLabel: { formatter: '{value}%', color: 'rgba(255,255,255,0.3)', fontSize: 10 }
				}
			],
			series: [
				{
					name: 'Gasto',
					type: 'bar',
					barWidth: '55%',
					itemStyle: {
						borderRadius: [8, 8, 0, 0],
						color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
							{ offset: 0, color: barColor },
							{ offset: 1, color: 'rgba(244, 63, 94, 0.02)' }
						])
					},
					data: amounts
				},
				{
					name: 'Porcentaje',
					type: 'line',
					yAxisIndex: 1,
					smooth: true,
					symbol: 'circle',
					symbolSize: 4,
					showSymbol: false,
					lineStyle: { color: lineColor, width: 3, cap: 'round' },
					itemStyle: { color: lineColor },
					data: percents,
					markLine: {
						symbol: 'none',
						label: { show: false },
						lineStyle: { type: 'dashed', color: 'rgba(255,255,255,0.15)', width: 1 },
						data: [{ yAxis: 80 }]
					}
				}
			]
		});
	}
</script>

<div class="kaira-panel rounded-[32px] p-6">
	<div class="mb-6 flex items-center justify-between px-2">
		<div class="flex flex-col gap-1">
			<span class="text-[10px] font-black tracking-[0.2em] text-white/30 uppercase"
				>Análisis Pareto</span
			>
		</div>
		<div class="flex gap-5">
			<div class="flex items-center gap-2">
				<div
					class="h-1.5 w-1.5 rounded-full bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.4)]"
				></div>
				<span class="text-[10px] font-bold tracking-wider text-white/40 uppercase">Gasto</span>
			</div>
			<div class="flex items-center gap-2">
				<div
					class="h-1.5 w-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]"
				></div>
				<span class="text-[10px] font-bold tracking-wider text-white/40 uppercase">Acum.</span>
			</div>
		</div>
	</div>

	<div
		bind:this={chartEl}
		class="h-72 w-full transition-opacity duration-500"
		class:hidden={paretoData.length === 0}
		class:opacity-0={paretoData.length === 0}
	></div>

	{#if paretoData.length === 0}
		<div class="flex h-72 flex-col items-center justify-center">
			<div
				class="mb-3 h-10 w-10 animate-pulse rounded-full border-2 border-dashed border-white/10"
			></div>
			<p class="text-[10px] font-black tracking-[0.2em] text-white/20 uppercase">
				Sin datos para este periodo
			</p>
		</div>
	{/if}
</div>

<style>
	.hidden {
		display: none;
	}
</style>
