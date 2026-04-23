<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { haptics } from '$lib/utils/haptic';
	let pin = $state('');
	let error = $state(false);
	let inputElement: HTMLInputElement;

	// Función auxiliar para vibrar sin complicaciones
	const vibrate = (ms: number | number[]) => {
		if (typeof navigator !== 'undefined' && navigator.vibrate) {
			navigator.vibrate(ms);
		}
	};

	$effect(() => {
		if (inputElement) {
			setTimeout(() => inputElement.focus(), 100);
		}
	});

	function addNumber(n: string) {
		if (error) error = false;

		haptics.tap();

		if (pin.length < 4) {
			pin += n;
		}

		if (pin.length === 4) {
			validate(); // sin delay si quieres haptics fiable
		}
	}

	function validate() {
		const savedPin = localStorage.getItem('user_pin') || '1234';

		if (pin === savedPin) {
			haptics.success();
			auth.unlock();
		} else {
			error = true;
			pin = '';

			haptics.error();

			setTimeout(() => (error = false), 500);
		}
	}

	function deleteLast() {
		vibrate(10); // Vibración sutil al borrar
		pin = pin.slice(0, -1);
	}
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6 backdrop-blur-md">
	<form class="absolute h-1 w-1 overflow-hidden opacity-0" onsubmit={(e) => e.preventDefault()}>
		<input
			bind:this={inputElement}
			type="password"
			autocomplete="current-password"
			value={pin}
			readonly
		/>
	</form>

	<div
		class="glass-panel relative flex w-full max-w-sm flex-col items-center rounded-[40px] border border-white/10 bg-[#020617]/90 p-10 shadow-2xl transition-all duration-500"
	>
		<div
			class="pointer-events-none absolute inset-0 rounded-[40px] bg-gradient-to-b from-white/[0.05] to-transparent"
		></div>

		<div class="relative mb-10 flex flex-col items-center">
			<div class="absolute -top-6 h-28 w-28 rounded-full bg-primary/20 blur-3xl"></div>

			<div
				class="relative flex h-20 w-20 items-center justify-center rounded-[28px] border border-white/10 bg-white/5 shadow-inner"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="32"
					height="32"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="1.5"
					class="text-primary drop-shadow-[0_0_8px_rgba(var(--primary-rgb),0.5)]"
				>
					<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" />
				</svg>
			</div>

			<h2 class="mt-4 text-xl font-black tracking-tighter text-white uppercase italic">Kaira</h2>
			<div class="flex items-center gap-1.5 opacity-30">
				<span class="h-1 w-1 animate-pulse rounded-full bg-primary"></span>
				<p class="text-[8px] font-black tracking-[0.4em] uppercase">Secure</p>
			</div>
		</div>

		<div class="mb-12 flex gap-4 {error ? 'animate-shake' : ''}">
			{#each Array(4) as _, i}
				<div
					class="h-2.5 w-2.5 rounded-full border transition-all duration-300
                    {pin.length > i
						? 'scale-125 border-primary bg-primary shadow-[0_0_10px_var(--primary-glow)]'
						: 'border-white/20'}"
				></div>
			{/each}
		</div>

		<div class="grid grid-cols-3 gap-6">
			{#each ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', 'DEL'] as key}
				<button
					type="button"
					onclick={() => (key === 'DEL' ? deleteLast() : key !== '' && addNumber(key))}
					class="h-16 w-16 text-xl font-light transition-all active:scale-90
                    {key === ''
						? 'pointer-events-none opacity-0'
						: 'flex items-center justify-center rounded-full border border-white/[0.05] bg-white/[0.03] hover:bg-white/[0.08]'}"
				>
					{#if key === 'DEL'}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="18"
							height="18"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
						>
							<path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z" />
							<line x1="18" y1="9" x2="12" y2="15" /><line x1="12" y1="9" x2="18" y2="15" />
						</svg>
					{:else}
						{key}
					{/if}
				</button>
			{/each}
		</div>
	</div>
</div>

<style>
	.pin-text {
		color: var(--text-main);
	}

	.glass-btn-pin {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		-webkit-tap-highlight-color: transparent;
		/* Evita selección de texto al pulsar rápido */
		-webkit-user-select: none;
	}

	:global([data-theme='light']) .glass-btn-pin {
		background: rgba(0, 0, 0, 0.05);
		border: 1px solid rgba(0, 0, 0, 0.08);
	}

	.glass-btn-pin:active {
		background: var(--primary) !important;
		color: white !important;
	}
	button:active {
		transform: scale(0.96);
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
