<script lang="ts">
	let { type = $bindable(''), isPaid = $bindable('') } = $props();

	const types = [
		{ value: '', label: 'Todos' },
		{ value: 'expense', label: 'Gastos' },
		{ value: 'income', label: 'Ingresos' },
		{ value: 'invest', label: 'Inversión' }
	];

	const paidStates = [
		{ value: '', label: 'Todos' },
		{ value: 'true', label: 'Pagado' },
		{ value: 'false', label: 'Pendiente' }
	];
</script>

<div class="space-y-4">
	<!-- TYPE -->
	<div class="flex gap-2 overflow-x-auto py-1">
		{#each types as t}
			<button
				onclick={() => (type = t.value)}
				class="flex-none rounded-xl px-4 py-2 text-[10px] font-bold uppercase transition-all
				{type === t.value ? 'kaira-chip-active' : 'kaira-chip'}"
			>
				{t.label}
			</button>
		{/each}
	</div>

	<!-- IS PAID -->
	<div class="flex items-center justify-between px-2">
		<span class="kaira-soft text-[10px] font-black tracking-widest uppercase">
			Estado de pago
		</span>

		<!-- MISMO ESTILO QUE TYPE -->
		<div class="flex gap-2 overflow-x-auto py-1">
			{#each paidStates as p}
				<button
					onclick={() => (isPaid = p.value)}
					class="flex-none rounded-xl px-4 py-2 text-[10px] font-bold uppercase transition-all
				{isPaid === p.value ? 'kaira-chip-active' : 'kaira-chip'}"
				>
					{p.label}
				</button>
			{/each}
		</div>
	</div>
</div>
