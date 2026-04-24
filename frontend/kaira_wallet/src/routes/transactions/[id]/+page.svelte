<script lang="ts">
	import { onMount } from 'svelte';
	import { getTransaction } from '$lib/api/transactions';
	import TransactionForm from '$lib/components/forms/TransactionForm.svelte';

	let { data } = $props();

	let tx = $state<any>(null);
	let loading = $state(true);

	onMount(async () => {
		try {
			tx = await getTransaction(data.id);
		} finally {
			loading = false;
		}
	});
</script>

<div class="mx-auto max-w-xl pt-10 pb-20">
	<header class="mb-6">
		<h1 class="text-3xl font-black">Editar movimiento</h1>
		<p class="text-[10px] font-bold tracking-widest uppercase opacity-30">
			Corrige o actualiza los detalles de tu movimiento
		</p>
	</header>

	{#if loading}
		<p class="text-center opacity-50">Cargando...</p>
	{:else if tx}
		{#key tx.id}
			<TransactionForm mode="edit" id={data.id} initial={tx} />
		{/key}
	{:else}
		<p class="text-center text-rose-400">No se pudo cargar la transacción</p>
	{/if}
</div>
