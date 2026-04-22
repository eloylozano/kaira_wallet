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
			name: 'Experiencia',
			items: [
				{
					label: 'Vibración al tocar',
					type: 'toggle',
					value: () => useHaptics,
					set: (v: boolean) => {
						useHaptics = v;
						if (v) haptics.light();
					}
				}
			]
		},
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
			name: 'Datos',
			items: [
				{
					label: 'Configurar categorías',
					type: 'action',
					action: () => {
						// luego lo conectas a router o modal
						goto('/categories');
					},
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
			<div class="flex flex-col gap-2">
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

<ChangePinModal isOpen={isPinModalOpen} onComplete={() => (isPinModalOpen = false)} onTouchOutside={() => (isPinModalOpen = false)} />

<ConfirmModal
	isOpen={isConfirmLockOpen}
	title="Seguridad"
	message="¿Quieres bloquear la sesión ahora?"
	confirmText="Bloquear"
	onConfirm={handleLockConfirm}
	onCancel={() => (isConfirmLockOpen = false)}
/>

<ConfirmModal
	isOpen={isConfirmDeleteOpen}
	title="Borrar todo"
	message="Esta acción eliminará todos tus gastos permanentemente. ¿Estás seguro?"
	confirmText="Eliminar permanentemente"
	onConfirm={handleClearAllData}
	onCancel={() => (isConfirmDeleteOpen = false)}
/>

<style>
	h1,
	span {
		color: var(--text-main);
	}

	.ios-header {
		padding-top: var(--safe-area-top);
		padding-left: 0.5rem;
		padding-bottom: 0.5rem;
	}

	.space-y-6 > div {
		animation: slideIn 0.5s ease forwards;
		opacity: 0;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateY(8px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
