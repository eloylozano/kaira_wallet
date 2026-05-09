<script lang="ts">
	import { onMount } from 'svelte';
	import * as echarts from 'echarts';
	// Importamos el store que ahora maneja la lógica y persistencia
	import { investmentStore } from '$lib/stores/investments.svelte';

	interface AssetNode {
		name: string;
		value?: number;
		children?: AssetNode[];
		itemStyle?: { color: string; opacity?: number };
	}

	let { data = [] }: { data: AssetNode[] } = $props();

	let chartEl: HTMLDivElement | null = null;
	let chart: echarts.ECharts | null = null;

	// Procesamos los datos usando el store para colores y nombres cortos
	const processedData = $derived(
		data.map((cat) => {
			// Accedemos a los colores desde el store
			const baseColor = investmentStore.categoryColors[cat.name] || '#64748b';

			const groupedChildren = (cat.children || []).reduce((acc: any[], asset) => {
				// Usamos el método del store para detectar el alias
				const shortName = investmentStore.getShortName(asset.name);
				const existing = acc.find((item) => item.name === shortName);

				if (existing) {
					existing.value += asset.value || 0;
				} else {
					acc.push({ name: shortName, value: asset.value || 0 });
				}
				return acc;
			}, []);

			return {
				name: cat.name,
				itemStyle: { color: baseColor },
				children: groupedChildren.map((asset, index) => ({
					...asset,
					itemStyle: {
						color: baseColor,
						opacity: Math.max(0.4, 0.9 - index * 0.08)
					}
				}))
			};
		})
	);

	function updateChart() {
		if (!chart || !processedData.length) return;

		const option: echarts.EChartsOption = {
			backgroundColor: 'transparent',
			tooltip: {
				trigger: 'item',
				backgroundColor: 'rgba(23, 23, 23, 0.95)',
				borderWidth: 0,
				borderRadius: 12,
				textStyle: { color: '#fff', fontSize: 11 },
				formatter: (params: any) => {
					// Formato numérico con coma para España
					const val =
						params.value?.toLocaleString('es-ES', {
							minimumFractionDigits: 2,
							maximumFractionDigits: 2
						}) || '0';
					return `
                        <div style="padding: 4px;">
                            <span style="opacity: 0.5; font-size: 9px; text-transform: uppercase;">
                                ${params.treePathInfo.length > 2 ? 'Activo' : 'Categoría'}
                            </span><br/>
                            <b style="font-size: 13px;">${params.name}</b><br/>
                            <span style="color: ${params.color}; font-weight: 900;">${val}€</span>
                        </div>
                    `;
				}
			},
			series: [
				{
					type: 'sunburst',
					data: processedData,
					// Ajustamos radios para que las etiquetas externas no se corten
					radius: ['15%', '75%'],
					center: ['50%', '50%'],
					sort: 'desc',
					emphasis: { focus: 'ancestor' },
					levels: [
						{}, // Root
						{
							// Nivel 1: Categorías
							r0: '20%',
							r: '45%',
							itemStyle: { borderRadius: 6, borderWidth: 2, borderColor: '#111' },
							label: { rotate: 'tangential', fontSize: 10, fontWeight: '900', color: '#fff' }
						},
						{
							// Nivel 2: Activos agrupados
							r0: '48%',
							r: '75%',
							itemStyle: { borderRadius: 4, borderWidth: 2, borderColor: '#111' },
							label: {
								position: 'outside',
								padding: 8,
								fontSize: 9,
								color: 'rgba(255,255,255,0.7)',
								overflow: 'none',
								minMargin: 5
							}
						}
					]
				}
			]
		};

		chart.setOption(option);
	}

	onMount(() => {
		if (chartEl) {
			chart = echarts.init(chartEl);
			updateChart();
		}

		const handleResize = () => chart?.resize();
		window.addEventListener('resize', handleResize);

		return () => {
			window.removeEventListener('resize', handleResize);
			chart?.dispose();
		};
	});

	// Al usar processedData ($derived), el gráfico se actualizará solo
	// si cambias una regla o un color en el investmentStore.
	$effect(() => {
		updateChart();
	});
</script>

<div bind:this={chartEl} class="h-80 w-full"></div>