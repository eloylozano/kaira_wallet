<script lang="ts">
	import { onMount } from 'svelte';
	import SavingsCircle from '$lib/components/charts/SavingsCircle.svelte';
	import GlassSelector from '$lib/components/ui/core/GlassSelector.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import DailyBudgetCard from '$lib/components/charts/DailyBudgetCard.svelte';
	import { statsService } from '$lib/stores/stats.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import RemainingDaysCard from '$lib/components/charts/RemainingDaysCard.svelte';
	import YearlyFlowChart from '$lib/components/charts/YearlyFlowChart.svelte';

	let selectedTab = $state('mes');

	const tabOptions = [
		{ value: 'mes', label: 'Mes' },
		{ value: 'distribucion', label: 'Distribución' },
		{ value: 'patrimonio', label: 'Patrimonio' },
		{ value: 'libertad', label: 'Libertad' }
	];



	$effect(() => {
		statsService.fetchMonthlyStats();
	});
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 pt-10 pb-32">
	<header class="flex flex-col gap-4">
		<div class="flex flex-col">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
				<!-- TITULO -->
				<div class="flex min-w-0 flex-col">
					<h1 class="h1-kaira text-3xl leading-tight sm:text-4xl">Stats</h1>
					<p class="text-[10px] font-bold tracking-[0.2em] uppercase opacity-30">
						Análisis de rendimiento
					</p>
				</div>

				<!-- SELECTORS -->
				<div class="flex w-full gap-2 sm:w-auto sm:min-w-[260px]">
					<div class="min-w-0 flex-1">
						<GlassSelector
							bind:value={statsService.selectedMonth}
							options={statsService.availableMonths}
						/>
					</div>

					<div class="min-w-0 flex-1">
						<GlassSelector
							bind:value={statsService.selectedYear}
							options={statsService.availableYears}
						/>
					</div>
				</div>
			</div>
		</div>

		<SegmentedControl bind:selected={selectedTab} options={tabOptions} />
	</header>

	{#if selectedTab === 'mes'}
		<SavingsCircle
			percent={statsService.monthlyStatsData.savings_percent}
			amount={statsService.monthlyStatsData.savings_amount}
		/>

		<div class="space-y-6">
			<div class="grid grid-cols-2 gap-4">
				<DailyBudgetCard />

				<RemainingDaysCard />
			</div>

			<YearlyFlowChart />
		</div>
	{:else if selectedTab === 'dist'}
		<div class="space-y-4">
			<div
				class="glass-panel flex h-64 items-center justify-center rounded-[32px] border border-white/10 bg-white/5"
			>
				<p class="text-xs font-black tracking-widest uppercase opacity-20">
					Pareto Categorías (Chart)
				</p>
			</div>
			<div class="grid grid-cols-1 gap-2">
				{#each ['Vivienda', 'Comida', 'Ocio'] as cat}
					<div
						class="flex items-center justify-between rounded-2xl border border-white/5 bg-white/5 px-6 py-4"
					>
						<span class="text-sm font-bold">{cat}</span>
						<span class="text-sm font-black italic">{(Math.random() * 500).toFixed(0)}€</span>
					</div>
				{/each}
			</div>
		</div>
	{:else if selectedTab === 'patri'}
		<div class="space-y-6">
			<div class="text-center">
				<p class="text-[10px] font-black tracking-widest uppercase opacity-40">Patrimonio Total</p>
				<h2 class="text-5xl font-black tracking-tighter italic">42.500€</h2>
				<p class="mt-1 text-xs font-bold text-primary">+1.2% este mes</p>
			</div>
			<div
				class="glass-panel flex h-64 items-center justify-center rounded-[32px] border border-white/10 bg-white/10"
			>
				<p class="text-xs font-black tracking-widest uppercase opacity-20">
					Evolución Histórica (Area Chart)
				</p>
			</div>
		</div>
	{:else if selectedTab === 'libertad'}
		<div class="space-y-8 py-4">
			<div class="flex justify-around">
				<div class="flex flex-col items-center gap-3">
					<div
						class="flex h-32 w-32 items-center justify-center rounded-full border-8 border-primary/20 border-t-primary"
					>
						<span class="text-2xl font-black italic">1.2</span>
					</div>
					<p class="text-[9px] font-black tracking-widest uppercase opacity-40">Años cubiertos</p>
				</div>
				<div class="flex flex-col items-center gap-3">
					<div
						class="flex h-32 w-32 items-center justify-center rounded-full border-8 border-white/5 border-t-amber-400"
					>
						<span class="text-2xl font-black italic">65%</span>
					</div>
					<p class="text-[9px] font-black tracking-widest uppercase opacity-40">Independencia</p>
				</div>
			</div>
			<div class="glass-panel rounded-[32px] border border-white/10 bg-primary/5 p-6 text-center">
				<p class="text-[10px] font-black tracking-widest uppercase opacity-50">Previsión a 31/12</p>
				<p class="mt-1 text-3xl font-black text-primary italic">48.200€</p>
				<p class="mt-2 text-[10px] opacity-40">Siguiendo tu ritmo de ahorro actual</p>
			</div>
		</div>
	{/if}
</div>

<style>
	/* Animación básica para que el cambio de pestaña no sea brusco */
	.glass-panel {
		backdrop-filter: blur(12px);
		-webkit-backdrop-filter: blur(12px);
	}
</style>
