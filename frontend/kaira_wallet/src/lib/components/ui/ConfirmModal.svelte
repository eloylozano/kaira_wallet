<script lang="ts">
	import { fade, scale } from 'svelte/transition';

	let { isOpen, title, message, confirmText, onConfirm, onCancel } = $props();
</script>

{#if isOpen}
	<div
		transition:fade={{ duration: 200 }}
		class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 p-6 backdrop-blur-sm"
	>
		<button class="absolute inset-0 cursor-default" onclick={onCancel}></button>

		<div
			transition:scale={{ start: 0.9, duration: 200 }}
			class="glass-panel relative w-full max-w-[320px] overflow-hidden rounded-[32px] border border-white/10 bg-[#1c1c1e]/90 shadow-2xl"
		>
			<div class="p-8 text-center">
				<h3 class="text-xl font-bold text-white">{title}</h3>
				{#if message}
					<p class="mt-3 text-sm leading-relaxed text-white/60">{message}</p>
				{/if}
			</div>

			<div class="flex flex-col border-t border-white/5">
				<button
					onclick={onConfirm}
					class="w-full border-b border-white/5 py-4 text-base font-bold text-rose-500 transition-colors active:bg-white/10"
				>
					{confirmText}
				</button>

				<button
					onclick={onCancel}
					class="w-full py-4 text-base font-medium text-white/50 transition-colors active:bg-white/10"
				>
					Cancelar
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.glass-panel {
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
	}
</style>
