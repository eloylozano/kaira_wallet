<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
    
    let { data = [] } = $props();

    let chartEl: HTMLDivElement | null = null;
    let chart: echarts.ECharts | null = null;

    const COLORS = {
        cash: '#10b981',    // Verde esmeralda
        invest: '#0ea5e9'   // Sky Blue
    };

    function updateChart() {
        if (!chart || !data || data.length === 0) return;

        chart.setOption({
            backgroundColor: 'transparent',
            // Definimos los colores globales de la paleta para que la leyenda los herede
            color: [COLORS.cash, COLORS.invest],
            tooltip: { 
                trigger: 'axis', 
                backgroundColor: 'rgba(23, 23, 23, 0.95)', 
                borderWidth: 0,
                borderRadius: 12,
                textStyle: { color: '#fff', fontSize: 11 },
                formatter: (params: any) => {
                    let res = `<div class="p-1"><b style="font-size: 12px; margin-bottom: 8px; display: block;">${params.name}</b>`;
                    params.forEach((item: any) => {
                        res += `<div style="display: flex; justify-content: space-between; gap: 20px;">
                            <span style="opacity: 0.7">${item.seriesName}</span>
                            <b style="color: ${item.color}">${item.value.toLocaleString('es-ES')}€</b>
                        </div>`;
                    });
                    res += `</div>`;
                    return res;
                }
            },
            legend: {
                show: true,
                textStyle: { color: 'rgba(255,255,255,0.4)', fontSize: 10, fontWeight: 'bold' },
                top: 0,
                icon: 'circle',
                // Forzamos a que la leyenda use el color del item
                itemStyle: {
                    borderWidth: 0
                }
            },
            grid: { left: '2%', right: '2%', bottom: '3%', top: '15%', containLabel: true },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.map((d: any) => d.date),
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 10 }
            },
            yAxis: {
                type: 'value',
                splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } },
                axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 10 }
            },
            series: [
                {
                    name: 'Efectivo',
                    data: data.map((d: any) => d.cash),
                    type: 'line',
                    stack: 'total',
                    smooth: true,
                    // itemStyle asegura que el color de la leyenda coincida
                    itemStyle: { color: COLORS.cash },
                    lineStyle: { width: 3, color: COLORS.cash },
                    areaStyle: { 
                        opacity: 0.2, 
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: COLORS.cash },
                            { offset: 1, color: 'transparent' }
                        ])
                    },
                    symbol: 'none'
                },
                {
                    name: 'Inversión',
                    data: data.map((d: any) => d.invested),
                    type: 'line',
                    stack: 'total',
                    smooth: true,
                    // itemStyle asegura que el color de la leyenda coincida
                    itemStyle: { color: COLORS.invest },
                    lineStyle: { width: 3, color: COLORS.invest },
                    areaStyle: { 
                        opacity: 0.4, 
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: COLORS.invest },
                            { offset: 1, color: 'transparent' }
                        ])
                    },
                    symbol: 'none'
                }
            ]
        });
    }

    $effect(() => {
        if (data.length > 0) updateChart();
    });

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
</script>

<div bind:this={chartEl} class="h-80 w-full"></div>