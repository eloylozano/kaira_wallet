<script lang="ts">
    import HomeHeader from '$lib/components/home/HomeHeader.svelte';
    import BalanceCard from '$lib/components/home/BalanceCard.svelte';
    import { transactionsStore } from '$lib/stores/transactions.svelte';
    import { onMount } from 'svelte';
	import HomeChart from '$lib/components/charts/HomeChart.svelte';
	import RecentTransactions from '$lib/components/ui/RecentTransactions.svelte';

    // Solo pedimos las últimas transacciones al montar
    onMount(() => {
        transactionsStore.fetch({
            limit: 10,
            sort: 'desc'
        });
    });
</script>

<div class="mx-auto max-w-xl pb-24">
    <HomeHeader />
    <BalanceCard />
    
    <HomeChart />
    
    <RecentTransactions />
</div>