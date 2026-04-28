<script lang="ts">
    import { statsService } from '$lib/stores/stats.svelte';

    let data = $derived(statsService.monthlyStatsData);

    const fmt = (n: number) => n.toLocaleString('es-ES', { 
        style: 'currency', 
        currency: 'EUR',
        maximumFractionDigits: 0 
    });

    // Proporciones visuales
    let totalIn = $derived(data.income || 1);
    let expW = $derived((data.expense / totalIn) * 100);
    let invW = $derived((data.invest / totalIn) * 100);
    let savW = $derived((Math.max(0, data.savings) / totalIn) * 100);
</script>

<div class="space-y-4">
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div class="glass-panel flex flex-col rounded-3xl border border-white/10 bg-white/5 p-4">
            <span class="text-[9px] font-black uppercase tracking-widest text-emerald-400/60">Ingresos</span>
            <span class="text-xl font-black italic tracking-tighter">{fmt(data.income)}</span>
        </div>

        <div class="glass-panel flex flex-col rounded-3xl border border-white/10 bg-white/5 p-4">
            <span class="text-[9px] font-black uppercase tracking-widest text-rose-400/60">Gastos</span>
            <span class="text-xl font-black italic tracking-tighter">{fmt(data.expense)}</span>
        </div>

        <div class="glass-panel col-span-2 flex flex-col rounded-3xl border border-white/10 bg-white/5 p-4 sm:col-span-1">
            <span class="text-[9px] font-black uppercase tracking-widest text-sky-400/60">Inversión</span>
            <span class="text-xl font-black italic tracking-tighter">{fmt(data.invest)}</span>
        </div>
    </div>

    <div class="glass-panel rounded-[32px] border border-white/10 bg-white/5 p-6">
        <div class="mb-4 flex items-end justify-between">
            <div>
                <h3 class="text-[10px] font-black uppercase tracking-widest opacity-40">Distribución Mensual</h3>
                <p class="text-2xl font-black italic tracking-tighter {data.savings >= 0 ? 'text-primary' : 'text-rose-500'}">
                    {data.savings >= 0 ? '+' : ''}{fmt(data.savings)}
                </p>
            </div>
            <div class="text-right">
                <span class="text-[8px] font-bold uppercase opacity-30">Ratio de Ahorro</span>
                <p class="text-sm font-black italic">
                    {data.income > 0 ? ((data.savings / data.income) * 100).toFixed(1) : 0}%
                </p>
            </div>
        </div>

        <div class="relative h-6 w-full overflow-hidden rounded-xl bg-white/5 p-1 flex gap-1">
            {#if data.expense > 0}
                <div class="h-full bg-rose-500/40 rounded-lg transition-all duration-1000" style="width: {expW}%"></div>
            {/if}
            {#if data.invest > 0}
                <div class="h-full bg-sky-500/40 rounded-lg transition-all duration-1000" style="width: {invW}%"></div>
            {/if}
            {#if data.savings > 0}
                <div class="h-full bg-primary rounded-lg transition-all duration-1000" style="width: {savW}%"></div>
            {/if}
        </div>

        <div class="mt-4 flex justify-between text-[8px] font-bold uppercase tracking-widest opacity-30">
            <span>Gastos</span>
            <span>Inversión</span>
            <span>Ahorro</span>
        </div>
    </div>
</div>

<style>
    .glass-panel {
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }
</style>