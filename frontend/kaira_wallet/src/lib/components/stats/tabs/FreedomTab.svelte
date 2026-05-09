<script lang="ts">
	import { onMount } from 'svelte';
	import { statsService } from '$lib/stores/domain/stats.svelte';
	import { investmentStore } from '$lib/stores/domain/investments.svelte';
	import GlassCard from '$lib/components/ui/core/GlassCard.svelte';
	import FreedomChart from '../charts/FreedomChart.svelte';

	const target = $derived(investmentStore.targetSavings);
	const data = $derived(statsService.projectionData);

	// Formateadores para evitar errores visuales con nulos
	const currentPercent = $derived(target > 0 ? (data.current_balance / target) * 100 : 0);
	const projectedPercent = $derived(target > 0 ? (data.projected_december / target) * 100 : 0);

	onMount(async () => {
		// Forzamos la carga del target desde localStorage si no está
		await statsService.fetchFreedomProjection();
	});
</script>

<div class="space-y-6">
	<header class="flex flex-col gap-1 px-2">
		<span class="text-[10px] font-black tracking-[0.3em] text-emerald-400 uppercase"
			>Estrategia Kaira</span
		>
		<h2 class="text-2xl font-bold tracking-tighter text-white italic">Libertad Financiera</h2>
	</header>

	<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
		<GlassCard class="!rounded-[32px] border-white/5 bg-white/[0.02]">
			<FreedomChart title="Estado Actual" value={data.current_balance} {target} />
			<div class="px-6 pb-6 text-center">
				<span class="text-[10px] font-bold tracking-widest text-white/30 uppercase">
					{currentPercent.toFixed(1)}% Alcanzado
				</span>
			</div>
		</GlassCard>

		<GlassCard class="!rounded-[32px] border-emerald-500/10 bg-emerald-500/[0.03]">
			<FreedomChart title="Objetivo 31 Dic" value={data.projected_december} {target} />
			<div class="px-6 pb-6 text-center">
				<span class="text-[10px] font-bold tracking-widest text-emerald-400/60 uppercase">
					{projectedPercent.toFixed(1)}% Proyectado
				</span>
			</div>
		</GlassCard>
	</div>

	<GlassCard class="space-y-4 !rounded-[28px] border-white/5 p-5">
		<div class="flex items-end justify-between">
			<div>
				<p class="mb-1 text-[9px] font-black tracking-widest text-white/20 uppercase">
					Ahorro Neto Mensual (Media)
				</p>
				<p class="text-xl font-bold text-white">
					{data.avg_monthly_savings.toLocaleString('es-ES')}€
				</p>
			</div>
			<div class="text-right">
				<p class="mb-1 text-[9px] font-black tracking-widest text-white/20 uppercase">
					Faltan para la meta
				</p>
				<p class="text-sm font-bold text-emerald-400">
					{(target - data.current_balance).toLocaleString('es-ES')}€
				</p>
			</div>
		</div>

		<div class="h-[1px] w-full bg-white/5"></div>

		<p class="text-[10px] leading-relaxed text-white/30 italic">
			Basado en tu comportamiento desde Enero, tu patrimonio crece a un ritmo de <span
				class="font-bold text-white/60">{data.avg_monthly_savings}€/mes</span
			>. A este paso, terminarás el año con un saldo neto de
			<span class="font-bold text-emerald-400/80">{data.projected_december.toLocaleString()}€</span
			>.
		</p>
	</GlassCard>
</div>
