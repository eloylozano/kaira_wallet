<script lang="ts">
	type TransactionType = 'expense' | 'income' | 'invest';

	let { value = $bindable<string>(), type = 'expense' as TransactionType } = $props<{
		value: string;
		type?: TransactionType;
	}>();

	let displayValue = $state<string>('');

	// PADRE → INPUT
	$effect(() => {
		if (value === undefined || value === null || value === '') {
			displayValue = '';
			return;
		}

		// asegura formato string limpio
		displayValue = String(value);
	});

	// INPUT → PADRE
	$effect(() => {
		value = displayValue;
	});

	const colors: Record<TransactionType, string> = {
		expense: 'text-red-500',
		income: 'text-emerald-500',
		invest: 'text-blue-500'
	};

	const bgColors: Record<TransactionType, string> = {
		expense: 'bg-red-500/5',
		income: 'bg-emerald-500/5',
		invest: 'bg-blue-500/5'
	};

	function formatToDecimal(val: string): string {
		if (!val) return '';
		const numericValue = Number.parseFloat(val);
		return Number.isNaN(numericValue) ? '' : numericValue.toFixed(2);
	}

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		displayValue = target.value;
	}

	function handleBlur() {
		displayValue = formatToDecimal(displayValue);

		if (typeof navigator !== 'undefined' && navigator.vibrate) {
			navigator.vibrate(5);
		}
	}
</script>

<div
	class="glass-panel relative rounded-[32px] border border-white/10 p-8 transition-colors duration-500 {bgColors[
		type
	]}"
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
			class="amount-input w-3/4 bg-transparent text-center text-6xl font-black placeholder:opacity-10 {colors[
				type
			]}"
		/>

		<span class="text-5xl font-bold opacity-50 {colors[type]}">€</span>
	</div>
</div>

<style>
	.amount-input {
		appearance: none;
		-moz-appearance: textfield;
		border: none !important;
		background: none !important;
		box-shadow: none !important;
		outline: none !important;
		-webkit-tap-highlight-color: transparent;
	}

	.amount-input:focus,
	.amount-input:active,
	.amount-input:focus-visible {
		outline: none !important;
		border: none !important;
		box-shadow: none !important;
	}

	.amount-input::-webkit-outer-spin-button,
	.amount-input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
</style>
