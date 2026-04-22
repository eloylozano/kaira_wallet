<script lang="ts">
	// Usamos la sintaxis de Svelte 5 para props vinculables
	let { type = $bindable(''), isPaid = $bindable('') } = $props();

	const types = [
		{ value: '', label: 'Todos' },
		{ value: 'expense', label: 'Gastos' },
		{ value: 'income', label: 'Ingresos' },
		{ value: 'invest', label: 'Inversión' }
	];
</script>

<div class="flex gap-2">
	<select bind:value={type} class="flex-1 rounded-xl bg-white/5 p-3 text-sm">
		{#each types as t}
			<option value={t.value}>{t.label}</option>
		{/each}
	</select>

	<select bind:value={isPaid} class="flex-1 rounded-xl bg-white/5 p-3 text-sm">
		<option value="">Todos</option>
		<option value={true}>Pagados</option>
		<option value={false}>Pendientes</option>
	</select>
</div>