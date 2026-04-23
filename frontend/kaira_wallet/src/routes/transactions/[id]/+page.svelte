<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import AmountInput from '$lib/components/ui/AmountInput.svelte';
	import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
	import DatePicker from '$lib/components/ui/DatePicker.svelte';
	import PaidToggle from '$lib/components/ui/PaidToggle.svelte';
	import NoteInput from '$lib/components/ui/NoteInput.svelte';

	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { transactionsStore } from '$lib/stores/transactions.svelte';

	let { data } = $props();

	type TransactionType =
		| 'expense'
		| 'income'
		| 'invest';

	let loading = $state(true);
	let saving = $state(false);

	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');

	let date = $state(
		new Date().toISOString().split('T')[0]
	);

	let selectedCategoryId = $state<number | null>(null);

	let isPaid = $state(true);

	onMount(async () => {

		try {

			if (!categoriesStore.all.length) {
				await categoriesStore.refresh(
					PUBLIC_KAIRA_PIN
				);
			}

			const res = await fetch(
				`${PUBLIC_API_URL}/transactions/${data.id}`,
				{
					headers: {
						'X-Kaira-PIN': PUBLIC_KAIRA_PIN
					}
				}
			);

			if (!res.ok) {
				goto('/transactions');
				return;
			}

			const tx = await res.json();

			amount = String(tx.amount ?? '');

			description =
				tx.description ?? '';

			type =
				tx.type ?? 'expense';

			date = new Date(tx.date)
				.toISOString()
				.split('T')[0];

			selectedCategoryId =
				tx.category_id ?? null;

			isPaid = !!tx.is_paid;

		} catch (e) {

			console.error(e);
			goto('/transactions');

		} finally {

			loading = false;

		}
	});

	async function handleUpdate() {

		if (!amount || !selectedCategoryId) {
			alert('Faltan campos');
			return;
		}

		saving = true;

		try {

			const payload = {
				type,
				amount: parseFloat(amount),
				description,
				category_id: selectedCategoryId,
				date: new Date(date).toISOString(),
				is_paid: isPaid,
				frequency: 'variable',
				user_id: 1
			};

			const res = await fetch(
				`${PUBLIC_API_URL}/transactions/${data.id}`,
				{
					method: 'PUT',
					headers: {
						'Content-Type':'application/json',
						'X-Kaira-PIN': PUBLIC_KAIRA_PIN
					},
					body: JSON.stringify(payload)
				}
			);

			if (!res.ok) {
				throw new Error();
			}

			await transactionsStore.fetch();

			goto('/transactions');

		} catch(e){

			console.error(e);
			alert('No se pudo actualizar');

		} finally {

			saving = false;

		}
	}

	async function handleDelete() {

		if (
			!confirm(
				'¿Seguro que quieres borrar este movimiento?'
			)
		) return;

		const res = await fetch(
			`${PUBLIC_API_URL}/transactions/${data.id}`,
			{
				method:'DELETE',
				headers:{
					'X-Kaira-PIN': PUBLIC_KAIRA_PIN
				}
			}
		);

		if(res.ok){
			goto('/transactions');
		}
	}

	function goBack(){
		if(history.length > 1){
			history.back();
		}else{
			goto('/transactions');
		}
	}
</script>

<div class="mx-auto flex max-w-xl flex-col gap-8 pt-10 pb-20">

	<header class="flex items-center justify-between">

		<button
			onclick={goBack}
			class="flex items-center gap-1 text-xs font-bold uppercase tracking-wide text-white/40 transition-all hover:text-white/70 active:scale-95"
		>
			<span class="text-lg">←</span>
			Volver
		</button>

		<h1 class="h1-kaira text-lg">
			Editar
		</h1>

		<button
			onclick={handleDelete}
			class="rounded-xl border border-rose-500/20 bg-rose-500/10 px-4 py-2 text-xs font-bold uppercase tracking-widest text-rose-400 transition-all hover:bg-rose-500/15 active:scale-95"
		>
			Borrar
		</button>

	</header>

	{#if loading}

		<p class="text-center opacity-50">
			Cargando...
		</p>

	{:else}

		<SegmentedControl
			bind:selected={type}
			options={[
				{ value:'expense', label:'Gastos' },
				{ value:'income', label:'Ingresos' },
				{ value:'invest', label:'Inversión' }
			]}
		/>

		<DatePicker bind:value={date} />

		<AmountInput bind:value={amount} {type} />

		<PaidToggle bind:value={isPaid} />

		<CategorySelector
			{type}
			bind:selectedCategoryId
		/>

		<NoteInput
			bind:value={description}
			label="Descripción"
			placeholder="Añadir nota..."
		/>

		<button
			onclick={handleUpdate}
			disabled={saving}
			class="w-full rounded-[24px] bg-primary py-5 text-xs font-black uppercase tracking-[0.3em] disabled:opacity-50"
		>
			{saving
				? 'Guardando...'
				: 'Guardar cambios'}
		</button>

	{/if}

</div>