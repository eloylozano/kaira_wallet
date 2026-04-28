<script lang="ts">
	import { statsService } from '$lib/stores/stats.svelte';

	import SavingsCircle from '../charts/SavingsCircle.svelte';
	import DailyBudgetCard from '../charts/DailyBudgetCard.svelte';
	import RemainingDaysCard from '../charts/RemainingDaysCard.svelte';
	import YearlyFlowChart from '../charts/YearlyFlowChart.svelte';
	import FixedRatio from '../charts/FixedRatio.svelte';
	import MonthlyBoxChart from '../charts/MonthlyBoxChart.svelte';
</script>

<div class="space-y-6">
	<MonthlyBoxChart />

	<SavingsCircle
		amount={statsService.monthlyStatsData.savings + statsService.monthlyStatsData.invest}
		percent={statsService.monthlyStatsData.income > 0
			? ((statsService.monthlyStatsData.savings + statsService.monthlyStatsData.invest) /
					statsService.monthlyStatsData.income) *
				100
			: 0}
	/>
	<div class="grid grid-cols-2 gap-4">
		<DailyBudgetCard />
		<RemainingDaysCard />
	</div>

	<FixedRatio />

	<YearlyFlowChart />
</div>
