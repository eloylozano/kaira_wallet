<script lang="ts">
	import CategoryItem from './CategoryItem.svelte';

	let { items = [], onEdit } = $props();
</script>

<div class="space-y-3">
	{#each items as cat (cat.id)}
		<CategoryItem {cat} {onEdit} />
	{/each}
</div>