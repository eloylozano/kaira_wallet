<script lang="ts">
	import { statsService } from '$lib/stores/stats.svelte';

	let stats = $derived(() => statsService.monthlyStatsData || {});

	let safeFixed = $derived(() =>
		Number(stats()?.fixed_total || 0)
	);

	let safeVariable = $derived(() =>
		Number(stats()?.variable_total || 0)
	);

	let safeTotal = $derived(() =>
		safeFixed() + safeVariable()
	);

	let fixedPercent = $derived(() => {
		const apiRatio = Number(stats()?.fixed_ratio);

		if (!isNaN(apiRatio) && apiRatio >= 0) {
			return apiRatio; // ya viene en %
		}

		const total = safeTotal();

		return total > 0
			? (safeFixed() / total) * 100
			: 0;
	});

	// clamp por seguridad para evitar valores absurdos
	let normalizedPercent = $derived(() =>
		Math.min(Math.max(fixedPercent(), 0), 100)
	);

	let statusColor = $derived(() =>
		normalizedPercent() > 60
			? 'text-rose-400'
			: normalizedPercent() < 30
				? 'text-primary'
				: 'text-sky-300'
	);
</script>

<div class="glass-panel group relative overflow-hidden rounded-[32px] border border-white/10 bg-white/5 p-6">
	<div class="mb-6 flex items-center justify-between">
		<div>
			<h3 class="text-[10px] font-black tracking-[0.2em] text-white/40 uppercase">
				Estructura de Gastos
			</h3>
			<p class="text-[9px] font-bold text-primary/60">
				Fijos vs Variables
			</p>
		</div>

		<div class="flex flex-col items-end">
			<span class="text-2xl font-black tracking-tighter italic {statusColor()}">
				{fixedPercent().toFixed(0)}%
			</span>

			<span class="text-[8px] font-bold uppercase opacity-30">
				Carga Fija
			</span>
		</div>
	</div>

	<div class="relative h-4 w-full overflow-hidden rounded-full bg-white/5">
		<div
			class="absolute top-0 left-0 h-full bg-primary transition-all duration-1000"
			style="width:{fixedPercent()}%"
		></div>

		<div
			class="absolute top-0 h-full bg-sky-400/30"
			style="left:{fixedPercent()}%; width:{100 - fixedPercent()}%"
		></div>
	</div>

	<div class="mt-6 grid grid-cols-2 gap-8">

		<div class="flex flex-col gap-1">
			<div class="flex items-center gap-2">
				<div class="h-1.5 w-1.5 rounded-full bg-primary"></div>
				<span class="text-[10px] font-bold uppercase opacity-40">
					Gastos Fijos
				</span>
			</div>

			<p class="text-lg font-black italic">
				{safeFixed().toLocaleString('es-ES',{minimumFractionDigits:2})}€
			</p>
		</div>

		<div class="flex flex-col gap-1 text-right">
			<div class="flex items-center justify-end gap-2">
				<span class="text-[10px] font-bold uppercase opacity-40">
					Variables
				</span>
				<div class="h-1.5 w-1.5 rounded-full bg-sky-400/50"></div>
			</div>

			<p class="text-lg font-black text-sky-100/80 italic">
				{safeVariable().toLocaleString('es-ES',{minimumFractionDigits:2})}€
			</p>
		</div>

	</div>

	<div class="mt-6 border-t border-white/5 pt-4">
		<p class="text-[10px] leading-relaxed text-white/40">

			{#if fixedPercent() > 60}
				⚠️ Carga fija alta.
			{:else if fixedPercent() < 30}
				✅ Estructura ágil.
			{:else}
				✨ Equilibrio sano.
			{/if}

		</p>
	</div>
</div>