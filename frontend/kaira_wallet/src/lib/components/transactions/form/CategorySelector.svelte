<script lang="ts">
	import { categoriesStore } from '$lib/stores/domain/categories.svelte';
	import * as Icons from 'lucide-svelte';

	const iconSet = Icons as unknown as Record<string, any>;

	type Category = {
		id: number;
		name: string;
		icon?: string;
		subcategories?: Category[];
	};

	let { type, selectedCategoryId = $bindable<number | null>() } = $props<{
		type: string; // 'income', 'expense', 'invest'
		selectedCategoryId: number | null;
	}>();

	// 🎨 Mapeo de colores dinámicos según el tipo
	const theme = $derived(() => {
		switch (type) {
			case 'income':
				return {
					active: 'bg-emerald-500! text-white shadow-[0_0_15px_rgba(16,185,129,0.3)]!',
					base: 'bg-emerald-500/5! text-emerald-200! hover:bg-emerald-500/10! hover:text-emerald-100!',
					icon: 'text-emerald-300/60!'
				};
			case 'expense':
				return {
					active: 'bg-rose-500! text-white shadow-[0_0_15px_rgba(244,63,94,0.3)]!',
					base: 'bg-rose-500/5! text-rose-200! hover:bg-rose-500/10! hover:text-rose-100!',
					icon: 'text-rose-300/60!'
				};
			case 'invest':
				return {
					active: 'bg-sky-500! text-white shadow-[0_0_15px_rgba(14,165,233,0.3)]!',
					base: 'bg-sky-500/5! text-sky-200! hover:bg-sky-500/10! hover:text-sky-100!',
					icon: 'text-sky-300/60!'
				};
			default:
				return { active: 'bg-gray-500', base: 'bg-gray-500/10', icon: 'text-white' };
		}
	});

	let selectedParentId = $state<number | null>(null);

	let currentCategories = $derived<Category[]>(categoriesStore.getByType(type));

	let selectedParent = $derived<Category | undefined>(
		currentCategories.find((c) => c.id === selectedParentId)
	);

	function findParentId(categoryId: number) {
		const parentMatch = currentCategories.find((c) => c.id === categoryId);
		if (parentMatch) return parentMatch.id;

		for (const parent of currentCategories) {
			if (parent.subcategories?.some((sub) => sub.id === categoryId)) {
				return parent.id;
			}
		}
		return null;
	}

	function selectFirstCategory() {
		const first = currentCategories[0];
		if (!first) return;
		selectedParentId = first.id;
		selectedCategoryId = first.subcategories?.length ? first.subcategories[0].id : first.id;
	}

	$effect(() => {
		if (!currentCategories.length) {
			selectedParentId = null;
			selectedCategoryId = null;
			return;
		}

		if (selectedCategoryId) {
			const parentId = findParentId(selectedCategoryId);
			if (parentId) {
				selectedParentId = parentId;
				return;
			}
		}

		if (selectedParentId && currentCategories.some((c) => c.id === selectedParentId)) {
			return;
		}

		selectFirstCategory();
	});

	function toPascalCase(str: string | undefined) {
		if (!str) return '';
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
                {selectedParentId === parent.id
						? theme().active + ' text-white!'
						: 'bg-white/5 text-white/90 hover:text-white'}"
				>
					{parent.name}
				</button>
			{/each}
		</div>
	</div>

	<!-- SUBCATEGORIAS -->
	<div class="space-y-4">
		<p class="kaira-soft px-2 text-[10px] font-black tracking-[0.2em] uppercase">
			Detalle de {selectedParent?.name || '...'}
		</p>

		<div class="grid grid-cols-3 gap-3">
			{#if selectedParent?.subcategories?.length}
				{#each selectedParent.subcategories as sub}
					{@const IconName = toPascalCase(sub.icon)}
					{@const Icon = iconSet[IconName]}

					<button
						type="button"
						onclick={() => (selectedCategoryId = sub.id)}
						class="kaira-panel flex flex-col items-center gap-2 rounded-[24px] p-4 transition-all
                            {selectedCategoryId === sub.id ? theme().active : theme().base}"
					>
						{#if Icon}
							<Icon
								class="h-6 w-6 transition-colors
                            {selectedCategoryId === sub.id ? 'text-white' : theme().icon}"
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
					class="kaira-panel col-span-3 flex items-center justify-center gap-3 rounded-[24px] p-6
                    {selectedCategoryId === selectedParentId ? theme().active : theme().base}"
				>
					<span class="text-xs font-black tracking-widest uppercase">
						Usar {selectedParent.name}
					</span>
				</button>
			{/if}
		</div>
	</div>
</div>
