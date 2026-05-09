<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';

    let { value, target, title } = $props<{ value: number, target: number, title: string }>();
    let chartEl: HTMLDivElement | null = null;
    let chart: echarts.ECharts | null = null;

    // Calculamos el porcentaje real para el texto y el visual para la barra (máx 100)
    const realPercentage = $derived(target > 0 ? Math.round((value / target) * 100) : 0);
    const visualPercentage = $derived(Math.min(realPercentage, 100));

    function updateChart() {
        if (!chart) return;
        
        chart.setOption({
            backgroundColor: 'transparent',
            series: [{
                type: 'gauge',
                startAngle: 210,
                endAngle: -30,
                min: 0,
                max: 100,
                splitNumber: 8,
                axisLine: { 
                    lineStyle: { 
                        width: 6, 
                        color: [[1, 'rgba(255,255,255,0.05)']] 
                    } 
                },
                progress: { 
                    show: true, 
                    width: 6, 
                    itemStyle: { 
                        // Cambia a un color dorado si supera el 100%
                        color: realPercentage >= 100 ? '#fbbf24' : '#10b981' 
                    }, 
                    roundCap: true 
                },
                pointer: { show: false },
                axisTick: { show: false },
                splitLine: { show: false },
                axisLabel: { show: false },
                detail: {
                    valueAnimation: true,
                    offsetCenter: [0, '5%'],
                    fontSize: 28,
                    fontWeight: '900',
                    color: '#fff',
                    // Mostramos el porcentaje real (puede ser > 100%)
                    formatter: () => `${realPercentage}%`
                },
                data: [{ value: visualPercentage }]
            }]
        });
    }

    onMount(() => {
        if (chartEl) {
            chart = echarts.init(chartEl);
            updateChart();
            const resize = () => chart?.resize();
            window.addEventListener('resize', resize);
            return () => {
                window.removeEventListener('resize', resize);
                chart?.dispose();
            };
        }
    });

    // Reactividad: se actualiza cuando cambian los valores
    $effect(() => { 
        value; 
        target; 
        updateChart(); 
    });
</script>

<div class="flex flex-col items-center">
    <div bind:this={chartEl} class="h-44 w-full md:h-52"></div>
    
    <div class="text-center -mt-6 pb-4">
        <span class="text-[9px] font-black uppercase tracking-[0.2em] text-white/20">
            {title}
        </span>
        <p class="text-xs font-bold {realPercentage >= 100 ? 'text-amber-400' : 'text-emerald-400/80'}">
            {value.toLocaleString('es-ES', { maximumFractionDigits: 0 })}€ 
            <span class="mx-1 opacity-20 text-white">/</span> 
            {target.toLocaleString('es-ES', { maximumFractionDigits: 0 })}€
        </p>
    </div>
</div>

<style>
    /* Aseguramos que el chart no cause scroll horizontal en móviles */
    div {
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
</style>