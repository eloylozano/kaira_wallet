<script lang="ts">
	import SearchBar from '$lib/components/ui/SearchBar.svelte';
	import FilterBar from '$lib/components/ui/FilterBar.svelte';
	import SortBar from '$lib/components/ui/SortBar.svelte';
	import TransactionItem from '$lib/components/ui/TransactionItem.svelte';
	import PaginationBar from '$lib/components/ui/PaginationBar.svelte';

	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { groupByMonth } from '$lib/utils/groupByMonth';

	let search = $state('');
	let type = $state('');
	let isPaid = $state<boolean | ''>('');
	let sort = $state<'desc' | 'asc'>('desc');

	let page = $state(0);
	const limit = 20;

	$effect(() => {
		type;
		isPaid;
		search;

		page = 0;
	});

	$effect(() => {
		page;
		type;
		isPaid;

		const skip = page * limit;

		transactionsStore.fetch({
			transaction_type: type || undefined,
			is_paid: isPaid === '' ? undefined : isPaid,
			skip,
			limit
		});
	});

	let grouped = $derived.by(() => {
		let list = [...transactionsStore.all];

		// SEARCH
		if (search) {
			const q = search.toLowerCase();

			list = list.filter((tx) => {
				return (
					tx.description?.toLowerCase().includes(q) || tx.category?.name?.toLowerCase().includes(q)
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

	let hasMore = $derived((page + 1) * limit < transactionsStore.total);

	function nextPage() {
		if (hasMore) page += 1;
	}

	function prevPage() {
		if (page > 0) page -= 1;
	}
</script>

<div class="mx-auto max-w-xl space-y-8">
	<h1 class="h1-kaira">Movimientos</h1>

	<SearchBar bind:search />

	<div class="space-y-3 rounded-3xl border border-white/5 bg-transparent p-2">
		<FilterBar bind:type bind:isPaid />
		<SortBar bind:sort />
	</div>

	{#each Object.entries(grouped) as [month, items]}
		<section class="space-y-4">
			<h2 class="text-[11px] font-black uppercase opacity-60">
				{month}
			</h2>

			{#each items as tx (tx.id)}
				<a href="/transactions/{tx.id}" class="block transition-transform active:scale-95">
					<TransactionItem {tx} />
				</a>
			{/each}
		</section>
	{/each}

	<PaginationBar {page} onNext={nextPage} onPrev={prevPage} />
</div>
