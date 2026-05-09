<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';

    // Recibimos los valores calculados desde el padre (EquityTab)
    let { invested = 0, cash = 0 } = $props();

    let chartEl: HTMLDivElement | null = null;
    let chart: echarts.ECharts | null = null;

    const COLORS = {
        cash: '#10b981',    // Verde
        invest: '#0ea5e9'   // Sky Blue
    };

    function updateChart() {
        if (!chart) return;

        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(23, 23, 23, 0.95)',
                borderWidth: 0,
                borderRadius: 12,
                textStyle: { color: '#fff', fontSize: 11 },
                formatter: (params: any) => {
                    return `<div class="p-1">
                        <b style="color: ${params.color}">${params.name}</b><br/>
                        ${params.value.toLocaleString('es-ES')}€ (${params.percent}%)
                    </div>`;
                }
            },
            legend: {
                show: true,
                bottom: '0%',
                left: 'center',
                textStyle: { color: 'rgba(255,255,255,0.4)', fontSize: 10, fontWeight: 'bold' },
                icon: 'circle'
            },
            series: [{
                name: 'Ratio de Liquidez',
                type: 'pie',
                radius: ['50%', '80%'],
                center: ['50%', '45%'],
                avoidLabelOverlap: false,
                itemStyle: { 
                    borderRadius: 8, 
                    borderColor: 'rgba(0,0,0,0.2)', 
                    borderWidth: 2 
                },
                label: { show: false },
                emphasis: {
                    label: {
                        show: false
                    }
                },
                data: [
                    { value: cash, name: 'Efectivo', itemStyle: { color: COLORS.cash } },
                    { value: invested, name: 'Inversión', itemStyle: { color: COLORS.invest } }
                ]
            }]
        });
    }

    // Reaccionar a cambios en las props
    $effect(() => {
        if (invested !== undefined || cash !== undefined) {
            updateChart();
        }
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

<div bind:this={chartEl} class="h-64 w-full"></div>