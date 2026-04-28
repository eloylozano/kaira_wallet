<script lang="ts">
	import { statsService } from '$lib/stores/stats.svelte';

	const stats = $derived(() => statsService.monthlyStatsData || {});

	const fixedTotal = $derived(() => Number(stats().fixed_total || 0));
	const variableTotal = $derived(() => Number(stats().variable_total || 0));

	const total = $derived(() => fixedTotal() + variableTotal());

	const fixedRatio = $derived(() =>
		total() > 0 ? (fixedTotal() / total()) * 100 : 0
	);
</script>

<div class="glass-panel rounded-[32px] border border-white/10 bg-white/5 p-5">

	<div class="mb-4 flex items-center justify-between">
		<h3 class="text-[8px] font-black tracking-widest uppercase opacity-40">
			Estructura de Gastos
		</h3>

		<span class="rounded-full bg-primary/10 px-2 py-1 text-[10px] font-bold text-primary">
			{fixedRatio().toFixed(0)}% Fijos
		</span>
	</div>

	<!-- barra -->
	<div class="flex h-2 w-full overflow-hidden rounded-full bg-white/5">
		<div
			class="h-full bg-primary transition-all duration-500"
			style="width:{fixedRatio()}%"
		></div>

		<div
			class="h-full bg-sky-400/50 transition-all duration-500"
			style="width:{100 - fixedRatio()}%"
		></div>
	</div>

	<!-- valores -->
	<div class="mt-4 grid grid-cols-2 gap-4">

		<div>
			<p class="text-[7px] font-bold uppercase opacity-40">Fijos</p>
			<p class="text-sm font-black italic">
				{fixedTotal().toLocaleString('es-ES', { minimumFractionDigits: 2 })}€
			</p>
		</div>

		<div class="text-right">
			<p class="text-[7px] font-bold uppercase opacity-40">Variables</p>
			<p class="text-sm font-black italic">
				{variableTotal().toLocaleString('es-ES', { minimumFractionDigits: 2 })}€
			</p>
		</div>

	</div>

</div>