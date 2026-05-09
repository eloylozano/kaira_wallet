<script lang="ts">
	import { settingsStore } from '$lib/stores/domain/settings.svelte';
	import { transactionsStore } from '$lib/stores/domain/transactions.svelte';

	let budget = $derived(settingsStore.monthlyBudget);

	const isCurrentMonth = (dateStr: string) => {
		const d = new Date(dateStr);
		const now = new Date();

		return (
			d.getMonth() === now.getMonth() &&
			d.getFullYear() === now.getFullYear()
		);
	};

	let spent = $derived(
		(transactionsStore.all ?? [])
			.filter(
				t =>
					t.type === 'expense' &&
					t.is_paid &&
					isCurrentMonth(t.date)
			)
			.reduce(
				(acc, t) =>
					acc + Number(t.amount || 0),
				0
			)
	);

	let investments = $derived(
		(transactionsStore.all ?? [])
			.filter(
				t =>
					t.type === 'invest' &&
					t.is_paid &&
					isCurrentMonth(t.date)
			)
			.reduce(
				(acc, t) =>
					acc + Number(t.amount || 0),
				0
			)
	);

	let remaining = $derived(
		budget - spent
	);

	let percentage = $derived(
		budget <= 0
			? 0
			: Math.min(
					(spent / budget) * 100,
					100
			  )
	);

	let barColor = $derived(() => {
		if (percentage < 20)
			return 'bg-emerald-400';

		if (percentage < 50)
			return 'bg-amber-400';

		if (percentage < 85)
			return 'bg-orange-500';

		return 'bg-rose-500';
	});

	let textStatusColor = $derived(() => {
		if (remaining < 0)
			return 'text-rose-500';

		if (remaining < budget * 0.1)
			return 'text-orange-400';

		return 'text-emerald-400';
	});
</script>

<div class="mt-4">
	<div class="glass-panel relative overflow-hidden rounded-[32px] border border-white/10 p-5">
		<div class="relative z-10 flex flex-col gap-3">

			<div class="flex items-end justify-between">
				<div class="flex flex-col">
					<p class="text-[9px] font-bold tracking-[0.2em] uppercase opacity-40">
						Presupuesto Mensual
					</p>

					<div class="flex items-baseline gap-2">
						<h2 class="text-2xl font-black tracking-tighter">
							{percentage.toFixed(0)}%
						</h2>

						<span class="text-[10px] font-bold uppercase opacity-30">
							utilizado
						</span>
					</div>
				</div>

				<div class="text-right">
					<p class="text-[9px] font-bold uppercase opacity-30">
						Restante
					</p>

					<p class="text-sm font-black transition-colors duration-500 {textStatusColor()}">
						{remaining.toFixed(2)}€
					</p>
				</div>
			</div>

			<div class="relative h-2 w-full overflow-hidden rounded-full bg-white/5">
				<div
					class="h-full transition-all duration-1000 ease-out {barColor()}"
					style="width:{percentage}%"
				>
					<div class="h-full w-full bg-white/20 blur-sm"></div>
				</div>
			</div>

			<div class="flex justify-between text-[9px] font-bold uppercase opacity-40">
				<span>
					{spent.toFixed(2)}€ gastados
				</span>

				<span>
					{investments.toFixed(2)}€ invertidos
				</span>

				<span>
					Meta: {budget}€
				</span>
			</div>

		</div>
	</div>
</div>

<style>
.glass-panel{
	background:rgba(255,255,255,.03);
	backdrop-filter:blur(20px);
	-webkit-backdrop-filter:blur(20px);
}
</style>