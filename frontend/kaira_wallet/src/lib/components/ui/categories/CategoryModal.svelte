<script lang="ts">
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import IconPicker from './IconPicker.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import { createCategory, updateCategory } from '$lib/api/categories';
	import CategoryParentSelector from './CategoryParentSelector.svelte';
	import GlassInput from '../GlassInput.svelte';

	let { editing = null, onClose } = $props();

	let name = $state(editing?.name ?? '');
	let icon = $state(editing?.icon ?? 'circle');
	let type = $state(editing?.transaction_type ?? 'expense');

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

<div
	class="fixed inset-0 z-[9999] flex items-end justify-center bg-black/60 p-4 pb-32 sm:items-center sm:pb-4"
>
	<div
		class="
            /* 2.

            Redondeado
            completo para
            que flote
            bien

            */ max-h-[75vh] w-full overflow-y-auto rounded-3xl border border-white/10 bg-white/10 p-5
            shadow-2xl

            backdrop-blur-xl
            backdrop-saturate-150

            sm:max-w-xl
        "
	>
		<!-- HANDLE (solo móvil) -->
		<div class="mx-auto mb-4 h-1 w-12 rounded-full bg-white/20 sm:hidden"></div>

		<h2 class="mb-5 text-center text-xl font-bold tracking-tight">
			{editing ? 'Editar categoría' : 'Nueva categoría'}
		</h2>

		<!-- INPUT -->
		<div class="mb-4">

			<GlassInput label="Nombre" placeholder="Ej: Comida, Sueldo..." bind:value={name} />
		</div>

		<!-- TYPE -->
		<div class="mb-5">
			<p class="mb-2 text-[10px] font-bold uppercase opacity-60">Tipo</p>

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
			<p class="mb-2 text-[10px] font-bold uppercase opacity-60">Icono</p>

			<IconPicker bind:icon />
		</div>

		<!-- ACTIONS -->
		<div class="flex gap-2 pb-2">
			<button onclick={cancel} class="flex-1 rounded-xl bg-white/5 py-3 text-sm font-bold">
				Cancelar
			</button>

			<button onclick={save} class="flex-1 rounded-xl bg-primary py-3 text-sm font-bold text-white">
				Guardar
			</button>
		</div>
	</div>
</div>
