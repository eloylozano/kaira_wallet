<script lang="ts">
	import { statsService } from '$lib/stores/domain/stats.svelte';
	import { settingsStore } from '$lib/stores/domain/settings.svelte';

	const monthLabels = ['E','F','M','A','M','J','J','A','S','O','N','D'];

	let chartData = $derived(() => {
		const raw = statsService.monthlyBreakdown ?? [];

		const base = Array.from({ length: 12 }, (_, i) => ({
			month: i,
			income: 0,
			expense: 0,
			invest: 0
		}));

		for (const row of raw) {
			if (!row?.month) continue;

			const parts = row.month.split('-');
			const m = Number(parts[1]) - 1;

			if (isNaN(m) || m < 0 || m > 11) continue;

			base[m] = {
				month: m,
				income: Number(row.income || 0),
				expense: Number(row.expense || 0),
				invest: Number(row.invest || 0)
			};
		}

		return base;
	});

	let maxValue = $derived(() => {
		const values = chartData().flatMap(d => [d.income, d.expense, d.invest]);
		const maxData = Math.max(...values, 0);
		const budget = Number(settingsStore.monthlyBudget || 0);

		return Math.max(maxData, budget, 100) * 1.15;
	});

	let budget = $derived(() => Number(settingsStore.monthlyBudget || 0));

	let budgetLineY = $derived(() => {
		const max = maxValue();
		if (!max) return 0;
		return (budget() / max) * 100;
	});

	// 🔥 Y AXIS LABELS (esto es lo nuevo)
	let yLabels = $derived(() => {
		const max = maxValue();
		return [
			max,
			max * 0.75,
			max * 0.5,
			max * 0.25,
			0
		];
	});
</script>

<div class="glass-panel relative flex h-64 flex-col rounded-[32px] border border-white/10 bg-white/5 pt-6 pb-8 pe-4">

	<p class="text-center text-[8px] font-black tracking-widest uppercase opacity-40">
		Flujo Anual {statsService.selectedYear}
	</p>

	<div class="relative mt-6 flex h-full">

		<!-- 🔹 EJE Y -->
		<div class="flex w-10 flex-col justify-between text-[8px] opacity-30 pr-2">
			{#each yLabels() as y}
				<span class="text-right">
					{Math.round(y)}
				</span>
			{/each}
		</div>

		<!-- 🔹 GRÁFICO -->
		<div class="relative flex flex-1 items-end gap-1.5 sm:gap-3">

			<!-- línea presupuesto -->
			<div
				class="absolute left-0 right-0 z-10 border-t border-dashed border-amber-400/50"
				style="bottom: {budgetLineY()}%"
			>
				<span class="absolute -top-4 right-2 text-[7px] font-bold text-amber-400/60 uppercase">
					Meta: {budget()}€
				</span>
			</div>

			{#each chartData() as d, i}
				<div class="relative flex h-full flex-1 items-end justify-center gap-[1px]">

					<div
						class="w-full max-w-[6px] rounded-t-[2px] bg-emerald-500/90 transition-all duration-500"
						style="height: {(d.income / maxValue()) * 100}%"
					></div>

					<div
						class="w-full max-w-[6px] rounded-t-[2px] bg-rose-400/90 transition-all duration-500"
						style="height: {(d.expense / maxValue()) * 100}%"
					></div>

					<div
						class="w-full max-w-[6px] rounded-t-[2px] bg-sky-400/90 transition-all duration-500"
						style="height: {(d.invest / maxValue()) * 100}%"
					></div>

					<span class="absolute -bottom-5 text-[8px] opacity-30">
						{monthLabels[i]}
					</span>
				</div>
			{/each}
		</div>
	</div>
</div>