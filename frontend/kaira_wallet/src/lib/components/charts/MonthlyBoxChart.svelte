<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
    import { statsService } from '$lib/stores/stats.svelte';

    let chartEl: HTMLDivElement | undefined = $state();
    let chart: echarts.ECharts | undefined;

    let data = $derived(statsService.monthlyStatsData);

    const fmt = (n: number) => n.toLocaleString('es-ES', { 
        style: 'currency', 
        currency: 'EUR',
        maximumFractionDigits: 0 
    });

    onMount(() => {
        const resizeHandler = () => chart?.resize();
        window.addEventListener('resize', resizeHandler);
        return () => {
            window.removeEventListener('resize', resizeHandler);
            chart?.dispose();
        };
    });

    $effect(() => {
        if (chartEl && data) {
            if (!chart) chart = echarts.init(chartEl);
            updateChart();
        }
    });

    function updateChart() {
        if (!chart) return;

        const { income, expense, invest, savings } = data;

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
                    const p = params[1]; 
                    const color = p.value >= 0 ? '#10b981' : '#f43f5e';
                    return `
                        <div style="min-width: 100px;">
                            <div style="font-size: 10px; text-transform: uppercase; opacity: 0.5; font-weight: 900; letter-spacing: 0.1em;">${p.name}</div>
                            <div style="font-size: 16px; font-weight: 900; color: ${color}; italic;">${fmt(Math.abs(p.value))}</div>
                        </div>
                    `;
                }
            },
            grid: { top: '10%', left: '0%', right: '0%', bottom: '5%', containLabel: true },
            xAxis: {
                type: 'category',
                data: ['Ingresos', 'Gastos', 'Inversión', 'Restante'],
                axisLabel: { color: 'rgba(255,255,255,0.2)', fontSize: 9, fontWeight: '900', margin: 20, textTransform: 'uppercase' },
                axisLine: { show: false },
                axisTick: { show: false }
            },
            yAxis: {
                type: 'value',
                splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)', type: 'dashed' } },
                axisLabel: { show: false }
            },
            series: [
                {
                    name: 'Placeholder',
                    type: 'bar',
                    stack: 'Total',
                    itemStyle: { borderColor: 'transparent', color: 'transparent' },
                    emphasis: { itemStyle: { borderColor: 'transparent', color: 'transparent' } },
                    data: [
                        0,                      // Ingresos: empieza en el suelo
                        income - expense,       // Gastos: flota sobre lo que queda tras gastar
                        savings,                // Inversión: flota sobre el ahorro final
                        0                       // Restante: empieza en el suelo
                    ]
                },
                {
                    name: 'Valor',
                    type: 'bar',
                    stack: 'Total',
                    barWidth: '65%',
                    label: {
                        show: true,
                        position: 'inside',
                        formatter: (params: any) => params.value !== 0 ? fmt(Math.abs(params.value)) : '',
                        color: '#000',
                        fontSize: 10,
                        fontWeight: '900'
                    },
                    data: [
                        { value: income, itemStyle: { color: '#10b981', borderRadius: 12 } },
                        { value: -expense, itemStyle: { color: '#f43f5e', borderRadius: 12 } },
                        { value: -invest, itemStyle: { color: '#38bdf8', borderRadius: 12 } },
                        { 
                            value: savings, 
                            itemStyle: { 
                                color: savings >= 0 ? 'rgba(255,255,255,0.8)' : '#f43f5e', 
                                borderRadius: 12
                            },
                            label: { color: savings >= 0 ? '#000' : '#fff' }
                        }
                    ]
                }
            ]
        };

        chart.setOption(option);
    }
</script>

<div class="space-y-4">
    <!-- Mini Widgets con Estilo Corregido -->
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div class="kaira-panel-mini">
            <span class="label text-emerald-400/60">Ingresos</span>
            <span class="value">{fmt(data.income)}</span>
        </div>
        <div class="kaira-panel-mini">
            <span class="label text-rose-400/60">Gastos</span>
            <span class="value">{fmt(data.expense)}</span>
        </div>
        <div class="kaira-panel-mini col-span-2 sm:col-span-1">
            <span class="label text-sky-400/60">Inversión</span>
            <span class="value">{fmt(data.invest)}</span>
        </div>
    </div>

    <!-- Panel de Cascada -->
    <div class="kaira-panel p-6">
        <div class="mb-6 flex items-center justify-between">
            <div>
                <h3 class="text-[10px] font-black uppercase tracking-[0.2em] text-white/20">Flujo de Efectivo</h3>
                <p class="text-3xl font-black italic tracking-tighter text-white">
                    {data.savings >= 0 ? '+' : ''}{fmt(data.savings)}
                </p>
            </div>
            <div class="rounded-2xl bg-white/5 p-3 text-right">
                <span class="block text-[8px] font-black uppercase tracking-widest text-white/30">Ahorro</span>
                <p class="text-sm font-black italic text-emerald-400">
                    {data.income > 0 ? ((data.savings / data.income) * 100).toFixed(1) : 0}%
                </p>
            </div>
        </div>

        <div bind:this={chartEl} class="h-64 w-full"></div>
    </div>
</div>

<style>
    /* 
       IMPORTANTE: Para Tailwind 4.0+, si usas @apply en <style>, 
       necesitas añadir @reference para que reconozca las utilidades.
    */
    @reference "tailwindcss";

    .kaira-panel {
        @apply rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl shadow-2xl;
    }

    .kaira-panel-mini {
        @apply flex flex-col rounded-[24px] border border-white/10 bg-white/5 p-4 backdrop-blur-xl transition-all hover:bg-white/10;
    }

    .label {
        @apply text-[9px] font-black uppercase tracking-[0.2em] mb-1;
    }

    .value {
        @apply text-xl font-black italic tracking-tighter text-white;
    }
</style>