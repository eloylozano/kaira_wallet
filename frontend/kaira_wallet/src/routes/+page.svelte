<script lang="ts">
	import HomeHeader from '$lib/components/home/HomeHeader.svelte';
	import BalanceCard from '$lib/components/home/BalanceCard.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { onMount } from 'svelte';

	import HomeChart from '$lib/components/charts/HomeChart.svelte';
	import RecentTransactions from '$lib/components/ui/RecentTransactions.svelte';
	import BudgetProgress from '$lib/components/ui/BudgetProgress.svelte';

	let monthlyBudget = 350;

	onMount(() => {
		transactionsStore.fetch({
			limit: 50,
			sort: 'desc'
		});
	});

	let thisMonthExpenses = $derived(() => {
		const now = new Date();
		const m = now.getMonth();
		const y = now.getFullYear();

		return transactionsStore.all.filter((t) => {
			const d = new Date(t.date);
			return t.type === 'expense' &&
				d.getMonth() === m &&
				d.getFullYear() === y;
		});
	});

	let spentThisMonth = $derived(() =>
		thisMonthExpenses().reduce((acc, t) => acc + Number(t.amount || 0), 0)
	);
</script>

<div class="mx-auto max-w-xl pb-24">
	<HomeHeader />
	<BalanceCard />
	<BudgetProgress
		budget={monthlyBudget}
		spent={spentThisMonth()}
	/>

	<HomeChart />


	<RecentTransactions />
</div>