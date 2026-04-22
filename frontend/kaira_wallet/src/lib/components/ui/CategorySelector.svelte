<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import * as Icons from 'lucide-svelte';

	let { type, selectedCategoryId = $bindable() } = $props();
	let selectedParentId = $state<number | null>(null);

	let currentCategories = $derived(categoriesStore.getByType(type));

	let selectedParent = $derived(currentCategories.find((c) => c.id === selectedParentId));

	$effect(() => {
		if (!currentCategories.length) return;

		const first = currentCategories[0];

		selectedParentId = first.id;

		selectedCategoryId = first.subcategories?.length ? first.subcategories[0].id : first.id;
	});
	function toPascalCase(str: string) {
		return str
			.split('-')
			.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
			.join('');
	}
	function handleParentSelect(id: number) {
		selectedParentId = id;

		const parent = currentCategories.find((c) => c.id === id);

		if (!parent) return;

		selectedCategoryId = parent.subcategories?.length ? parent.subcategories[0].id : parent.id;
	}
</script>

<div class="flex flex-col gap-6">
	<!-- GRUPOS -->
	<div class="space-y-3">
		<p class="px-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Grupo</p>

		<div class="no-scrollbar flex gap-2 overflow-x-auto px-1 pb-2">
			{#each currentCategories as parent}
				<button
					type="button"
					onclick={() => handleParentSelect(parent.id)}
					class="flex-none rounded-2xl border px-5 py-3 text-[11px] font-bold transition-all
					{selectedParentId === parent.id
						? 'border-white bg-white text-black'
						: 'border-white/10 bg-white/5 text-white/50'}"
				>
					{parent.name}
				</button>
			{/each}
		</div>
	</div>

	<!-- SUBCATEGORÍAS -->
	<div class="space-y-4">
		<p class="px-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
			Detalle de {selectedParent?.name || '...'}
		</p>

		<div class="grid grid-cols-3 gap-3">
			{#if selectedParent?.subcategories?.length}
				{#each selectedParent.subcategories as sub}
					{@const Icon = Icons[toPascalCase(sub.icon)]}

					<button
						type="button"
						onclick={() => (selectedCategoryId = sub.id)}
						class="flex flex-col items-center gap-2 rounded-[24px] border p-4 transition-all
						{selectedCategoryId === sub.id
							? 'border-primary bg-primary/20 text-primary'
							: 'border-white/5 bg-white/5 opacity-60'}"
					>
						<!-- ICONO LUCIDE DINÁMICO -->
						{#if Icon}
							<Icon class="h-6 w-6" />
						{:else}
							<span class="text-2xl">✨</span>
						{/if}

						<span class="text-center text-[9px] font-black tracking-tighter uppercase">
							{sub.name}
						</span>
					</button>
				{/each}
			{:else if selectedParent}
				<button
					type="button"
					onclick={() => (selectedCategoryId = selectedParentId)}
					class="col-span-3 flex items-center justify-center gap-3 rounded-[24px] border border-primary bg-primary/10 p-6 text-primary"
				>
					<span class="text-center text-xs font-black tracking-widest uppercase">
						Usar {selectedParent.name}
					</span>
				</button>
			{/if}
		</div>
	</div>
</div>

<style>
	.no-scrollbar::-webkit-scrollbar {
		display: none;
	}
	.no-scrollbar {
		-ms-overflow-style: none;
		scrollbar-width: none;
	}
</style>
