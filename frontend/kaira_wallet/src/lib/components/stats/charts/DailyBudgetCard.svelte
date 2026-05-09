<script lang="ts">
	import { transactionsStore } from '$lib/stores/domain/transactions.svelte';
	import { statsService } from '$lib/stores/domain/stats.svelte';
	import { settingsStore } from '$lib/stores/domain/settings.svelte';

	// 1. Datos base
	let spentSoFar = $derived(statsService.monthlyStatsData.expense || 0);
	let remainingDays = $derived(statsService.daysRemaining.current);
	let totalDays = $derived(statsService.daysRemaining.total);

	// 2. Presupuesto Diario Ideal (el "benchmark" del mes)
	// Ej: 300€ / 30 días = 10€/día ideal
	let idealDailyBudget = $derived(settingsStore.monthlyBudget / totalDays);

	// 3. Presupuesto Diario Actual (lo que realmente puedes gastar hoy)
	let actualDailyAvailable = $derived(() => {
		if (remainingDays <= 0) return 0;
		const available = settingsStore.monthlyBudget - spentSoFar;
		return Math.max(0, available / remainingDays);
	});

	// 4. Cálculo de Salud (Ratio entre lo que tienes y lo que deberías tener)
	let healthRatio = $derived(() => {
		if (idealDailyBudget <= 0) return 0;
		return (actualDailyAvailable() / idealDailyBudget) * 100;
	});

	// 5. Lógica de colores dinámica según tu petición
	// Verde: >= 100% (tienes 10€ o más si el ideal eran 10€)
	// Naranja: 70% - 99% (tienes entre 7€ y 10€)
	// Rojo: < 70% (tienes menos de 7€)
	let statusColorClass = $derived(() => {
		const ratio = healthRatio();
		if (ratio >= 100) return 'text-emerald-400';
		if (ratio >= 70) return 'text-amber-500';
		return 'text-rose-500';
	});

	let barColorClass = $derived(() => {
		const ratio = healthRatio();
		if (ratio >= 100) return 'bg-emerald-400';
		if (ratio >= 70) return 'bg-amber-500';
		return 'bg-rose-500';
	});

	// Para la barra: si tienes más del ideal, la barra está llena.
	// Si tienes menos, se va vaciando.
	let barWidth = $derived(Math.min(healthRatio(), 100));
</script>

<div class="glass-panel flex flex-col gap-4 rounded-[32px] border border-white/10 bg-white/5 p-5">
	<div class="flex items-center justify-between">
		<p class="text-[8px] font-black tracking-[0.2em] uppercase opacity-40">Ritmo de gasto</p>
	</div>

	<div class="flex items-end justify-between">
		<div class="flex items-baseline gap-1">
			<p class="text-2xl font-black {statusColorClass()}">
				{actualDailyAvailable().toFixed(2)}€
			</p>
			<p class="text-[10px] font-medium opacity-40">/ día</p>
		</div>
	</div>

	<div class="flex flex-col gap-2">
		{#if healthRatio() < 100}
			<p class="text-[8px] font-bold text-amber-500/60 uppercase italic">
				Objetivo diario - {(100 - healthRatio()).toFixed(0)}% 
			</p>
		{:else}
			<p class="text-[8px] font-bold text-emerald-400/60 uppercase italic">
				Objetivo diario + {Math.max(0, healthRatio() - 100).toFixed(0)}%
			</p>
		{/if}
		<div class="relative h-1.5 w-full overflow-hidden rounded-full bg-white/10">
			<div
				class="h-full transition-all duration-1000 ease-out {barColorClass()}"
				style="width: {barWidth}%"
			>
				<div class="h-full w-full bg-white/20 blur-sm"></div>
			</div>
		</div>
	</div>
</div>
