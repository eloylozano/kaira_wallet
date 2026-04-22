<script lang="ts">
	import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import AmountInput from '$lib/components/ui/AmountInput.svelte';
	import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
	import { categoriesStore } from '$lib/stores/categories.svelte';
	import { onMount } from 'svelte';

	type TransactionType = 'expense' | 'income' | 'invest';

	const typeOptions = [
		{ value: 'expense', label: 'Gasto' },
		{ value: 'income', label: 'Ingreso' },
		{ value: 'invest', label: 'Inversión' }
	];

	let amount = $state('');
	let description = $state('');
	let type = $state<TransactionType>('expense');
	let isPaid = $state(true); // Estado de pago
	let selectedCategoryId = $state<number | null>(null);

	onMount(async () => {
		if (categoriesStore.all.length === 0) {
			await categoriesStore.refresh(PUBLIC_KAIRA_PIN);
		}
	});

	async function handleSubmit() {
		// 1. Limpieza de URL (evita la doble barra)
		const baseUrl = PUBLIC_API_URL.endsWith('/') ? PUBLIC_API_URL.slice(0, -1) : PUBLIC_API_URL;

		const finalUrl = `${baseUrl}/transactions/`;
		console.log('🔗 Intentando conectar a:', finalUrl);

		if (!amount || !selectedCategoryId) {
			alert('Faltan datos');
			return;
		}

		const payload = {
			type,
			amount: parseFloat(amount),
			description: description || 'Nueva transacción',
			category_id: selectedCategoryId,
			is_paid: isPaid,
			frequency: 'variable',
			user_id: 1
		};

		try {
			const res = await fetch(finalUrl, {
				method: 'POST',
				mode: 'cors', // Forzamos modo CORS
				headers: {
					'Content-Type': 'application/json',
					'X-Kaira-PIN': PUBLIC_KAIRA_PIN
				},
				body: JSON.stringify(payload)
			});

			if (res.ok) {
				alert('¡Guardado!');
				amount = '';
			} else {
				const err = await res.json();
				console.error('Respuesta error:', err);
			}
		} catch (error) {
			console.error('🚨 Error de conexión real:', error);
			alert('No hay conexión con el servidor. ¿Está el backend encendido en esa IP?');
		}
	}
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 px-4 pt-10 pb-32">
	<header>
		<h1 class="h1-kaira">Nuevo Movimiento</h1>
	</header>

	<SegmentedControl options={typeOptions} bind:selected={type} />

	<AmountInput bind:value={amount} {type} />

	<div class="grid grid-cols-2 gap-2 rounded-[28px] border border-white/5 bg-white/5 p-1.5">
		<button
			onclick={() => (isPaid = true)}
			class="flex items-center justify-center gap-2 rounded-[22px] py-4 text-[11px] font-black tracking-widest uppercase transition-all
            {isPaid ? 'bg-white text-black shadow-xl' : 'text-white/30'}"
		>
			Pagado
		</button>
		<button
			onclick={() => (isPaid = false)}
			class="flex items-center justify-center gap-2 rounded-[22px] py-4 text-[11px] font-black tracking-widest uppercase transition-all
            {!isPaid ? 'bg-amber-400 text-black shadow-xl' : 'text-white/30'}"
		>
			Pendiente
		</button>
	</div>

	<CategorySelector {type} bind:selectedCategoryId />

	<div class="space-y-6">
		<input
			type="text"
			placeholder="Nota opcional..."
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
