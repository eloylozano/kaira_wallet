<script lang="ts">
	interface Option {
		value: string | number | boolean;
		label: string;
		color?: string; // Ej: '#ef4444' para gastos
	}

	let {
		options,
		selected = $bindable(),
		useHaptics = true
	} = $props<{
		options: Option[];
		selected: Option['value'];
		useHaptics?: boolean;
	}>();

	const vibrate = () => {
		if (useHaptics && typeof navigator !== 'undefined' && navigator.vibrate) {
			navigator.vibrate(10);
		}
	};

	let activeIndex = $derived(options.findIndex((o) => o.value === selected));
	let widthPercent = $derived(100 / options.length);
	let activeColor = $derived(options[activeIndex]?.color ?? 'var(--primary)');

	// Función para oscurecer el fondo del indicador y que el texto resalte
	function darken(hex: string, amount = 40) {
		if (!hex?.startsWith('#')) return hex;
		const num = parseInt(hex.slice(1), 16);
		let r = Math.max(0, (num >> 16) - amount);
		let g = Math.max(0, ((num >> 8) & 0x00ff) - amount);
		let b = Math.max(0, (num & 0x0000ff) - amount);
		return `rgb(${r}, ${g}, ${b})`;
	}
</script>

<div
	class="relative isolate flex w-full overflow-hidden rounded-2xl border border-[color:var(--glass-border)] p-1"
>
	<!-- INDICADOR -->
	<div
		class="absolute top-1 bottom-1 left-1 z-0 rounded-xl transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
		style="
			width: calc(100% / {options.length} - 4px);
			left: calc((100% / {options.length}) * {activeIndex});
			background: {darken(activeColor)};
			box-shadow: 0 8px 24px {activeColor}40;
		"
	></div>

	<!-- OPTIONS -->
	{#each options as opt}
		<button
			type="button"
			onclick={() => {
				selected = opt.value;
				vibrate();
			}}
			class="relative z-10 flex flex-1 items-center justify-center py-3 text-[10px] font-black tracking-widest uppercase transition-colors duration-300
		{selected === opt.value
				? 'text-[color:var(--text-main)]'
				: 'text-[color:var(--text-soft)] hover:text-[color:var(--text-muted)]'}"
		>
			{opt.label}
		</button>
	{/each}
</div>

<style>
	button {
		-webkit-tap-highlight-color: transparent;
	}

	.kaira-segment-inactive {
		color: var(--text-soft);
	}
</style>
