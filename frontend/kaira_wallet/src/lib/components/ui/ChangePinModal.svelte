<script lang="ts">
	import { haptics } from '$lib/utils/haptic';
	import { fade, scale } from 'svelte/transition';

	let { isOpen, onTouchOutside, onComplete } = $props();

	let step = $state(1);
	let pin = $state('');
	let oldPinVerified = $state('');
	let error = $state(false);

	const savedPin =
		typeof localStorage !== 'undefined'
			? localStorage.getItem('user_pin') || '1234'
			: '1234';

	function addNumber(n: string) {
		haptics.light();

		if (pin.length < 4) pin += n;

		if (pin.length === 4) {
			setTimeout(validate, 200);
		}
	}

	function validate() {
		if (step === 1) {
			if (pin === savedPin) {
				oldPinVerified = pin;
				pin = '';
				step = 2;
			} else {
				triggerError();
			}
		} else {
			localStorage.setItem('user_pin', pin);
			resetAndClose();
		}
	}

	function triggerError() {
		error = true;
		pin = '';
		setTimeout(() => (error = false), 500);
	}

	function handleBack() {
		if (step === 2) {
			step = 1;
			pin = '';
		} else {
			resetAndClose();
		}
	}

	function resetAndClose() {
		step = 1;
		pin = '';
		onComplete();
	}
</script>

{#if isOpen}
	<div
		transition:fade
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-md"
	>
		<!-- click outside -->
		<button class="absolute inset-0 cursor-default" onclick={onTouchOutside}></button>

		<div
			transition:scale={{ start: 0.9, duration: 300 }}
			class="
            glass-panel relative w-full max-w-sm rounded-[32px] border
            border-white/10 bg-white/5 p-8
            shadow-2xl backdrop-blur-xl
            dark:bg-black/30
        "
		>
			<!-- glow sutil -->
			<div
				class="pointer-events-none absolute inset-0 rounded-[32px] bg-gradient-to-b from-white/10 to-transparent opacity-30"
			></div>

			<div class="relative z-10 mb-8 text-center">
				<h3 class="modal-text text-lg font-bold">
					{step === 1 ? 'Verifica PIN Actual' : 'Nuevo PIN de Acceso'}
				</h3>
				<p class="modal-text mt-1 text-xs tracking-widest uppercase opacity-40">
					{step === 1 ? 'Introduce tu código actual' : 'Elige 4 nuevos dígitos'}
				</p>
			</div>

			<div class="relative z-10 mb-10 flex justify-center gap-4 {error ? 'animate-shake' : ''}">
				{#each Array(4) as _, i}
					<div
						class="
                        h-3 w-3 rounded-full border-2 transition-all
                        {pin.length > i
							? 'border-primary bg-primary shadow-[0_0_12px_var(--primary)]'
							: 'border-white/20 opacity-30'}
                    "
					></div>
				{/each}
			</div>

			<div class="relative z-10 grid grid-cols-3 gap-4">
				{#each ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'BACK', '0', 'DEL'] as key}
					<button
						onclick={() => {
							if (key === 'DEL') pin = pin.slice(0, -1);
							else if (key === 'BACK') handleBack();
							else addNumber(key);
						}}
						class="
                        modal-text glass-button flex h-16
                        w-full items-center
                        justify-center rounded-2xl text-xl
                        transition-all active:scale-90
                    "
					>
						{#if key === 'DEL'}
							<svg
								xmlns="http://www.w3.org/2000/svg"
								width="22"
								height="22"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
								><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z" /><line
									x1="18"
									y1="9"
									x2="12"
									y2="15"
								/><line x1="12" y1="9" x2="18" y2="15" /></svg
							>
						{:else if key === 'BACK'}
							<svg
								xmlns="http://www.w3.org/2000/svg"
								width="22"
								height="22"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"><path d="m15 18-6-6 6-6" /></svg
							>
						{:else}
							{key}
						{/if}
					</button>
				{/each}
			</div>
		</div>
	</div>
{/if}

<style>
	/* Usamos la variable de texto global para que cambie en modo claro */
	.modal-text {
		color: var(--text-main);
	}

	.glass-button {
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.08);
	}

	/* Ajuste para que los botones se vean en modo claro */
	:global([data-theme='light']) .glass-button {
		background: rgba(0, 0, 0, 0.05);
		border: 1px solid rgba(0, 0, 0, 0.08);
	}

	/* Estilo del panel en modo claro */
	:global([data-theme='light']) .glass-panel {
		background-color: rgba(255, 255, 255, 0.95);
		border-color: rgba(0, 0, 0, 0.1);
	}

	.animate-shake {
		animation: shake 0.4s ease-in-out;
	}
	@keyframes shake {
		0%,
		100% {
			transform: translateX(0);
		}
		25% {
			transform: translateX(-6px);
		}
		75% {
			transform: translateX(6px);
		}
	}
</style>
