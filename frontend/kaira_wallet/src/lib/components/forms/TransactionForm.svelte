<script lang="ts">
	import { goto } from '$app/navigation';

	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import AmountInput from '$lib/components/ui/AmountInput.svelte';
	import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
	import DatePicker from '$lib/components/ui/DatePicker.svelte';
	import NoteInput from '$lib/components/ui/NoteInput.svelte';

	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import { createTransaction, updateTransaction } from '$lib/api/transactions';

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

	let { mode = 'create', id = null, initial = null } = $props<Props>();

	// 🔥 IMPORTANTE: snapshot estable
	const tx = $derived(initial);

	// ---------------- STATE ----------------
	let saving = $state(false);

	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');
	let date = $state(new Date().toISOString().split('T')[0]);
	let selectedCategoryId = $state<number | null>(null);
	let frequency = $state<FrequencyType>('variable');
	let paidState = $state<PaidState>('paid');

	// ---------------- INIT (FIABLE) ----------------
	$effect(() => {
		if (mode !== 'edit') return;
		if (!tx) return;
		amount = initial?.amount != null ? String(initial.amount) : '';
		description = tx.description ?? '';
		type = tx.type ?? 'expense';
		date = new Date(tx.date).toISOString().split('T')[0];
		selectedCategoryId = tx.category_id ?? null;
		frequency = tx.frequency ?? 'variable';
		paidState = tx.is_paid ? 'paid' : 'pending';
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
			{ value: 'invest', label: 'Inversión', color: '#3b82f6' }
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
