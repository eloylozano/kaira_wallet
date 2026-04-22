<script lang="ts">
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import FilterBar from '$lib/components/ui/FilterBar.svelte';
	import SortBar from '$lib/components/ui/SortBar.svelte';
	import TransactionItem from '$lib/components/ui/TransactionItem.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { groupByMonth } from '$lib/utils/groupByMonth';

	let search = $state('');
	let type = $state(''); // expense | income | invest
	let isPaid = $state<boolean | ''>('');
	let sort = $state<'desc' | 'asc'>('desc');

	let grouped = $derived.by(() => {
		let list = [...transactionsStore.all];

		// SEARCH
		if (search) {
			const q = search.toLowerCase();

			list = list.filter((tx) => {
				return (
					tx.description?.toLowerCase().includes(q) ||
					tx.category?.name?.toLowerCase().includes(q)
				);
			});
		}

		// SORT
		list.sort((a, b) => {
			const aTime = new Date(a.date).getTime();
			const bTime = new Date(b.date).getTime();
			return sort === 'desc' ? bTime - aTime : aTime - bTime;
		});

		return groupByMonth(list);
	});

	// FETCH REACTIVO (ÚNICO)
	$effect(() => {
		transactionsStore.fetch({
			transaction_type: type || undefined,
			is_paid: isPaid === '' ? undefined : isPaid
		});
	});
</script>

<div class="mx-auto max-w-xl space-y-8 p-4 pb-24">
	<h1 class="h1-kaira">Movimientos</h1>

	<SearchBar bind:search />

	<div class="space-y-6 rounded-3xl bg-white/[0.02] p-2 border border-white/[0.05]">
		<FilterBar bind:type bind:isPaid />
		<SortBar bind:sort />
	</div>

	{#each Object.entries(grouped) as [month, items]}
		<section class="space-y-4">
			<h2 class="text-[11px] font-black uppercase opacity-60">
				{month}
			</h2>

			{#each items as tx (tx.id)}
				<TransactionItem {tx} />
			{/each}
		</section>
	{/each}
</div>