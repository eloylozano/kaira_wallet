<script lang="ts">
	let { value = $bindable(), type = 'expense' } = $props();

	// Estado interno para el input
	let displayValue = $state(value ? parseFloat(value).toFixed(2) : '');

	// 1. Sincroniza hacia AFUERA: cuando escribes, actualizas el 'amount' del padre
	$effect(() => {
		value = displayValue;
	});

	// 2. Sincroniza hacia ADENTRO: cuando el padre hace amount = '', el input se limpia
	$effect(() => {
		if (value === '' && displayValue !== '') {
			displayValue = '';
		}
	});

	const colors = {
		expense: 'text-red-500',
		income: 'text-emerald-500',
		invest: 'text-blue-500'
	};

	const bgColors = {
		expense: 'bg-red-500/5',
		income: 'bg-emerald-500/5',
		invest: 'bg-blue-500/5'
	};

	function formatToDecimal(val: string) {
		if (!val) return '';
		const numericValue = parseFloat(val);
		return isNaN(numericValue) ? '' : numericValue.toFixed(2);
	}

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		displayValue = target.value;
	}

	function handleBlur() {
		displayValue = formatToDecimal(displayValue);
		// Vibración sutil
		if (typeof navigator !== 'undefined' && navigator.vibrate) {
			navigator.vibrate(5);
		}
	}
</script>

<div
	class="glass-panel relative rounded-[32px] border border-white/10 p-8 transition-colors duration-500 {bgColors[type]}"
>
	<p class="text-center text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Importe</p>
	<div class="mt-2 flex items-center justify-center gap-1">
		<input
			type="number"
			inputmode="decimal"
			step="0.01"
			placeholder="0.00"
			value={displayValue}
			oninput={handleInput}
			onblur={handleBlur}
			class="amount-input w-3/4 bg-transparent text-center text-6xl font-black placeholder:opacity-10 {colors[type]}"
		/>
		<span class="text-5xl font-bold opacity-50 {colors[type]}">€</span>
	</div>
</div>

<style>
	/* Eliminamos cualquier estilo por defecto del navegador */
	.amount-input {
		appearance: none;
		-moz-appearance: textfield;
		border: none !important;
		background: none !important;
		box-shadow: none !important;
		outline: none !important;
		/* Importante: evita el recuadro azul en Chrome/Android */
		-webkit-tap-highlight-color: transparent; 
	}

	/* Quitamos el borde de enfoque (focus ring) */
	.amount-input:focus,
	.amount-input:active,
	.amount-input:focus-visible {
		outline: none !important;
		border: none !important;
		box-shadow: none !important;
	}

	/* Ocultar las flechas (spinners) */
	.amount-input::-webkit-outer-spin-button,
	.amount-input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
</style>