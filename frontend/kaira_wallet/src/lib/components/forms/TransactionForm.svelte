<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { createTransaction, updateTransaction } from '$lib/api/transactions';
	import AmountInput from '../ui/AmountInput.svelte';
	import CategorySelector from '../ui/CategorySelector.svelte';
	import DatePicker from '../ui/DatePicker.svelte';
	import NoteInput from '../ui/NoteInput.svelte';
	import SegmentedControl from '../ui/SegmentedControl.svelte';

	// ---------------- TYPES ----------------
	type TransactionType = 'expense' | 'income' | 'invest';
	type FrequencyType = 'fixed' | 'variable';
	type PaidState = 'paid' | 'pending';

	type Transaction = {
		amount: number;
		description?: string;
		type: TransactionType;
		date: string;
		category_id: number | null;
		is_paid: boolean;
		frequency: FrequencyType;
	};

	// ---------------- PROPS ----------------
	type Props = {
		mode?: 'create' | 'edit';
		id?: number | null;
		initial?: Transaction | null;
	};

	let { mode = 'create', id = null, initial = null }: Props = $props();

	// ---------------- STATE ----------------
	let saving = $state(false);

	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');
	let date = $state(new Date().toISOString().split('T')[0]);
	let selectedCategoryId = $state<number | null>(null);
	let frequency = $state<FrequencyType>('variable');
	let paidState = $state<PaidState>('paid');

	onMount(() => {
		categoriesStore.refresh();
	});

	// ---------------- INIT (FIABLE) ----------------
	// ---------------- INIT (CORREGIDO) ----------------
	$effect(() => {
		// Si no hay datos iniciales (estamos creando), no hacemos nada
		if (mode !== 'edit' || !initial) return;

		// Rellenamos los estados con los datos de la transacción
		amount = initial.amount != null ? String(initial.amount) : '';
		description = initial.description ?? '';
		type = initial.type ?? 'expense';

		// Formateo de fecha seguro
		if (initial.date) {
			date = new Date(initial.date).toISOString().split('T')[0];
		}

		// ESTO ES CLAVE: Sincronizar el ID de categoría
		selectedCategoryId = initial.category_id ?? null;

		frequency = initial.frequency ?? 'variable';
		paidState = initial.is_paid ? 'paid' : 'pending';
	});

	// ---------------- SUBMIT ----------------
	async function submit() {
		if (!amount || !selectedCategoryId) return;

		saving = true;

		const payload = {
			type,
			amount: Number(amount),
			description,
			category_id: selectedCategoryId,
			date: new Date(date).toISOString(),
			is_paid: paidState === 'paid',
			frequency,
			user_id: 1
		};

		try {
			if (mode === 'create') {
				await createTransaction(payload);
			} else if (id !== null) {
				await updateTransaction(id, payload);
			}

			await transactionsStore.fetch();
			goto('/transactions');
		} finally {
			saving = false;
		}
	}
</script>

<!-- UI -->
<div class="mx-auto flex max-w-xl flex-col gap-6">
	<SegmentedControl
		bind:selected={type}
		options={[
			{ value: 'expense', label: 'Gastos', color: '#ef4444' },
			{ value: 'income', label: 'Ingresos' },
			{ value: 'invest', label: 'Inversión', color: '#00a6f4' }
		]}
	/>

	<DatePicker bind:value={date} />

	<AmountInput bind:value={amount} {type} />

	<SegmentedControl
		bind:selected={frequency}
		options={[
			{ value: 'variable', label: 'Variable' },
			{ value: 'fixed', label: 'Fijo' }
		]}
	/>

	<CategorySelector {type} bind:selectedCategoryId />

	<SegmentedControl
		bind:selected={paidState}
		options={[
			{ value: 'paid', label: 'Pagado' },
			{ value: 'pending', label: 'Pendiente', color: '#f59e0b' }
		]}
	/>

	<NoteInput bind:value={description} label="Descripción" placeholder="Añadir nota..." />

	<button
		onclick={submit}
		disabled={saving}
		class="w-full rounded-2xl bg-primary py-4 text-xs font-black uppercase"
	>
		{saving ? 'Guardando...' : mode === 'create' ? 'Crear movimiento' : 'Guardar cambios'}
	</button>
</div>
