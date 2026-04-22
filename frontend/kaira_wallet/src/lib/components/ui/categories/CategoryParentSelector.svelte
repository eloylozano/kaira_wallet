<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';

	let { selected = $bindable<number | null>(null) } = $props();

	const parents = $derived(
		categoriesStore.all.filter(c => !c.parent_id)
	);

	function isActive(id: number | null) {
		return selected === id;
	}
</script>

<div class="grid grid-cols-2 gap-2">

	<!-- SIN PADRE -->
	<button
		type="button"
		onclick={() => (selected = null)}
		class="
			group relative overflow-hidden rounded-xl p-3 text-xs font-bold
			transition-all duration-300 ease-out active:scale-[0.97]
			{isActive(null)
				? 'bg-emerald-500 text-white shadow-xs '
				: 'bg-white/5 text-white/50 hover:bg-white/10 hover:text-white'}
		"
	>
		Sin padre

		<!-- glow -->
		<span
			class="
				absolute inset-0 opacity-0 transition-opacity duration-300
				group-hover:opacity-10 bg-emerald-400
			"
		></span>
	</button>

	<!-- PARENTS -->
	{#each parents as p}
		<button
			type="button"
			onclick={() => (selected = p.id)}
			class="
				group relative overflow-hidden rounded-xl p-3 text-xs font-bold
				transition-all duration-300 ease-out active:scale-[0.97]
				{isActive(p.id)
					? 'bg-emerald-500 text-white shadow-xs '
					: 'bg-white/5 text-white/50 hover:bg-white/10 hover:text-white'}
			"
		>
			{p.name}

			<!-- glow hover -->
			<span
				class="
					absolute inset-0 opacity-0 transition-opacity duration-300
					group-hover:opacity-10 bg-emerald-400
				"
			></span>
		</button>
	{/each}
</div>