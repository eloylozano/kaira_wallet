<script lang="ts">
    import { onMount } from 'svelte';
    import { statsService } from '$lib/stores/domain/stats.svelte';
    import AssetMixPie from '../charts/AssetMixPie.svelte';
    import LiquidityPie from '../charts/LiquidityPie.svelte';
    import NetWorthChart from '../charts/NetWorthChart.svelte';

    const formatEuro = (val: number) =>
        val.toLocaleString('es-ES', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

    // Asegúrate de que summaryData sea reactivo en tu statsService
    const netWorth = $derived(
        (statsService.summaryData?.total_income ?? 0) - (statsService.summaryData?.total_expense ?? 0)
    );
    const totalInvested = $derived(statsService.summaryData?.total_invest ?? 0);
    const cashBalance = $derived(netWorth - totalInvested);

    onMount(() => {
        statsService.fetchEquityData();
    });
</script>

<div class="flex flex-col gap-6">
    <div class="grid grid-cols-3 gap-2 sm:gap-4">
        <div class="kaira-panel flex flex-col justify-center rounded-2xl p-3 sm:rounded-3xl sm:p-5">
            <span class="text-[8px] leading-tight font-black tracking-widest uppercase opacity-30 sm:text-[10px]">
                Patrimonio neto
            </span>
            <span class="truncate text-lg font-black tracking-tighter text-white sm:text-2xl">
                {formatEuro(netWorth)}<span class="ml-0.5 text-[10px] opacity-40">€</span>
            </span>
        </div>

        <div class="kaira-panel flex flex-col justify-center rounded-2xl border-l-2 border-sky-500/50 p-3 sm:rounded-3xl sm:border-l-4 sm:p-5">
            <span class="text-[8px] leading-tight font-black tracking-widest uppercase opacity-30 sm:text-[10px]">
                Inversión total
            </span>
            <span class="truncate text-lg font-black tracking-tighter text-sky-400 sm:text-2xl">
                {formatEuro(totalInvested)}<span class="ml-0.5 text-[10px] opacity-40">€</span>
            </span>
        </div>

        <div class="kaira-panel flex flex-col justify-center rounded-2xl border-l-2 border-emerald-500/50 p-3 sm:rounded-3xl sm:border-l-4 sm:p-5">
            <span class="text-[8px] leading-tight font-black tracking-widest uppercase opacity-30 sm:text-[10px]">
                Efectivo
            </span>
            <span class="truncate text-lg font-black tracking-tighter text-emerald-400 sm:text-2xl">
                {formatEuro(cashBalance)}<span class="ml-0.5 text-[10px] opacity-40">€</span>
            </span>
        </div>
    </div>

    <div class="kaira-panel rounded-[32px] p-6">
        <div class="mb-6">
            <h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Evolución de Riqueza</h2>
        </div>
        {#if !statsService.equityLoading}
            <div class="h-80 w-full">
                <NetWorthChart data={statsService.equityEvolution} />
            </div>
        {:else}
            <div class="h-80 w-full animate-pulse rounded-xl bg-white/5"></div>
        {/if}
    </div>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div class="kaira-panel rounded-[32px] p-6">
            <div class="mb-4">
                <h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Asset Mix</h2>
            </div>
            {#if !statsService.equityLoading}
                <div class="h-64 w-full">
                    <AssetMixPie data={statsService.assetTypes} />
                </div>
            {:else}
                <div class="h-64 w-full animate-pulse rounded-xl bg-white/5"></div>
            {/if}
        </div>

        <div class="kaira-panel rounded-[32px] p-6">
            <div class="mb-4">
                <h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Ratio de Liquidez</h2>
            </div>
            {#if !statsService.equityLoading}
                <div class="h-64 w-full">
                    <LiquidityPie invested={totalInvested} cash={cashBalance} />
                </div>
            {:else}
                <div class="h-64 w-full animate-pulse rounded-xl bg-white/5"></div>
            {/if}
        </div>
    </div>
</div>