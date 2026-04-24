<script lang="ts">
	import GlassSelector from '$lib/components/ui/core/GlassSelector.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import { statsService } from '$lib/stores/stats.svelte';

	let selectedTab = $state('mes');


	const tabOptions = [
		{ value: 'mes', label: 'Mes' },
		{ value: 'distribucion', label: 'Distribución' },
		{ value: 'patrimonio', label: 'Patrimonio' },
		{ value: 'libertad', label: 'Libertad' }
	];
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 pt-10 pb-32">
	<header class="flex flex-col gap-4">
		<div class="flex flex-col gap-2">
			<div class="flex items-end justify-between">
				<div class="flex flex-col">
					<h1 class="h1-kaira text-4xl">Stats</h1>
					<p class="text-[10px] font-bold tracking-[0.2em] uppercase opacity-30">
						Análisis de rendimiento
					</p>
				</div>

				<div class="flex w-full max-w-1/2 gap-2">
					<div class="flex-[2]">
						<GlassSelector
							bind:value={statsService.selectedMonth}
							options={statsService.availableMonths}
						/>
					</div>

					<div class="flex-1">
						<GlassSelector
							bind:value={statsService.selectedYear}
							options={statsService.availableYears}
						/>
					</div>
				</div>
			</div>
		</div>

		<SegmentedControl bind:selected={selectedTab} options={tabOptions} />
	</header>

	{#if selectedTab === 'mes'}
		<div class="space-y-6">
			<div
				class="relative mx-auto flex h-56 w-56 items-center justify-center rounded-full border-[12px] border-white/5 shadow-[inset_0_0_20px_rgba(0,0,0,0.2)]"
			>
				<div class="text-center">
					<p class="text-[10px] font-black tracking-widest uppercase opacity-40">Ahorro</p>
					<p class="text-5xl font-black italic">32%</p>
					<p class="mt-1 text-[11px] font-bold text-primary">+450€</p>
				</div>
				<svg class="absolute -rotate-90" width="224" height="224">
					<circle
						cx="112"
						cy="112"
						r="106"
						fill="none"
						stroke="currentColor"
						stroke-width="12"
						stroke-dasharray="665"
						stroke-dashoffset="450"
						class="text-primary"
					/>
				</svg>
			</div>

			<div class="grid grid-cols-2 gap-4">
				<!-- <div class="glass-panel rounded-[32px] border border-white/10 bg-white/5 p-5">
					<p class="text-[9px] font-black tracking-[0.2em] uppercase opacity-40">Disponible Hoy</p>
					<p class="mt-2 text-2xl font-black {statusColor}">{dailyBudget - spentToday}€</p>
					<div class="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
						<div
							class="h-full bg-current transition-all"
							style="width: 70%;"
							class:text-rose-500={spentToday > dailyBudget}
							class:text-primary={spentToday <= dailyBudget}
						></div>
					</div>
				</div> -->

				<div class="glass-panel rounded-[32px] border border-white/10 bg-white/5 p-5">
					<p class="text-[9px] font-black tracking-[0.2em] uppercase opacity-40">Días restantes</p>
					<p class="mt-2 text-2xl font-black">12</p>
					<p class="text-[10px] font-bold italic opacity-30">de 30 días</p>
				</div>
			</div>

			<div
				class="glass-panel flex h-48 flex-col justify-between rounded-[32px] border border-white/10 bg-white/5 p-6"
			>
				<p class="text-center text-[10px] font-black tracking-widest uppercase opacity-40">
					Flujo Acumulado (Ingreso vs Gasto)
				</p>
				<div class="flex h-24 items-end gap-1">
					{#each Array(20) as _, i}
						<div
							class="flex-1 rounded-t-sm bg-primary/20"
							style="height: {Math.random() * 100}%"
						></div>
					{/each}
				</div>
			</div>
		</div>
	{:else if selectedTab === 'dist'}
		<div class="space-y-4">
			<div
				class="glass-panel flex h-64 items-center justify-center rounded-[32px] border border-white/10 bg-white/5"
			>
				<p class="text-xs font-black tracking-widest uppercase opacity-20">
					Pareto Categorías (Chart)
				</p>
			</div>
			<div class="grid grid-cols-1 gap-2">
				{#each ['Vivienda', 'Comida', 'Ocio'] as cat}
					<div
						class="flex items-center justify-between rounded-2xl border border-white/5 bg-white/5 px-6 py-4"
					>
						<span class="text-sm font-bold">{cat}</span>
						<span class="text-sm font-black italic">{(Math.random() * 500).toFixed(0)}€</span>
					</div>
				{/each}
			</div>
		</div>
	{:else if selectedTab === 'patri'}
		<div class="space-y-6">
			<div class="text-center">
				<p class="text-[10px] font-black tracking-widest uppercase opacity-40">Patrimonio Total</p>
				<h2 class="text-5xl font-black tracking-tighter italic">42.500€</h2>
				<p class="mt-1 text-xs font-bold text-primary">+1.2% este mes</p>
			</div>
			<div
				class="glass-panel flex h-64 items-center justify-center rounded-[32px] border border-white/10 bg-white/10"
			>
				<p class="text-xs font-black tracking-widest uppercase opacity-20">
					Evolución Histórica (Area Chart)
				</p>
			</div>
		</div>
	{:else if selectedTab === 'libertad'}
		<div class="space-y-8 py-4">
			<div class="flex justify-around">
				<div class="flex flex-col items-center gap-3">
					<div
						class="flex h-32 w-32 items-center justify-center rounded-full border-8 border-primary/20 border-t-primary"
					>
						<span class="text-2xl font-black italic">1.2</span>
					</div>
					<p class="text-[9px] font-black tracking-widest uppercase opacity-40">Años cubiertos</p>
				</div>
				<div class="flex flex-col items-center gap-3">
					<div
						class="flex h-32 w-32 items-center justify-center rounded-full border-8 border-white/5 border-t-amber-400"
					>
						<span class="text-2xl font-black italic">65%</span>
					</div>
					<p class="text-[9px] font-black tracking-widest uppercase opacity-40">Independencia</p>
				</div>
			</div>
			<div class="glass-panel rounded-[32px] border border-white/10 bg-primary/5 p-6 text-center">
				<p class="text-[10px] font-black tracking-widest uppercase opacity-50">Previsión a 31/12</p>
				<p class="mt-1 text-3xl font-black text-primary italic">48.200€</p>
				<p class="mt-2 text-[10px] opacity-40">Siguiendo tu ritmo de ahorro actual</p>
			</div>
		</div>
	{/if}
</div>

<style>
	/* Animación básica para que el cambio de pestaña no sea brusco */
	.glass-panel {
		backdrop-filter: blur(12px);
		-webkit-backdrop-filter: blur(12px);
	}
</style>
