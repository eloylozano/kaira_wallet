<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import CategoryList from './CategoryList.svelte';
	import CategoryModal from './CategoryModal.svelte';

	let isOpen = $state(false);
	let editing = $state(null);

	function openCreate() {
		editing = null;
		isOpen = true;
	}

	function openEdit(cat) {
		editing = cat;
		isOpen = true;
	}
</script>

<div class="mx-auto max-w-xl space-y-6 p-4">

	<header class="ios-header">
		<h1 class="text-3xl font-black uppercase italic">Categorías</h1>

		<button
			onclick={openCreate}
			class="mt-3 rounded-2xl bg-primary px-4 py-2 text-sm font-black text-white"
		>
			+ Nueva categoría
		</button>
	</header>

	<CategoryList
		items={categoriesStore.all}
		onEdit={openEdit}
	/>

</div>

{#if isOpen}
	<CategoryModal
		editing={editing}
		onClose={() => (isOpen = false)}
	/>
{/if}