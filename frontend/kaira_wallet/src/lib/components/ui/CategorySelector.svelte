<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';

	let { type, selectedCategoryId = $bindable() } = $props();
	let selectedParentId = $state<number | null>(null);

	const iconMap: Record<string, string> = {
		Transporte: '🚗', Coche: '🚘', Moto: '🏍️', Gasolina: '⛽',
		Alimentación: '🍎', Supermercado: '🛒', Restaurante: '🍔',
		Vivienda: '🏠', Alquiler: '🔑', Servicios: '⚡', Ocio: '🍿',
		Salario: '💰', Inversiones: '📈'
	};

	let currentCategories = $derived(categoriesStore.getByType(type));
	let selectedParent = $derived(currentCategories.find((c) => c.id === selectedParentId));

	$effect(() => {
		if (currentCategories.length > 0) {
			const first = currentCategories;
			selectedParentId = first.id;
			selectedCategoryId = first.subcategories?.length > 0 ? first.subcategories.id : first.id;
		}
	});

	function handleParentSelect(id: number) {
		selectedParentId = id;
		const parent = currentCategories.find((c) => c.id === id);
		if (parent) {
			selectedCategoryId = parent.subcategories?.length > 0 ? parent.subcategories.id : parent.id;
		}
	}
</script>

<div class="flex flex-col gap-6">
	<div class="space-y-3">
		<p class="px-2 text-[10px] font-black uppercase tracking-[0.2em] opacity-40">Grupo</p>
		<div class="no-scrollbar flex gap-2 overflow-x-auto px-1 pb-2">
			{#each currentCategories as parent}
				<button
					type="button"
					onclick={() => handleParentSelect(parent.id)}
					class="flex-none rounded-2xl border px-5 py-3 text-[11px] font-bold transition-all
                    {selectedParentId === parent.id ? 'border-white bg-white text-black' : 'border-white/10 bg-white/5 text-white/50'}"
				>
					{parent.name}
				</button>
			{/each}
		</div>
	</div>

	<div class="space-y-4">
		<p class="px-2 text-[10px] font-black uppercase tracking-[0.2em] opacity-40">
			Detalle de {selectedParent?.name || '...'}
		</p>
		<div class="grid grid-cols-3 gap-3">
			{#if selectedParent && selectedParent.subcategories?.length > 0}
				{#each selectedParent.subcategories as sub}
					<button
						type="button"
						onclick={() => (selectedCategoryId = sub.id)}
						class="flex flex-col items-center gap-2 rounded-[24px] border p-4 transition-all
                        {selectedCategoryId === sub.id ? 'border-primary bg-primary/20 text-primary' : 'border-white/5 bg-white/5 opacity-60'}"
					>
						<span class="text-2xl">{iconMap[sub.name] || '✨'}</span>
						<span class="text-center text-[9px] font-black uppercase tracking-tighter">{sub.name}</span>
					</button>
				{/each}
			{:else if selectedParent}
				<button
					type="button"
					onclick={() => (selectedCategoryId = selectedParentId)}
					class="col-span-3 flex items-center justify-center gap-3 rounded-[24px] border border-primary bg-primary/10 p-6 text-primary"
				>
					<span class="text-xs font-black uppercase tracking-widest text-center">Usar {selectedParent.name}</span>
				</button>
			{/if}
		</div>
	</div>
</div>

<style>
	.no-scrollbar::-webkit-scrollbar { display: none; }
	.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>