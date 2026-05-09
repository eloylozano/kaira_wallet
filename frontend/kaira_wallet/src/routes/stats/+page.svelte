<script lang="ts">
	import GlassSelector from '$lib/components/ui/core/GlassSelector.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import { statsService } from '$lib/stores/stats.svelte';

	// Importación de los nuevos componentes de pestaña
	import MonthlyTab from '$lib/components/stats/MonthlyTab.svelte';
	import DistributionTab from '$lib/components/stats/DistributionTab.svelte';
	import FreedomTab from '$lib/components/stats/FreedomTab.svelte';
	import EquityTab from '$lib/components/stats/EquityTab.svelte';

	let selectedTab = $state('mes');

	const tabOptions = [
		{ value: 'mes', label: 'Mes' },
		{ value: 'distribucion', label: 'Distribución' },
		{ value: 'patrimonio', label: 'Patrimonio' },
		{ value: 'libertad', label: 'Libertad' }
	];

	$effect(() => {
		statsService.fetchMonthlyStats();
		statsService.fetchDistributionData();
	});
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 pt-10 pb-24">
	<header class="flex flex-col gap-4">
		<div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
			<div class="flex min-w-0 flex-col">
				<h1 class="text-3xl leading-tight font-black italic sm:text-4xl">Stats</h1>
				<p class="text-[10px] font-bold tracking-[0.2em] uppercase opacity-30">
					Análisis de rendimiento
				</p>
			</div>

			<div class="flex w-full gap-2 sm:w-auto">
				<GlassSelector
					bind:value={statsService.selectedMonth}
					options={statsService.availableMonths}
				/>
				<GlassSelector
					bind:value={statsService.selectedYear}
					options={statsService.availableYears}
				/>
			</div>
		</div>

		<SegmentedControl bind:selected={selectedTab} options={tabOptions} />
	</header>

	<div class="transition-all duration-300">
		{#if selectedTab === 'mes'}
			<MonthlyTab />
		{:else if selectedTab === 'distribucion'}
			<DistributionTab />
		{:else if selectedTab === 'patrimonio'}
			<EquityTab />
		{:else if selectedTab === 'libertad'}
			<FreedomTab />
		{/if}
	</div>
</div>
