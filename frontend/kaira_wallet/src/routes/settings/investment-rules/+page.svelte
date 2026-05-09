<script lang="ts">
	import { investmentStore } from '$lib/stores/domain/investments.svelte';
	import GlassCard from '$lib/components/ui/core/GlassCard.svelte';
	import { fly, fade } from 'svelte/transition';

	let newPattern = $state('');
	let newAlias = $state('');

	function handleAdd() {
		if (!newPattern || !newAlias) return;
		investmentStore.addRule(newPattern.trim(), newAlias.trim());
		newPattern = '';
		newAlias = '';
	}
</script>

<div class="mx-auto max-w-xl space-y-8 py-6 md:px-0">
	<header class="space-y-1">
		<h1 class="text-3xl font-black tracking-tighter text-white uppercase italic md:text-4xl">
			Reglas de <span class="text-emerald-400">Detección</span>
		</h1>
		<p class="text-[9px] font-black tracking-[0.2em] text-white/30 uppercase md:text-[10px]">
			Smart Matching Engine
		</p>
	</header>

	<GlassCard class="!rounded-[28px] border-white/10 bg-white/[0.03] p-2">
		<div class="flex flex-col gap-4 p-3">
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				<div class="space-y-1.5">
					<span class="ml-2 text-[9px] font-black tracking-widest text-white/20 uppercase"
						>Patrón</span
					>
					<input bind:value={newPattern} placeholder="Ej: VANG" class="kaira-input" />
				</div>
				<div class="space-y-1.5">
					<span class="ml-2 text-[9px] font-black tracking-widest text-white/20 uppercase"
						>Alias</span
					>
					<input bind:value={newAlias} placeholder="Ej: S&P 500" class="kaira-input" />
				</div>
			</div>

			<button
				onclick={handleAdd}
				disabled={!newPattern || !newAlias}
				class="group relative w-full overflow-hidden rounded-xl bg-emerald-500 py-4 text-[10px] font-black tracking-[0.2em] text-white uppercase transition-all hover:bg-emerald-400 hover:shadow-[0_0_20px_rgba(16,185,129,0.2)] active:scale-[0.98] disabled:opacity-20 disabled:grayscale md:py-3"
			>
				<span class="relative z-10">Añadir Regla</span>
				<div
					class="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent transition-transform duration-500 group-hover:translate-x-full"
				></div>
			</button>
		</div>
	</GlassCard>

	<div class="space-y-4">
		<h3 class="px-2 text-[10px] font-black tracking-[0.2em] text-white/40 uppercase">
			Reglas Activas
		</h3>

		<div class="grid gap-2.5">
			{#each Object.entries(investmentStore.rules) as [pattern, alias] (pattern)}
				<div
					in:fly={{ y: 10, duration: 300 }}
					out:fade
					class="group relative flex items-center justify-between overflow-hidden rounded-[20px] border border-white/5 bg-white/[0.02] p-4 transition-all hover:border-white/10"
				>
					<div class="flex flex-col pl-2">
						<span class="text-[9px] font-black tracking-widest text-white/20 uppercase"
							>Detecta "{pattern}"</span
						>
						<span
							class="text-sm font-bold tracking-tight text-white transition-colors group-hover:text-emerald-400"
						>
							{alias}
						</span>
					</div>

					<button
						onclick={() => investmentStore.removeRule(pattern)}
						class="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5 text-white/20 transition-all hover:bg-rose-500/10 hover:text-rose-500 active:bg-rose-500/20 active:text-rose-500 md:h-8 md:w-8"
					>
						<span class="text-xl leading-none">×</span>
					</button>
				</div>
			{:else}
				<div class="flex flex-col items-center justify-center py-16 opacity-20">
					<div class="mb-3 h-[1px] w-8 bg-white"></div>
					<p class="text-[10px] font-black uppercase tracking-widest italic text-center px-4">
						No hay reglas de limpieza
					</p>
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	@reference "tailwindcss";

	.kaira-input {
		@apply w-full rounded-xl border border-white/5 bg-black/40 px-4 py-4 text-sm font-bold text-white transition-all outline-none placeholder:text-white/10 focus:border-emerald-500/50 focus:bg-black/60 focus:ring-4 focus:ring-emerald-500/10 md:py-3;
	}
</style>
