<script lang="ts">
	import { onMount } from 'svelte';
	import FilterBar from '$lib/components/ui/FilterBar.svelte';
	import SortBar from '$lib/components/ui/SortBar.svelte';
	import TransactionItem from '$lib/components/ui/TransactionItem.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { groupByMonth } from '$lib/utils/groupByMonth';

	let type = $state('');
	let isPaid = $state('');
	let sort = $state<'desc' | 'asc'>('desc');

	let grouped = $state<Record<string, any[]>>({});

	async function load() {
		await transactionsStore.fetch({
			type: type || undefined,
			is_paid: isPaid === '' ? undefined : isPaid
		});
	}

	onMount(() => {
		load();
	});

	// 🔥 REACTIVO REAL
	$effect(() => {
		const sorted = [...transactionsStore.all].sort((a, b) => {
			const tA = new Date(a.date).getTime();
			const tB = new Date(b.date).getTime();

			return sort === 'desc' ? tB - tA : tA - tB;
		});

		grouped = groupByMonth(sorted);
	});
</script>

<div class="mx-auto max-w-xl space-y-6 p-4">
	<header>
		<h1 class="h1-kaira">Últimos Movimientos</h1>
	</header>

	<FilterBar bind:type bind:isPaid />
	<SortBar bind:sort />

	{#each Object.entries(grouped) as [month, items]}
		<div class="space-y-3">
			<h2 class="text-sm font-black uppercase opacity-60">
				{month}
			</h2>

			{#each items as tx}
				<TransactionItem {tx} />
			{/each}
		</div>
	{/each}
</div>