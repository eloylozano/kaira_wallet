<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import IconPicker from './IconPicker.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import { createCategory, updateCategory } from '$lib/api/categories';
	import CategoryParentSelector from './CategoryParentSelector.svelte';

	let { editing = null, onClose } = $props();

	let name = $state(editing?.name ?? '');
	let icon = $state(editing?.icon ?? 'circle');
	let type = $state(editing?.transaction_type ?? 'expense');

	// 👇 NUEVO: parent
	let parentId = $state<number | null>(editing?.parent_id ?? null);

	const types = [
		{ value: 'expense', label: 'Gastos', color: '#f43f5e' },
		{ value: 'income', label: 'Ingresos', color: '#10b981' },
		{ value: 'invest', label: 'Inversión', color: '#3b82f6' }
	];

	// SOLO categorías padre (evitas anidar infinito)
	const parents = $derived(categoriesStore.all.filter((c) => !c.parent_id));

	async function save() {
		const payload = {
			name,
			icon,
			transaction_type: type,
			parent_id: parentId
		};

		if (editing) {
			await updateCategory(editing.id, payload);
		} else {
			await createCategory(payload);
		}

		await categoriesStore.refresh();
		onClose();
	}
	function cancel() {
		onClose();
	}
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
	<div
		class="
			

			relative w-full max-w-xl rounded-3xl border
			border-white/10
			bg-white/10
			p-5

			shadow-2xl backdrop-blur-xl
			backdrop-saturate-150
		"
	>
		<h2 class="mb-5 text-center text-xl font-bold tracking-tight">
			{editing ? 'Editar categoría' : 'Nueva categoría'}
		</h2>

		<!-- INPUT -->
		<div class="mb-4">
			<label class="text-[10px] font-bold tracking-widest uppercase opacity-60"> Nombre </label>

			<input
				bind:value={name}
				placeholder="Ej: Comida, Sueldo..."
				class="
					mt-1 w-full
					rounded-2xl
					bg-white/5
					px-4 py-3
					text-sm font-semibold
					transition
					outline-none
					focus:border-1
					focus:border-white/50
					focus:bg-white/10
					focus:ring-0
				"
			/>
		</div>

		<!-- TYPE -->
		<div class="mb-5">
			<p class="mb-2 text-[10px] font-bold tracking-widest uppercase opacity-60">Tipo</p>

			<SegmentedControl
				bind:selected={type}
				options={[
					{ value: 'expense', label: 'Gastos', color: '#f43f5e' },
					{ value: 'income', label: 'Ingresos', color: '#10b981' },
					{ value: 'invest', label: 'Inversión', color: '#3b82f6' }
				]}
			/>
		</div>

		<!-- PARENT -->
		<div class="mb-5">
			<p class="mb-2 text-[10px] font-bold uppercase opacity-60">Categoría padre (opcional)</p>

			<CategoryParentSelector bind:selected={parentId} />
		</div>

		<!-- ICON -->
		<div class="mb-6">
			<p class="mb-2 text-[10px] font-bold tracking-widest uppercase opacity-60">Icono</p>

			<IconPicker bind:icon />
		</div>

		<!-- ACTIONS -->
		<div class="flex gap-2">
			<button onclick={cancel} class="flex-1 rounded-xl bg-white/5 py-3 text-sm font-bold">
				Cancelar
			</button>

			<button onclick={save} class="flex-1 rounded-xl bg-primary py-3 text-sm font-bold text-white">
				Guardar
			</button>
		</div>
	</div>
</div>
