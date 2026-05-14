<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';

    // Usamos destructuring con valores por defecto para asegurar reactividad
    let { invested = 0, cash = 0 } = $props();

    let chartEl: HTMLDivElement | null = null;
    let chart: echarts.ECharts | null = null;

    const COLORS = {
        cash: '#10b981',    // Verde (Kaira Success)
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
                radius: ['55%', '80%'], // Un poco más fino para estilo moderno
                center: ['50%', '45%'],
                avoidLabelOverlap: false,
                itemStyle: { 
                    borderRadius: 10, 
                    borderColor: '#020617', // Color de fondo para separar sectores
                    borderWidth: 3 
                },
                label: { show: false },
                emphasis: {
                    scale: true,
                    scaleSize: 5
                },
                data: [
                    { value: cash, name: 'Efectivo', itemStyle: { color: COLORS.cash } },
                    { value: invested, name: 'Inversión', itemStyle: { color: COLORS.invest } }
                ]
            }]
        });
    }

    // Svelte 5 Effect: Se activará cada vez que 'invested' o 'cash' cambien
    $effect(() => {
        // Solo intentamos actualizar si el chart ya existe
        if (chart) {
            updateChart();
        }
    });

    onMount(() => {
        if (chartEl) {
            chart = echarts.init(chartEl);
            updateChart(); // Primera carga
        }
        
        const handleResize = () => chart?.resize();
        window.addEventListener('resize', handleResize);
        
        return () => {
            window.removeEventListener('resize', handleResize);
            chart?.dispose();
        };
    });
</script>

<div class="relative h-64 w-full">
    <div bind:this={chartEl} class="h-full w-full"></div>
    
    {#if invested === 0 && cash === 0}
        <div class="absolute inset-0 flex items-center justify-center pb-8">
            <span class="text-[10px] font-black uppercase opacity-20">Sin datos</span>
        </div>
    {/if}
</div>