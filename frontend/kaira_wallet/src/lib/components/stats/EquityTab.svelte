<script lang="ts">
	import { onMount } from 'svelte';
	import { statsService } from '$lib/stores/stats.svelte';
	import AssetMixPie from '../charts/AssetMixPie.svelte';
	import LiquidityPie from '../charts/LiquidityPie.svelte';
	import NetWorthChart from '../charts/NetWorthChart.svelte';

	// Helper de formato para asegurar consistencia en todo el archivo
	const formatEuro = (val: number) => 
		val.toLocaleString('es-ES', { 
			minimumFractionDigits: 2, 
			maximumFractionDigits: 2 
		});

	// Cálculos derivados
	const netWorth = $derived(statsService.summaryData.total_income - statsService.summaryData.total_expense);
	const totalInvested = $derived(statsService.summaryData.total_invest);
	const cashBalance = $derived(netWorth - totalInvested);

	onMount(() => {
		statsService.fetchEquityData();
	});
</script>

<div class="flex flex-col gap-6 py-6">
	<div class="flex gap-4">
		<div class="kaira-panel flex w-full flex-col justify-center rounded-3xl p-5">
			<span class="text-[10px] font-black tracking-widest uppercase opacity-30">Patrimonio Neto</span>
			<span class="text-2xl font-black tracking-tighter text-white">
				{formatEuro(netWorth)}<span class="ml-1 text-sm opacity-40">€</span>
			</span>
		</div>
		
		<div class="kaira-panel flex w-full flex-col justify-center rounded-3xl border-l-4 border-sky-500/50 p-5">
			<span class="text-[10px] font-black tracking-widest uppercase opacity-30">Inversión Total</span>
			<span class="text-2xl font-black tracking-tighter text-sky-400">
				{formatEuro(totalInvested)}<span class="ml-1 text-sm opacity-40">€</span>
			</span>
		</div>
		
		<div class="kaira-panel flex w-full flex-col justify-center rounded-3xl border-l-4 border-emerald-500/50 p-5">
			<span class="text-[10px] font-black tracking-widest uppercase opacity-30">Efectivo (2% TAE)</span>
			<span class="text-2xl font-black tracking-tighter text-emerald-400">
				{formatEuro(cashBalance)}<span class="ml-1 text-sm opacity-40">€</span>
			</span>
		</div>
	</div>

	<div class="kaira-panel rounded-[32px] p-6">
		<div class="mb-6">
			<h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Evolución de Riqueza</h2>
		</div>
		{#if !statsService.equityLoading}
			<NetWorthChart data={statsService.equityEvolution} />
		{:else}
			<div class="h-80 w-full animate-pulse rounded-xl bg-white/5"></div>
		{/if}
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
		<div class="kaira-panel rounded-[32px] p-6">
			<div class="mb-4">
				<h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Ratio de Liquidez</h2>
				<p class="text-xs font-bold text-white/80 italic">Cash vs. Inversión</p>
			</div>
			<LiquidityPie invested={totalInvested} cash={cashBalance} />
		</div>
		
		<div class="kaira-panel rounded-[32px] p-6">
			<div class="mb-4">
				<h2 class="text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Asset Mix</h2>
				<p class="text-xs font-bold text-white/80 italic">Diversificación por tipo</p>
			</div>
			{#if !statsService.equityLoading}
				<AssetMixPie data={statsService.assetTypes} />
			{:else}
				<div class="h-64 w-full animate-pulse rounded-xl bg-white/5"></div>
			{/if}
		</div>
	</div>
</div>