<script lang="ts">
	let { type = $bindable(''), isPaid = $bindable('') } = $props();
	const types = [
		{ value: '', label: 'Todos' },
		{ value: 'expense', label: 'Gastos' },
		{ value: 'income', label: 'Ingresos' },
		{ value: 'invest', label: 'Inversión' }
	];
</script>

<div class="space-y-4">
	<div class="flex gap-2 overflow-x-auto no-scrollbar py-1">
		{#each types as t}
			<button
				type="button"
				onclick={() => (type = t.value)}
				class="flex-none rounded-xl px-4 py-2 text-[10px] font-bold uppercase tracking-wider transition-all border
				{type === t.value 
					? 'bg-white text-black border-white' 
					: 'bg-white/5 border-white/5 text-white/40 hover:border-white/20'}"
			>
				{t.label}
			</button>
		{/each}
	</div>

	<div class="flex items-center justify-between px-2">
		<span class="text-[10px] font-black uppercase tracking-widest opacity-30">Estado de pago</span>
		<div class="flex bg-white/5 p-1 rounded-xl border border-white/5">
			{#each ['', true, false] as val}
				<button
					onclick={() => (isPaid = val)}
					class="px-3 py-1.5 rounded-lg text-[9px] font-bold uppercase transition-all
					{isPaid === val ? 'bg-white/10 text-white' : 'text-white/30'}"
				>
					{val === '' ? 'Todos' : val ? 'Pagado' : 'Pendiente'} 
				</button>
			{/each}
		</div>
	</div>
</div>