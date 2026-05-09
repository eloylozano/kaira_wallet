<script lang="ts">
	import CategoryItem from './CategoryItem.svelte';

	let { items = [], onEdit } = $props();
</script>

<div class="space-y-3">

	{#each items as cat}

		<!-- PADRE -->
		<CategoryItem {cat} {onEdit} />

		<!-- HIJOS -->
		{#if cat.subcategories?.length}
			<div class="ml-5 mt-2 space-y-2 border-l border-white/10 pl-3">

				{#each cat.subcategories as sub}
					<CategoryItem cat={sub} {onEdit} isChild={true} />
				{/each}

			</div>
		{/if}

	{/each}

</div>