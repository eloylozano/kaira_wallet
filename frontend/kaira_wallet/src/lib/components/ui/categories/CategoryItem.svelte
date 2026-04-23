<script lang="ts">
	import * as Icons from 'lucide-svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';

	import { deleteCategory } from '$lib/api/categories';
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { transactionTypeLabel } from '$lib/utils/transactionType';

	let { cat, onEdit } = $props();

	let showDeleteModal = $state(false);

	let modalTitle = $state('Eliminar categoría');
	let modalMessage = $state('Esta acción no se puede deshacer.');

	let confirmText = $state('Eliminar');

	function askDelete() {
		showDeleteModal = true;

		// reset por si venía de error anterior
		modalTitle = 'Eliminar categoría';
		modalMessage = 'Esta acción no se puede deshacer.';
		confirmText = 'Eliminar';
	}

	function closeModal() {
		showDeleteModal = false;
	}

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

	const style = $derived(typeStyle[cat.transaction_type] ?? typeStyle.expense);

	async function confirmDelete() {
		// 👇 si ya estamos en modo aviso ("Entendido"), solo cerrar
		if (confirmText === 'Entendido' || confirmText === 'Cerrar') {
			closeModal();
			return;
		}

		try {
			await deleteCategory(cat.id);

			showDeleteModal = false;

			await categoriesStore.refresh();
		} catch (e: any) {
			// si tiene movimientos asociados
			if (e.message?.includes('movimientos asociados') || e.message?.includes('foreign key')) {
				modalTitle = 'No se puede eliminar';

				modalMessage =
					'Esta categoría tiene movimientos asociados. Reasigna o elimina esos movimientos antes.';

				confirmText = 'Entendido';

				return;
			}

			modalTitle = 'Error';
			modalMessage = e.message || 'Ha ocurrido un error.';
			confirmText = 'Cerrar';
		}
	}
</script>

<ConfirmModal
	isOpen={showDeleteModal}
	title={modalTitle}
	message={modalMessage}
	{confirmText}
	onConfirm={confirmDelete}
	onCancel={closeModal}
/>

<div class="kaira-panel relative rounded-2xl p-4">
	<div class="flex items-center justify-between">
		<div class="flex items-center gap-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10"
				style="background:{style.bg}"
			>
				<svelte:component this={getIcon(cat.icon)} class="h-5 w-5" style="color:{style.color}" />
			</div>

			<div>
				<p class="font-bold">{cat.name}</p>

				<p class="text-xs opacity-50">
					{transactionTypeLabel[cat.transaction_type]}
				</p>
			</div>
		</div>

		<div class="flex gap-2">
			<button
				onclick={() => onEdit(cat)}
				class="flex h-9 w-9 items-center justify-center rounded-xl bg-white/5"
			>
				<Icons.Pencil class="h-4 w-4" />
			</button>

			<button
				onclick={askDelete}
				class="flex h-9 w-9 items-center justify-center rounded-xl bg-white/5 text-red-400"
			>
				<Icons.Trash2 class="h-4 w-4" />
			</button>
		</div>
	</div>
</div>
