<script lang="ts">
	import { statsService } from '$lib/stores/domain/stats.svelte';
	import { onMount } from 'svelte';

	let scrolled = $state(false);
	const currentYear = new Date().getFullYear();

	onMount(async () => {
		await statsService.fetchHomeData(currentYear);

		const onScroll = () => {
			scrolled = window.scrollY > 20;
		};
		window.addEventListener('scroll', onScroll);
		return () => window.removeEventListener('scroll', onScroll);
	});

	// BALANCE TOTAL (Histórico)
	let totalBalance = $derived(statsService.globalBalance);

	// DESGLOSE ANUAL (Solo 2026)
	let income = $derived(Number(statsService.summaryData.total_income));
	let expenses = $derived(Number(statsService.summaryData.total_expense));
	let investments = $derived(Number(statsService.summaryData.total_invest));
</script>

<div class="sticky top-0 z-40 w-full transition-all duration-500 {scrolled ? 'pt-2' : 'pt-4'}">
	<div class="mx-auto max-w-xl">
		<div
			class="glass-panel relative overflow-hidden border border-white/10 transition-all duration-500"
			class:rounded-[24px]={scrolled}
			class:rounded-[40px]={!scrolled}
			class:p-4={scrolled}
			class:p-6={!scrolled}
		>
			<div class="relative z-10 flex flex-col">
				<div class="flex items-center justify-between">
					<div class="flex flex-col">
						<p
							class="text-[9px] font-black tracking-[0.2em] text-white/50 uppercase"
							class:hidden={scrolled}
						>
							Balance Total Disponible
						</p>

						<h2
							class="font-black tracking-tight text-white"
							class:text-lg={scrolled}
							class:text-3xl={!scrolled}
							class:sm:text-4xl={!scrolled}
						>
							{totalBalance.toLocaleString('es-ES', { minimumFractionDigits: 2 })}€
						</h2>
					</div>

					<div class="flex items-center gap-2">
						{#if scrolled}
							<div class="flex gap-2 border-r border-white/10 pr-3 text-[10px] font-bold">
								<span class="text-primary">+{income.toFixed(0)}€</span>
								<span class="text-rose-400">-{expenses.toFixed(0)}€</span>
							</div>
						{/if}
						<span class="text-[10px] font-bold text-white/40">EUR</span>
					</div>
				</div>

				<div
					class="grid grid-cols-3 gap-4 transition-all duration-500"
					class:max-h-0={scrolled}
					class:opacity-0={scrolled}
					class:mt-4={!scrolled}
				>
					<div>
						<p class="text-[9px] font-bold text-white uppercase opacity-40">
							Ingresos {currentYear}
						</p>
						<p class="text-sm font-black text-primary sm:text-lg">+{income.toFixed(2)}€</p>
					</div>

					<div class="text-right">
						<p class="text-[9px] font-bold text-white uppercase opacity-40">Gastos {currentYear}</p>
						<p class="text-sm font-black text-rose-400 sm:text-lg">-{expenses.toFixed(2)}€</p>
					</div>

					<div class="text-right">
						<p class="text-[9px] font-bold text-white uppercase opacity-40">Inversión</p>
						<p class="text-sm font-black text-sky-400 sm:text-lg">≈ {investments.toFixed(2)}€</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
