<script lang="ts">
	let { percent = 0, amount = 0 } = $props<{ percent: number; amount: number }>();

	// Radio del círculo: 106px
	// Perímetro: 2 * Math.PI * 106 ≈ 666
	const circumference = 666;
	
	// Mantenemos el cálculo del offset con el valor original para suavidad
	let offset = $derived(circumference - (percent / 100) * circumference);

	// Formateador para moneda (opcional, pero queda más profesional)
	const formatAmount = (val: number) => {
		return Math.abs(val).toLocaleString('es-ES', {
			minimumFractionDigits: 2,
			maximumFractionDigits: 2
		});
	};
</script>

<div class="relative mx-auto flex h-56 w-56 items-center justify-center rounded-full border-[12px] border-white/5 shadow-[inset_0_0_20px_rgba(0,0,0,0.2)]">
	<div class="text-center">
		<p class="text-[10px] font-black tracking-widest uppercase opacity-40">Ahorro</p>
		<p class="text-5xl font-black italic">{Math.round(percent)}%</p>
		
		<p class="mt-1 text-[11px] font-bold {amount >= 0 ? 'text-primary' : 'text-rose-500'}">
			{amount >= 0 ? '+' : '-'}{formatAmount(amount)}€
		</p>
	</div>

	<svg class="absolute -rotate-90 pointer-events-none" width="224" height="224">
		<circle
			cx="112"
			cy="112"
			r="106"
			fill="none"
			stroke="currentColor"
			stroke-width="12"
			class="text-white/5"
		/>
		<circle
			cx="112"
			cy="112"
			r="106"
			fill="none"
			stroke="currentColor"
			stroke-width="12"
			stroke-dasharray={circumference}
			style="stroke-dashoffset: {offset}; transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);"
			stroke-linecap="round"
			class="text-primary"
		/>
	</svg>
</div>