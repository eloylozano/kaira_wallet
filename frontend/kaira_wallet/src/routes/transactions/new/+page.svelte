<script lang="ts">
	import TransactionForm from '$lib/components/forms/TransactionForm.svelte';
</script>

<div class="mx-auto max-w-xl pt-10 pb-20">
	<header class="mb-6">
		<h1 class="text-3xl font-black">Nuevo movimiento</h1>
		<p class="text-[10px] font-bold uppercase tracking-widest opacity-30">
			Añade un registro a tu cartera
		</p>
	</header>

	<TransactionForm mode="create" />
</div>