<script lang="ts">
	import { auth } from '$lib/stores/auth';

	// Usamos $state para que Svelte 5 reaccione al cambio
	let pin = $state('');
	let error = $state(false);

	function addNumber(n: string) {
		if (error) error = false;

		if (pin.length < 4) {
			pin += n;
			console.log('PIN actual:', pin); // Para debug
		}

		// Si llegamos a 4, validamos
		if (pin.length === 4) {
			setTimeout(validate, 150);
		}
	}

	function validate() {
		const savedPin = localStorage.getItem('user_pin');

		if (pin === savedPin) {
			auth.unlock();
		} else {
			error = true;
			pin = '';
			setTimeout(() => (error = false), 500);
		}
	}
	function deleteLast() {
		pin = pin.slice(0, -1);
	}
</script>

<div class="z- fixed inset-0 flex items-center justify-center bg-black/40 p-6 backdrop-blur-md">
	<div
		class="glass-card relative flex w-full max-w-sm flex-col items-center overflow-hidden rounded-[40px] border border-white/10 p-10 shadow-2xl"
	>
		<div
			class="pointer-events-none absolute inset-0 bg-gradient-to-b from-white/[0.05] to-transparent"
		></div>

		<div class="mb-6 text-primary">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width="40"
				height="40"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="1.5"
				stroke-linecap="round"
				stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" /></svg
			>
		</div>

		<h2 class="mb-8 text-lg font-bold tracking-tight text-white">Seguridad Kaira</h2>

		<div class="mb-12 flex gap-5 {error ? 'animate-shake' : ''}">
			{#each Array(4) as _, i}
				<div
					class="h-3 w-3 rounded-full border-2 transition-all duration-300
                    {pin.length > i
						? 'scale-125 border-primary bg-primary shadow-[0_0_10px_var(--primary-glow)]'
						: 'border-white/20 bg-white/5'}"
				></div>
			{/each}
		</div>

		<div class="grid grid-cols-3 gap-6">
			{#each ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', 'DEL'] as key}
				<button
					type="button"
					onclick={() => (key === 'DEL' ? deleteLast() : key !== '' && addNumber(key))}
					class="h-16 w-16 text-xl font-medium text-white transition-all active:scale-90
                    {key === ''
						? 'pointer-events-none opacity-0'
						: 'glass-btn flex items-center justify-center rounded-full'}"
				>
					{#if key === 'DEL'}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="20"
							height="20"
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
					{:else}
						{key}
					{/if}
				</button>
			{/each}
		</div>
	</div>
</div>

<style>
	/* Estilos base para simular tu GlassCard */
	.glass-card {
		background: var(--glass-bg, rgba(255, 255, 255, 0.03));
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
	}

	.glass-btn {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.glass-btn:active {
		background: var(--primary);
		border-color: var(--primary);
		box-shadow: 0 0 15px var(--primary-glow);
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
			transform: translateX(-5px);
		}
		75% {
			transform: translateX(5px);
		}
	}
</style>
