<script lang="ts">
	import { onMount } from 'svelte';
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import CategoryList from '$lib/components/ui/categories/CategoryList.svelte';
	import CategoryModal from '$lib/components/ui/categories/CategoryModal.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';

	let isOpen = $state(false);
	let editing = $state(null);

	let filter = $state<'all' | 'income' | 'expense' | 'invest'>('all');

	onMount(() => {
		categoriesStore.refresh();
	});

	function openCreate() {
		editing = null;
		isOpen = true;
	}

	function openEdit(cat) {
		editing = cat;
		isOpen = true;
	}

	function closeModal() {
		isOpen = false;
		editing = null;
	}

	let filteredCategories = $derived.by(() => {
		const items = categoriesStore.all ?? [];
		if (!Array.isArray(items)) return [];

		let result = items;
		if (filter !== 'all') {
			result = result.filter((c) => c.transaction_type === filter);
		}
		return [...result].sort((a, b) => a.name.localeCompare(b.name));
	});
</script>

<div class="mx-auto max-w-xl space-y-6">
	<header class="ios-header">
		<h1 class="text-3xl font-black uppercase italic">Categorías</h1>

		<button
			onclick={openCreate}
			class="mt-3 rounded-2xl bg-primary px-4 py-2 text-sm font-black text-white"
		>
			+ Nueva categoría
		</button>
	</header>

	<SegmentedControl
		bind:selected={filter}
		options={[
			{ value: 'all', label: 'Todo' },
			{ value: 'income', label: 'Ingresos', color: '#10b981' },
			{ value: 'invest', label: 'Inversión', color: '#3b82f6' },
			{ value: 'expense', label: 'Gastos', color: '#ef4444' }
		]}
	/>

	<CategoryList items={filteredCategories} onEdit={openEdit} />
</div>

{#if isOpen}
	<CategoryModal {editing} onClose={closeModal} />
{/if}
