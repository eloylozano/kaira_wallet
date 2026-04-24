<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import * as Icons from 'lucide-svelte';

	type Category = {
		id: number;
		name: string;
		icon?: string;
		subcategories?: Category[];
	};

	let { type, selectedCategoryId = $bindable<number | null>() } = $props<{
		type: string;
		selectedCategoryId: number | null;
	}>();

	let selectedParentId = $state<number | null>(null);

	let currentCategories = $derived<Category[]>(categoriesStore.getByType(type));

	let selectedParent = $derived<Category | undefined>(
		currentCategories.find((c) => c.id === selectedParentId)
	);

	// inicialización segura (evita auto overwrite raro)
	$effect(() => {
		if (!currentCategories.length) return;

		// si ya hay selección válida, no la pisamos
		if (selectedParentId && currentCategories.some((c) => c.id === selectedParentId)) {
			return;
		}

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
		<p class="kaira-soft px-2 text-[10px] font-black tracking-[0.2em] uppercase">Grupo</p>

		<div class="grid grid-cols-3 gap-2 px-1">
			{#each currentCategories as parent}
				<button
					type="button"
					onclick={() => handleParentSelect(parent.id)}
					class="kaira-chip rounded-2xl px-3 py-3 text-center text-[10px] font-bold transition-all
				{selectedParentId === parent.id ? 'kaira-chip-active' : ''}"
				>
					{parent.name}
				</button>
			{/each}
		</div>
	</div>

	<!-- SUBCATEGORÍAS -->
	<div class="space-y-4">
		<p class="kaira-soft px-2 text-[10px] font-black tracking-[0.2em] uppercase">
			Detalle de {selectedParent?.name || '...'}
		</p>

		<div class="grid grid-cols-3 gap-3">
			{#if selectedParent?.subcategories?.length}
				{#each selectedParent.subcategories as sub}
					{@const Icon = Icons[toPascalCase(sub.icon)]}

					<button
						type="button"
						onclick={() => (selectedCategoryId = sub.id)}
						class="kaira-panel flex flex-col items-center gap-2 rounded-[24px] p-4 transition-all
							{selectedCategoryId === sub.id
							? 'kaira-chip-active'
							: 'bg-emerald-500/5 text-emerald-200/60 hover:bg-emerald-500/10 hover:text-emerald-100'}"
					>
						{#if Icon}
							<Icon
								class="h-6 w-6 transition-colors
							{selectedCategoryId === sub.id ? 'text-white' : 'text-emerald-300/60'}"
							/>
						{:else}
							<span class="text-2xl">✨</span>
						{/if}

						<span
							class="text-center text-[9px] font-bold uppercase transition-colors
							{selectedCategoryId === sub.id ? 'text-white' : 'text-gray-200/60'}"
						>
							{sub.name}
						</span>
					</button>
				{/each}
			{:else if selectedParent}
				<button
					type="button"
					onclick={() => (selectedCategoryId = selectedParentId)}
					class="kaira-panel col-span-3 flex items-center justify-center gap-3 rounded-[24px] border-primary p-6 text-primary"
				>
					<span class="text-xs font-black tracking-widest uppercase">
						Usar {selectedParent.name}
					</span>
				</button>
			{/if}
		</div>
	</div>
</div>
