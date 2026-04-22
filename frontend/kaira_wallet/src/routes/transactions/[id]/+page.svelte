<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';
	import { goto } from '$app/navigation';

	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import AmountInput from '$lib/components/ui/AmountInput.svelte';
	import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
	import DatePicker from '$lib/components/ui/DatePicker.svelte';
	import PaidToggle from '$lib/components/ui/PaidToggle.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import NoteInput from '$lib/components/ui/NoteInput.svelte';

	let { data } = $props();

	type TransactionType = 'expense' | 'income' | 'invest';

	const typeOptions = [
		{ value: 'expense', label: 'Gasto' },
		{ value: 'income', label: 'Ingreso' },
		{ value: 'invest', label: 'Inversión' }
	];

	let loading = $state(true);

	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');
	let date = $state(new Date().toISOString().split('T')[0]);
	let selectedCategoryId = $state<number | null>(null);
	let isPaid = $state(true);

	onMount(async () => {
		const res = await fetch(`${PUBLIC_API_URL}/transactions/${data.id}`, {
			headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
		});

		if (res.ok) {
			const tx = await res.json();

			amount = String(tx.amount);
			description = tx.description ?? '';
			type = tx.type;
			date = new Date(tx.date).toISOString().split('T')[0];
			selectedCategoryId = tx.category_id;
			isPaid = tx.is_paid;
		}

		loading = false;
	});

	async function handleUpdate() {
		const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');

		const payload = {
			amount: parseFloat(amount),
			description,
			type,
			category_id: selectedCategoryId,
			date: new Date(date).toISOString(),
			is_paid: isPaid
		};

		const res = await fetch(`${baseUrl}/transactions/${data.id}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'X-Kaira-PIN': PUBLIC_KAIRA_PIN
			},
			body: JSON.stringify(payload)
		});

		if (res.ok) {
			transactionsStore.fetch();
			goto('/transactions');
		}
	}

	async function handleDelete() {
		if (!confirm('¿Seguro que quieres borrar este movimiento?')) return;

		const res = await fetch(`${PUBLIC_API_URL}/transactions/${data.id}`, {
			method: 'DELETE',
			headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
		});

		if (res.ok) goto('/transactions');
	}
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-8 px-4 pt-10 pb-20">
	<header class="flex items-center justify-between">
		<button onclick={() => history.back()} class="text-white/40"> ← Volver </button>

		<h1 class="h1-kaira text-xl">Editar</h1>

		<button onclick={handleDelete} class="text-xs font-bold text-red-400"> Borrar </button>
	</header>

	{#if loading}
		<p class="text-center opacity-50">Cargando...</p>
	{:else}
		<SegmentedControl
			bind:selected={type}
			options={[
				{ value: 'expense', label: 'Gastos', color: '#f43f5e' },
				{ value: 'income', label: 'Ingresos', color: '#10b981' },
				{ value: 'invest', label: 'Inversión', color: '#3b82f6' }
			]}
		/>

		<DatePicker bind:value={date} />

		<AmountInput bind:value={amount} {type} />

		<PaidToggle bind:value={isPaid} />

		<CategorySelector {type} bind:selectedCategoryId />

		<NoteInput bind:value={description} label="Descripción" placeholder="Añadir nota..." />

		<button
			onclick={handleUpdate}
			class="w-full rounded-[24px] bg-primary py-5 text-xs font-black tracking-[0.3em] uppercase"
		>
			Guardar cambios
		</button>
	{/if}
</div>
