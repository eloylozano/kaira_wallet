<script lang="ts">
	let { data = [] } = $props<{ data: { date: string; value: number }[] }>();

	let chartItems = $derived(
		(data ?? []).map((d) => ({
			...d,
			displayValue: Math.abs(d.value || 0),
			day: new Date(d.date).getDate() // Extraemos el número del día
		}))
	);

	let max = $derived(Math.max(...chartItems.map((d) => d.displayValue), 1));

	// Generamos 3 niveles para el eje Y (importes)
	let yTicks = $derived([max, max / 2, 0]);
</script>

<div class="glass-panel relative overflow-hidden rounded-[32px] border border-white/10 p-5">
	<div class="absolute -top-20 -right-20 h-40 w-40 rounded-full bg-rose-500/10 blur-[70px]"></div>

	<div class="relative z-10 mb-6 flex items-center justify-between">
		<p class="text-[10px] font-black uppercase tracking-widest opacity-60">Gastos del mes</p>
		<p class="text-[10px] font-bold text-rose-400/70">
			{chartItems.length} días activos
		</p>
	</div>

	<div class="relative flex h-32 w-full gap-2">
		<div class="flex flex-col justify-between pb-6 text-[8px] font-bold opacity-30">
			{#each yTicks as tick}
				<span class="flex items-center gap-1">
					{tick.toFixed(0)}<span class="text-[6px]">€</span>
				</span>
			{/each}
		</div>

		<div class="relative flex flex-1 items-end gap-[4px]">
			<div class="absolute inset-0 flex flex-col justify-between pb-6 opacity-[0.05]">
				<div class="w-full border-t border-white"></div>
				<div class="w-full border-t border-white"></div>
				<div class="w-full border-t border-white"></div>
			</div>

			{#each chartItems as d}
				<div class="group relative flex h-full flex-1 flex-col justify-end">
					<div
						class="w-full rounded-t-[3px] bg-rose-500/30 transition-all duration-500 group-hover:bg-rose-500/70"
						style="height: calc({(d.displayValue / max) * 100}% - 24px)"
					></div>

					<div class="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[8px] font-bold opacity-20 transition-opacity group-hover:opacity-100">
						{d.day}
					</div>

					<div class="absolute -top-7 left-1/2 -translate-x-1/2 scale-75 opacity-0 transition-all duration-300 group-hover:scale-100 group-hover:opacity-100">
						<span class="whitespace-nowrap rounded bg-rose-600 px-1.5 py-0.5 text-[9px] font-black text-white shadow-xl">
							{d.displayValue.toFixed(0)}€
						</span>
					</div>
				</div>
			{:else}
				<div class="flex w-full items-center justify-center pb-6 opacity-20">
					<p class="text-[10px] font-bold uppercase">Sin datos</p>
				</div>
			{/each}
		</div>
	</div>

	<div class="relative z-10 mt-4 flex justify-between px-6 text-[9px] font-bold uppercase opacity-30">
		<span>Inicio</span>
		<span>Hoy</span>
	</div>
</div>

<style>
	.glass-panel {
		background: rgba(255, 255, 255, 0.03);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
	}
</style>