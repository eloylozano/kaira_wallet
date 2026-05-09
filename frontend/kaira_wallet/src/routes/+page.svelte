<script lang="ts">
    import HomeHeader from '$lib/components/dashboard/HomeHeader.svelte';
    import BalanceCard from '$lib/components/dashboard/BalanceCard.svelte';
    import HomeChart from '$lib/components/stats/charts/HomeChart.svelte';
    import BudgetProgress from '$lib/components/dashboard/BudgetProgress.svelte';
    import TransactionItem from '$lib/components/transactions/TransactionItem.svelte';
    
    import { transactionsStore } from '$lib/stores/domain/transactions.svelte';
    import { statsService } from '$lib/stores/domain/stats.svelte';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let monthlyBudget = 350;

    // Cargamos datos al montar el componente
    onMount(() => {
        // Pedimos los últimos movimientos para la lista
        transactionsStore.fetch({
            limit: 50,
            sort: 'desc'
        });
        
        // Sincronizamos el mes actual en el servicio de stats
        const now = new Date();
        statsService.selectedMonth = now.getMonth();
        statsService.selectedYear = now.getFullYear();
        statsService.fetchMonthlyStats();
    });

    let lastFive = $derived(transactionsStore.all.slice(0, 5));
</script>

<div class="mx-auto max-w-xl pb-24">
    <HomeHeader />
    <BalanceCard />
    
    <BudgetProgress
        budget={monthlyBudget}
        spent={statsService.monthlyStatsData.expense}
    />

    <HomeChart />

    <div class="mt-8">
        <div class="mb-3 flex items-center justify-between">
            <h2 class="text-[10px] font-black tracking-widest uppercase opacity-60">
                Últimos movimientos
            </h2>
            <button
                onclick={() => goto('/transactions')}
                class="kaira-chip rounded-xl px-4 py-2 text-[10px] font-bold uppercase transition-all hover:opacity-80 active:scale-95"
            >
                Ver todo
            </button>
        </div>

        <div class="space-y-3">
            {#each lastFive as tx (tx.id)}
                <button
                    onclick={() => goto(`/transactions/${tx.id}`)}
                    class="w-full text-left transition-transform active:scale-[0.98]"
                >
                    <TransactionItem {tx} />
                </button>
            {:else}
                <p class="py-4 text-center text-[10px] uppercase opacity-30">Cargando movimientos...</p>
            {/each}
        </div>
    </div>
</div>