<script lang="ts">
	import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import AmountInput from '$lib/components/ui/AmountInput.svelte';
	import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { onMount } from 'svelte';
	import DatePicker from '$lib/components/ui/DatePicker.svelte';
	import PaidToggle from '$lib/components/ui/PaidToggle.svelte';

	type TransactionType = 'expense' | 'income' | 'invest';

	const typeOptions = [
		{ value: 'expense', label: 'Gasto' },
		{ value: 'income', label: 'Ingreso' },
		{ value: 'invest', label: 'Inversión' }
	];

	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');
	let isPaid = $state(true);
	let selectedCategoryId = $state<number | null>(null);

	let date = $state(new Date().toISOString().split('T')[0]);

	onMount(async () => {
		if (categoriesStore.all.length === 0) {
			await categoriesStore.refresh(PUBLIC_KAIRA_PIN);
		}
	});

	async function handleSubmit() {
		// 🔥 NORMALIZACIÓN FIABLE
		const cleanDescription = description.trim();

		const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');
		const finalUrl = `${baseUrl}/transactions/`;

		if (!amount || !selectedCategoryId) {
			alert('Faltan datos');
			return;
		}

		const payload = {
			type,
			amount: parseFloat(amount),
			date: new Date(date).toISOString(),
			description: description.trim() || 'Nueva transacción',
			notes: description.trim() || null,
			category_id: selectedCategoryId,
			is_paid: isPaid,
			frequency: 'variable',
			user_id: 1
		};

		try {
			const res = await fetch(finalUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Kaira-PIN': PUBLIC_KAIRA_PIN
				},
				body: JSON.stringify(payload)
			});

			if (res.ok) {
				amount = '';
				description = '';
			}
		} catch (error) {
			console.error(error);
		}
	}
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 px-2 pt-10">
	<header>
		<h1 class="h1-kaira">Nuevo Movimiento</h1>
	</header>

	<SegmentedControl options={typeOptions} bind:selected={type} />

	<DatePicker bind:value={date} label="Fecha del movimiento" />

	<AmountInput bind:value={amount} {type} />

	<PaidToggle bind:value={isPaid} />

	<CategorySelector {type} bind:selectedCategoryId />

	<div class="space-y-6">
		<input
			type="text"
			placeholder="Nota..."
			bind:value={description}
			class="w-full rounded-2xl border border-white/5 bg-white/5 p-5 text-sm outline-none focus:border-primary/40"
		/>

		<button
			onclick={handleSubmit}
			class="w-full rounded-[24px] bg-primary py-5 text-xs font-black tracking-[0.3em] text-white uppercase shadow-2xl transition-all active:scale-95"
		>
			Confirmar {typeOptions.find((o) => o.value === type)?.label}
		</button>
	</div>
</div>
