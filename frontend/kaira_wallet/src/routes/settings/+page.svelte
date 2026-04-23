<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import GlassCard from '$lib/components/ui/GlassCard.svelte';
	import GlassToggle from '$lib/components/ui/GlassToggle.svelte';
	import GlassButton from '$lib/components/ui/GlassButton.svelte';
	import ChangePinModal from '$lib/components/ui/ChangePinModal.svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	const haptics = {
		light: () => {
			if (typeof navigator !== 'undefined' && navigator.vibrate) {
				navigator.vibrate(10);
			}
		}
	};

	let useHaptics = $state(true);
	let isPinModalOpen = $state(false);
	let isConfirmLockOpen = $state(false);
	let isConfirmDeleteOpen = $state(false);
	let monthlyBudget = $state<number>(350);
	// Mapeamos los temas al formato que espera el componente
	const themeOptions = [
		{ value: 'dark', label: 'Modo Noche' },
		{ value: 'light', label: 'Modo Claro' }
	];

	function handleLockConfirm() {
		auth.lock();
		isConfirmLockOpen = false;
	}

	function handleClearAllData() {
		isConfirmDeleteOpen = false;
		if (useHaptics) haptics.light();
	}

	const sections = [
		{
			name: 'Seguridad',
			items: [
				{
					label: 'PIN de acceso',
					type: 'action',
					action: () => (isPinModalOpen = true),
					btnText: 'Cambiar'
				},
				{
					label: 'Bloquear sesión',
					type: 'action',
					variant: 'danger',
					action: () => (isConfirmLockOpen = true),
					btnText: 'Bloquear'
				}
			]
		},

		{
			name: 'Finanzas',
			items: [
				{
					label: 'Presupuesto mensual',
					type: 'input'
				}
			]
		},

		{
			name: 'Datos',
			items: [
				{
					label: 'Configurar categorías',
					type: 'action',
					action: () => goto('/categories'),
					btnText: 'Configurar'
				},
				{
					label: 'Exportar historial (CSV)',
					type: 'action',
					action: () => {
						if (useHaptics) haptics.light();
					},
					btnText: 'Exportar'
				},
				{
					label: 'Borrar todos los gastos',
					type: 'action',
					variant: 'danger',
					action: () => (isConfirmDeleteOpen = true),
					btnText: 'Borrar todo'
				}
			]
		}
	];
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6">
	<header class="ios-header">
		<h1 class="text-4xl font-black tracking-tight uppercase italic">Ajustes</h1>
	</header>

	<SegmentedControl options={themeOptions} bind:selected={$theme} {useHaptics} />

	<div class="space-y-6">
		{#each sections as section}
			<div class="section-anim flex flex-col gap-2">
				<p class="px-3 text-[10px] font-black tracking-[0.3em] text-primary uppercase opacity-70">
					{section.name}
				</p>

				<GlassCard class="overflow-hidden !rounded-[24px]">
					<div class="flex flex-col">
						{#each section.items as item, i}
							<div class="flex items-center justify-between px-4 py-3.5 transition-all">
								<div class="flex items-center gap-3">
									<span class="text-sm leading-tight font-semibold tracking-tight sm:text-base">
										{item.label}
									</span>
								</div>

								{#if item.type === 'toggle'}
									<GlassToggle
										checked={item.value()}
										onchange={(v) => {
											item.set(v);
											if (useHaptics) haptics.light();
										}}
									/>
								{:else if item.type === 'action'}
									<GlassButton
										onclick={() => {
											item.action();
											if (useHaptics) haptics.light();
										}}
										text={item.btnText || 'Ejecutar'}
										variant={item.variant || 'normal'}
									/>
								{:else if item.type === 'input'}
									<div class="flex items-center gap-3">
										<span class="text-xs opacity-50">€</span>

										<input
											type="number"
											bind:value={monthlyBudget}
											min="0"
											class="w-16 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-right
               text-sm font-bold text-white/90 transition
               outline-none focus:border-white/20 focus:bg-white/10 focus:ring-0"
											oninput={() => {
												if (useHaptics) haptics.light();
											}}
										/>
									</div>
								{/if}
							</div>

							{#if i < section.items.length - 1}
								<div class="mx-4 h-[1px] bg-current opacity-5"></div>
							{/if}
						{/each}
					</div>
				</GlassCard>
			</div>
		{/each}
	</div>
</div>

<style>
	/* Chrome, Safari, Edge */
	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	/* Firefox */
	input[type='number'] {
		-moz-appearance: textfield;
	}
</style>
