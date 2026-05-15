<script lang="ts">
	import { haptics } from '$lib/utils/device/haptic';
	import { fly, fade } from 'svelte/transition';

	interface Option {
		value: string | number;
		label: string;
	}

	let {
		value = $bindable(),
		options = [],
		placeholder = 'Seleccionar...',
		label = ''
	} = $props<{
		value: any;
		options: Option[];
		placeholder?: string;
		label?: string;
	}>();

	let isOpen = $state(false);
	let container: HTMLElement;

	let coords = $state({
		top: 0,
		left: 0,
		width: 0
	});

	let selectedLabel = $derived(
		options.find((opt: Option) => opt.value == value)?.label || placeholder
	);

	function updateCoords() {
		if (!container) return;

		const rect = container.getBoundingClientRect();

		coords = {
			top: rect.bottom + window.scrollY,
			left: rect.left + window.scrollX,
			width: rect.width
		};
	}

	function toggle(e: MouseEvent) {
		e.stopPropagation();

		if (!isOpen) updateCoords();

		haptics.light();
		isOpen = !isOpen;
	}

	function closeDropdown() {
		isOpen = false;
	}

	function selectOption(optValue: string | number, e: MouseEvent) {
		e.stopPropagation();
		value = optValue;
		isOpen = false;
	}
</script>

<!-- SELECT -->
<div class="relative z-20 flex w-full flex-col gap-1.5" bind:this={container}>
	{#if label}
		<span class="ml-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-30">
			{label}
		</span>
	{/if}

	<button
		type="button"
		onclick={toggle}
		class="relative flex h-12 w-full items-center justify-between gap-2 min-w-0
		rounded-[20px] border border-white/10 bg-white/5 px-4
		active:scale-[0.98]
		{isOpen ? 'border-primary/40 ring-4 ring-primary/5' : 'hover:bg-white/10'}"
	>
		<span class="min-w-0 truncate text-[11px] font-black tracking-widest uppercase">
			{selectedLabel}
		</span>

		<svg
			width="14"
			height="14"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="3"
			class="transition-transform {isOpen ? 'rotate-180 text-primary' : 'opacity-40'}"
		>
			<path d="m6 9 6 6 6-6" />
		</svg>
	</button>
</div>

{#if isOpen}
	<!-- BACKDROP -->
	<button
		type="button"
		class="fixed inset-0 z-[9998] bg-black/20 backdrop-blur-[2px]"
		onclick={closeDropdown}
		transition:fade={{ duration: 150 }}
	/>

	<!-- DROPDOWN -->
	<div
		transition:fly={{ y: 8, duration: 200 }}
		style="
			top:{coords.top + 8}px;
			left:{coords.left}px;
			width:{coords.width}px;
		"
		class="fixed z-[9999] box-border
		overflow-hidden rounded-[24px]
		border border-white/15
		bg-[#1c1c1e]/80
		p-1.5
		shadow-[0_20px_50px_rgba(0,0,0,0.6)]
		backdrop-blur-lg"
	>
		<div class="custom-scrollbar max-h-[280px] overflow-y-auto py-1 pb-2 pr-1">
			{#each options as opt}
				<button
					type="button"
					onclick={(e) => selectOption(opt.value, e)}
					class="
						flex w-full items-center justify-between gap-2 min-w-0
						rounded-[14px] px-4 py-3.5
						text-left active:scale-[0.97]
						{value === opt.value
							? 'bg-primary font-black text-black'
							: 'text-white/70 hover:bg-white/5'}
					"
				>
					<span class="min-w-0 truncate text-[10px] font-bold tracking-widest uppercase">
						{opt.label}
					</span>

					{#if value === opt.value}
						✓
					{/if}
				</button>
			{/each}
		</div>
	</div>
{/if}

<style>
	.custom-scrollbar::-webkit-scrollbar {
		width: 4px;
	}

	.custom-scrollbar::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.12);
		border-radius: 10px;
	}

	.custom-scrollbar {
		scrollbar-gutter: stable;
		overscroll-behavior: contain;
	}
</style>
