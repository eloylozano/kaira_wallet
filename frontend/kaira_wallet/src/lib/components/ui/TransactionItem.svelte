<script lang="ts">
	import * as Icons from 'lucide-svelte';

	let { tx } = $props();

	// Mantenemos la lógica de conversión que usas en el selector para Lucide
	function toPascalCase(str: string) {
		if (!str) return '';
		return str
			.split('-')
			.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
			.join('');
	}

	// DERIVACIÓN CORRECTA: Extraemos el componente de icono directamente
	let IconComponent = $derived(() => {
		if (!tx.category?.icon) return null;
		const key = toPascalCase(tx.category.icon);
		return Icons[key] || null;
	});

	// Ejecutamos la función derivada para obtener el componente renderizable <Icon />
	const Icon = $derived(IconComponent());

	// NUEVO: Derivamos el color del icono basado en el tipo de transacción
	let iconColorClasses = $derived(() => {
		switch (tx.type) {
			case 'income':
				// Verde neón para ingresos
				return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
			case 'expense':
				// Rojo vibrante para gastos
				return 'text-red-400 bg-red-400/10 border-red-400/20';
			case 'invest':
				// Azul eléctrico para inversiones (como Bitcoin)
				return 'text-sky-400 bg-sky-400/10 border-sky-400/20';
			default:
				// Gris neutro por defecto
				return 'text-white/40 bg-white/5 border-white/10';
		}
	});
</script>

<div class="flex items-center gap-4 rounded-3xl bg-white/5 p-4 transition-all hover:bg-white/10">
	<div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border {iconColorClasses()} transition-colors">
		{#if Icon}
			<Icon class="h-6 w-6" />
		{:else}
			<Icons.CircleDollarSign class="h-6 w-6 opacity-20" />
		{/if}
	</div>

	<div class="flex flex-1 flex-col gap-0.5">
		<p class="text-sm font-bold text-white/90">
			{tx.description || 'Sin descripción'}
		</p>

		<p class="text-[11px] font-medium opacity-50 text-white uppercase tracking-wider">
			{tx.category?.name ?? 'General'} · 
			{tx.date ? new Date(tx.date).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' }) : 'Hoy'}
		</p>
	</div>

	<div class="flex flex-col items-end gap-1">
		<span class="text-sm font-black text-white">
			{tx.amount.toLocaleString('es-ES', { minimumFractionDigits: 2 })} €
		</span>
		
		{#if tx.is_paid === false}
			<span class="text-[9px] font-black uppercase tracking-tighter text-orange-400 bg-orange-400/10 px-2 py-0.5 rounded-lg">
				Pendiente
			</span>
		{/if}
	</div>
</div>