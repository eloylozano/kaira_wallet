<script lang="ts">
	import FilterBar from '$lib/components/transactions/controls/FilterBar.svelte';
	import PaginationBar from '$lib/components/transactions/controls/PaginationBar.svelte';
	import SearchBar from '$lib/components/transactions/controls/SearchBar.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import TransactionItem from '$lib/components/transactions/TransactionItem.svelte';
	import { transactionsStore } from '$lib/stores/domain/transactions.svelte';
	import { groupByMonth } from '$lib/utils/date/groupByMonth';

	let search = $state('');
	let type = $state('');
	let isPaid = $state<'' | 'true' | 'false'>('');
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
		search;

		const skip = page * limit;

		transactionsStore.fetch({
			transaction_type: type || undefined,
			is_paid: isPaid === '' ? undefined : isPaid === 'true',
			search: search || undefined, // 👈 AQUÍ
			skip,
			limit,
			sort
		});
	});
	let grouped = $derived.by(() => {
		let list = [...transactionsStore.all];

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
		<SegmentedControl
			bind:selected={sort}
			options={[
				{ value: 'desc', label: 'Recientes' },
				{ value: 'asc', label: 'Antiguos' }
			]}
		/>
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
