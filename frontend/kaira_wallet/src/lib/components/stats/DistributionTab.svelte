<script lang="ts">
	import ParetoChart from '../charts/ParetoChart.svelte';
	import CategoryPieChart from '../charts/CategoryPieChart.svelte';
	import CashRatioChart from '../charts/CashRatioChart.svelte';
	import InvestmentMixChart from '../charts/InvestmentMixChart.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import { statsService } from '$lib/stores/stats.svelte';
	import { onMount } from 'svelte';

	let subView = $state('gastos'); // 'gastos' | 'inversiones'

	const distributionOptions = [
		{ value: 'gastos', label: 'Gastos' },
		{ value: 'inversiones', label: 'Inversiones' }
	];

	onMount(() => {
		statsService.fetchDistributionData();
	});

	// Reaccionar si el usuario cambia el año/mes en el header
	$effect(() => {
		// Accedemos a las dependencias para que el effect se dispare al cambiar
		statsService.selectedYear;
		statsService.selectedMonth;
		statsService.fetchDistributionData();
	});
</script>

<div class="space-y-8">
	<SegmentedControl bind:selected={subView} options={distributionOptions} />

	{#if subView === 'gastos'}
		<div class="animate-in fade-in slide-in-from-bottom-2 space-y-8 duration-500">
			<section>
				
				<CategoryPieChart />
			</section>

			<section>
				<ParetoChart />
			</section>
		</div>
	{:else}
		<div class="animate-in fade-in slide-in-from-bottom-2 space-y-8 duration-500">
			<section>
				<h2 class="mb-4 px-4 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
					Liquidez vs Inversión
				</h2>
				<CashRatioChart />
			</section>

			<section>
				<h2 class="mb-4 px-4 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
					Asset Allocation
				</h2>
				<InvestmentMixChart />
			</section>
		</div>
	{/if}
</div>
