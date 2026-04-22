<script lang="ts">
	import * as Icons from 'lucide-svelte';
	import { deleteCategory } from '$lib/api/categories';
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { transactionTypeLabel } from '$lib/utils/transactionType';

	let { cat, onEdit } = $props();

	function toPascal(str: string) {
		return str
			.split('-')
			.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
			.join('');
	}

	function getIcon(name: string) {
		const key = toPascal(name);
		return Icons[key] || Icons.Circle;
	}

	const typeStyle = {
		expense: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
		income: { color: '#22c55e', bg: 'rgba(34,197,94,0.12)' },
		invest: { color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' }
	};

	const style = typeStyle[cat.transaction_type] ?? typeStyle.expense;

	async function remove() {
		const ok = confirm('¿Eliminar categoría?');
		if (!ok) return;

		await deleteCategory(cat.id);
		await categoriesStore.refresh();
	}
</script>

<div class="kaira-panel relative rounded-2xl p-4 transition hover:scale-[1.01]">

	<div class="flex items-center justify-between">

		<!-- LEFT -->
		<div class="flex items-center gap-3">

			<div
				class="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 backdrop-blur-md"
				style="background: {style.bg}"
			>
				<svelte:component
					this={getIcon(cat.icon)}
					class="h-5 w-5"
					style="color: {style.color}"
				/>
			</div>

			<div>
				<p class="font-bold">{cat.name}</p>
				<p class="text-xs capitalize opacity-50">
					{transactionTypeLabel[cat.transaction_type] ?? cat.transaction_type}
				</p>
			</div>

		</div>

		<!-- ACTIONS -->
		<div class="flex gap-2">

			<button
				onclick={() => onEdit(cat)}
				class="flex h-9 w-9 items-center justify-center rounded-xl bg-white/5 text-white/70 transition hover:bg-white/10 hover:text-white"
				title="Editar"
			>
				<Icons.Pencil class="h-4 w-4" />
			</button>

			<button
				onclick={remove}
				class="flex h-9 w-9 items-center justify-center rounded-xl bg-white/5 text-red-400/80 transition hover:bg-red-500/10 hover:text-red-300"
				title="Eliminar"
			>
				<Icons.Trash2 class="h-4 w-4" />
			</button>

		</div>

	</div>

</div>