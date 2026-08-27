<script lang="ts">
	import BalanceCard from '$lib/components/dashboard/BalanceCard.svelte';
	import HomeChart from '$lib/components/stats/charts/HomeChart.svelte';
	import BudgetProgress from '$lib/components/dashboard/BudgetProgress.svelte';
	import TransactionItem from '$lib/components/transactions/TransactionItem.svelte';

	import { transactionsStore } from '$lib/stores/domain/transactions.svelte';
	import { statsService } from '$lib/stores/domain/stats.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';

	let loading = $state(true);
	let accountName = $state('Kaira Wallet');
	let accountDescription = $state('Kaira Wallet');

	function loadActiveAccountData() {
		if (browser) {
			try {
				const raw = localStorage.getItem('kaira_active_account');
				if (raw) {
					const parsed = JSON.parse(raw);
					if (parsed?.name) {
						accountName = parsed.name;
					}
					if (parsed?.description) {
						accountDescription = parsed.description;
					}
				}
			} catch (e) {
				console.error('Error leyendo la cuenta activa', e);
			}
		}
	}

	onMount(async () => {
		loadActiveAccountData();

		try {
			await transactionsStore.fetch({
				limit: 50,
				sort: 'desc'
			});
		} finally {
			loading = false;
		}

		const now = new Date();
		statsService.selectedMonth = now.getMonth();
		statsService.selectedYear = now.getFullYear();
		statsService.fetchMonthlyStats();
	});

	let lastFive = $derived(transactionsStore.all.slice(0, 5));
</script>

<div class="mx-auto max-w-xl pb-24">
	<header class="flex items-end justify-between pt-8">
		<div>
			<p class="text-[10px] font-black tracking-[0.2em] text-primary/70 uppercase">
				{accountDescription}
			</p>
			<h1 class="text-3xl font-black tracking-tighter uppercase italic">Hola, {accountName}</h1>
		</div>
	</header>

	<div class="isolate transform-gpu [backface-visibility:hidden] [perspective:1000px]">
		<BalanceCard />
	</div>

	<BudgetProgress />

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
				<p class="py-4 text-center text-[10px] uppercase opacity-30">
					{loading ? 'Cargando movimientos...' : 'No hay movimientos registrados'}
				</p>
			{/each}
		</div>
	</div>
</div>