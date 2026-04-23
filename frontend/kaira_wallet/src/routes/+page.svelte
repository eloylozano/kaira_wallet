<script lang="ts">
	import HomeHeader from '$lib/components/home/HomeHeader.svelte';
	import BalanceCard from '$lib/components/home/BalanceCard.svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import FilterBar from '$lib/components/ui/FilterBar.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import TransactionItem from '$lib/components/ui/TransactionItem.svelte';

	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { goto } from '$app/navigation';

	type PaidFilter = boolean | '';

	let search = $state('');
	let type = $state('');
	let isPaid = $state<PaidFilter>('');
	let sort = $state<'desc' | 'asc'>('desc');
	let page = $state(0);

	const limit = 20;

	// reset page cuando filtros cambian
	$effect(() => {
		search;
		type;
		isPaid;
		page = 0;
	});

	// fetch transacciones (para balance + home data)
	$effect(() => {
		page;
		type;
		isPaid;
		search;
		sort;

		transactionsStore.fetch({
			transaction_type: type || undefined,
			is_paid: isPaid === '' ? undefined : isPaid,
			search: search || undefined,
			skip: page * limit,
			limit,
			sort
		});
	});

	// 🧠 últimos 5 movimientos (HOME STYLE)
	let lastFive = $derived(() => {
		const list = [...transactionsStore.all];

		list.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

		return list.slice(0, 5);
	});
</script>

<div class="mx-auto max-w-xl pb-24">
	<!-- HEADER + BALANCE -->
	<HomeHeader />
	<BalanceCard />

	<!-- 🟢 ÚLTIMOS MOVIMIENTOS -->
	<div class="mt-8">
		<div class="mb-3 flex items-center justify-between">
			<h2 class="text-[10px] font-black tracking-widest uppercase opacity-60">
				Últimos movimientos
			</h2>

			<button
				onclick={() => goto('/transactions')}
				class="kaira-chip flex-none rounded-xl px-4 py-2 text-[10px] font-bold uppercase
		transition-all hover:opacity-80 active:scale-95"
			>
				Ver todo
			</button>
		</div>

		<div class="space-y-3">
			{#each lastFive() as tx (tx.id)}
				<button
					onclick={() => goto(`/transactions/${tx.id}`)}
					class="w-full text-left transition-transform active:scale-[0.98]"
				>
					<TransactionItem {tx} />
				</button>
			{/each}
		</div>
	</div>
</div>
