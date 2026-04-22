<script lang="ts">
	import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import AmountInput from '$lib/components/ui/AmountInput.svelte';
	import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { onMount } from 'svelte';
	import DatePicker from '$lib/components/ui/DatePicker.svelte';
	import PaidToggle from '$lib/components/ui/PaidToggle.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';
	import NoteInput from '$lib/components/ui/NoteInput.svelte';

	type TransactionType = 'expense' | 'income' | 'invest';
	const paidOptions = [
		{ value: true, label: 'Pagado' },
		{ value: false, label: 'Pendiente', color: '#f59e0b' } // Color ámbar para pendientes
	];
	const typeOptions = [
		{ value: 'expense', label: 'Gasto' },
		{ value: 'income', label: 'Ingreso' },
		{ value: 'invest', label: 'Inversión' }
	];

	// --- ESTADO ---
	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');
	let isPaid = $state(true);
	let selectedCategoryId = $state<number | null>(null);
	let date = $state(new Date().toISOString().split('T'));
	let loading = $state(false);

	// --- CARGA INICIAL ---
	onMount(async () => {
		if (categoriesStore.all.length === 0) {
			await categoriesStore.refresh(PUBLIC_KAIRA_PIN);
		}
	});

	// --- LÓGICA DE ENVÍO ---
	async function handleSubmit() {
		if (!amount || !selectedCategoryId) {
			alert('Por favor, introduce un importe y selecciona una categoría.');
			return;
		}

		loading = true;
		const cleanDescription = description.trim();
		const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');

		const payload = {
			type,
			amount: parseFloat(amount),
			date: new Date(date).toISOString(),
			description: cleanDescription || 'Nueva transacción',
			notes: cleanDescription || null,
			category_id: selectedCategoryId,
			is_paid: isPaid,
			frequency: 'variable',
			user_id: 1 // Ajustar según tu sistema de auth
		};

		try {
			const res = await fetch(`${baseUrl}/transactions/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Kaira-PIN': PUBLIC_KAIRA_PIN
				},
				body: JSON.stringify(payload)
			});

			if (res.ok) {
				// Resetear formulario
				amount = '';
				description = '';
				// Opcional: recargar el histórico de transacciones
				transactionsStore.fetch();
				alert('¡Movimiento guardado!');
			} else {
				const errorData = await res.json();
				console.error('Error del servidor:', errorData);
			}
		} catch (error) {
			console.error('Error de red:', error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-8 pt-10 pb-20">
	<header>
		<h1 class="h1-kaira text-3xl font-black">Nuevo Movimiento</h1>
		<p class="text-[10px] font-bold tracking-widest uppercase opacity-30">
			Añade un registro a tu cartera
		</p>
	</header>
    
	<SegmentedControl
		bind:selected={type}
		options={[
			{ value: 'expense', label: 'Gastos', color: '#f43f5e' },
			{ value: 'income', label: 'Ingresos', color: '#10b981' },
			{ value: 'invest', label: 'Inversión', color: '#3b82f6' }
		]}
	/>

	<DatePicker bind:value={date} label="Fecha del movimiento" />

	<div class="py-4">
		<AmountInput bind:value={amount} {type} />
	</div>

	<SegmentedControl options={paidOptions} bind:selected={isPaid} />

	<CategorySelector {type} bind:selectedCategoryId />

	<div class="space-y-4">
		<div class="group relative">
			<NoteInput bind:value={description} label="Descripción" placeholder="Añadir nota..." />
		</div>

		<button
			onclick={handleSubmit}
			disabled={loading}
			class="w-full rounded-[24px] bg-primary py-5 text-xs font-black tracking-[0.3em] text-white uppercase shadow-2xl transition-all active:scale-95 disabled:opacity-50"
		>
			{loading ? 'Procesando...' : `Confirmar ${typeOptions.find((o) => o.value === type)?.label}`}
		</button>
	</div>
</div>
