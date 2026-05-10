<script lang="ts">
    import { onMount } from 'svelte';
    import { statsService } from '$lib/stores/domain/stats.svelte';
    import { investmentStore } from '$lib/stores/domain/investments.svelte';
    import GlassCard from '$lib/components/ui/core/GlassCard.svelte';
    import FreedomChart from '../charts/FreedomChart.svelte';

    const target = $derived(investmentStore.targetSavings);
    const data = $derived(statsService.projectionData);

    // Cálculos de porcentaje
    const currentPercent = $derived(target > 0 ? (data.current_balance / target) * 100 : 0);
    const projectedPercent = $derived(target > 0 ? (data.projected_december / target) * 100 : 0);

    // --- CÁLCULOS PREDICTIVOS ---
    const remainingAmount = $derived(Math.max(0, target - data.current_balance));

    // Meses restantes al ritmo actual
    const monthsToTarget = $derived(
        data.avg_monthly_savings > 0 ? Math.ceil(remainingAmount / data.avg_monthly_savings) : null
    );

    // Ahorro necesario para llegar a fin de año (Diciembre)
    const requiredMonthlyForYearEnd = $derived(
        data.months_left > 0 ? Math.max(0, (target - data.current_balance) / data.months_left) : 0
    );

    // Esfuerzo extra necesario sobre la media actual
    const extraEffortNeeded = $derived(
        Math.max(0, requiredMonthlyForYearEnd - data.avg_monthly_savings)
    );

    onMount(async () => {
        await statsService.fetchFreedomProjection();
    });
</script>

<div class="space-y-6">
    <header class="flex flex-col gap-1 px-2">
        <span class="text-[10px] font-black tracking-[0.3em] text-emerald-400 uppercase">Estrategia Kaira</span>
        <h2 class="text-2xl font-bold tracking-tighter text-white italic">Libertad Financiera</h2>
    </header>

    <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
        <GlassCard class="!rounded-[32px] border-white/5 bg-white/[0.02]">
            <FreedomChart title="Estado Actual" value={data.current_balance} {target} />
            <div class="px-6 pb-6 text-center">
                <span class="text-[10px] font-bold tracking-widest text-white/30 uppercase">
                    {currentPercent.toFixed(1)}% Alcanzado
                </span>
            </div>
        </GlassCard>

        <GlassCard class="!rounded-[32px] border-emerald-500/10 bg-emerald-500/[0.03]">
            <FreedomChart title="Objetivo 31 Dic" value={data.projected_december} {target} />
            <div class="px-6 pb-6 text-center">
                <span class="text-[10px] font-bold tracking-widest text-emerald-400/60 uppercase">
                    {projectedPercent.toFixed(1)}% Proyectado
                </span>
            </div>
        </GlassCard>
    </div>

    <div class="space-y-4">
        <GlassCard class="!rounded-[28px] border-white/5 p-6">
            <div class="flex items-center justify-between gap-4">
                <div>
                    <p class="mb-1 text-[9px] font-black tracking-widest text-white/30 uppercase">
                        Ahorro Neto Mensual (Media Real YTD)
                    </p>
                    <p class="text-2xl font-bold tracking-tight text-white">
                        {data.avg_monthly_savings.toLocaleString('es-ES')}€
                        <span class="text-sm font-normal text-white/50">/mes</span>
                    </p>
                    <p class="mt-1 text-[10px] text-white/40 italic">* Basado en datos reales desde Enero</p>
                </div>
                <div class="flex-shrink-0 text-right">
                    <p class="mb-1 text-[9px] font-black tracking-widest text-amber-300 uppercase">
                        Faltan para la meta
                    </p>
                    <p class="text-xl font-bold tracking-tight text-amber-300">
                        {remainingAmount.toLocaleString('es-ES')}€
                    </p>
                </div>
            </div>
        </GlassCard>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <GlassCard class="!rounded-[28px] border-white/5 bg-white/[0.01] p-6">
                <div class="mb-4 text-left">
                    <h3 class="mb-1 text-[9px] font-black tracking-widest text-white/30 uppercase">
                        Estimación Temporal
                    </h3>
                </div>

                <div>
                    <p class="text-3xl font-bold tracking-tighter text-white">
                        {#if monthsToTarget !== null}
                            {monthsToTarget}
                            <span class="text-sm font-medium tracking-normal text-white/30 ">meses</span>
                        {:else}
                            ---
                        {/if}
                    </p>
                    <p class="mt-2 text-[10px] font-medium tracking-tight text-white/40 ">
                        Al ritmo de ahorro actual
                    </p>
                </div>
            </GlassCard>

            <GlassCard class="!rounded-[28px] border-white/10 bg-white/[0.02] p-6">
                <div class="mb-4 text-left">
                    <h3 class="mb-1 text-[9px] font-black tracking-widest text-white/30 uppercase">
                        Objetivo Sugerido
                    </h3>
                </div>

                <div>
                    <p class="text-3xl font-bold tracking-tighter text-white">
                        {requiredMonthlyForYearEnd.toLocaleString('es-ES', { maximumFractionDigits: 0 })}€<span
                            class="text-sm font-medium tracking-normal  opacity-40">/mes</span
                        >
                    </p>
                    <p class="mt-2 text-[10px] font-medium tracking-tight text-white/40 ">
                        Esfuerzo extra: +{extraEffortNeeded.toLocaleString('es-ES', {
                            maximumFractionDigits: 0
                        })}€
                    </p>
                </div>
            </GlassCard>
        </div>
    </div>
</div>