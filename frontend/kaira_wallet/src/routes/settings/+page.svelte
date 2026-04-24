<script lang="ts">
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
	import GlassCard from '$lib/components/ui/GlassCard.svelte';
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
	let isConfirmBudgetOpen = $state(false); // Nuevo modal
	
	let monthlyBudget = $state<number>(350);
	let tempBudget = $state<number>(350); // Valor temporal mientras se edita

	onMount(() => {
		const saved = localStorage.getItem('monthly_budget');
		if (saved) {
			const val = Number(saved);
			monthlyBudget = val;
			tempBudget = val;
		}
	});

	// Esta función se activa al pulsar el botón de guardar
	function askConfirmBudget() {
		if (useHaptics) haptics.light();
		isConfirmBudgetOpen = true;
	}

	function handleBudgetConfirm() {
		monthlyBudget = tempBudget; // Aplicamos el cambio real
		localStorage.setItem('monthly_budget', monthlyBudget.toString());
		isConfirmBudgetOpen = false;
	}

	function handleLockConfirm() {
		auth.lock();
		isConfirmLockOpen = false;
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
		<h1 class="text-4xl font-black italic uppercase tracking-tight">Ajustes</h1>
	</header>

	<SegmentedControl options={[{ value: 'dark', label: 'Modo Noche' }, { value: 'light', label: 'Modo Claro' }]} bind:selected={$theme} {useHaptics} />

	<div class="space-y-6">
		{#each sections as section}
			<div class="section-anim flex flex-col gap-2">
				<p class="px-3 text-[10px] font-black uppercase tracking-[0.3em] text-primary opacity-70">
					{section.name}
				</p>

				<GlassCard class="overflow-hidden !rounded-[24px]">
					<div class="flex flex-col">
						{#each section.items as item, i}
							<div class="flex items-center justify-between px-4 py-3.5">
								<span class="text-sm font-semibold">{item.label}</span>

								{#if item.type === 'action'}
									<GlassButton
										onclick={() => { item.action(); if (useHaptics) haptics.light(); }}
										text={item.btnText}
										variant={item.variant || 'normal'}
									/>
								{:else if item.type === 'input'}
									<div class="flex items-center gap-3">
										<div class="flex items-center gap-2">
											<span class="text-xs opacity-50">€</span>
											<input
												type="number"
												bind:value={tempBudget}
												class="w-20 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-right text-sm font-bold text-white/90 outline-none transition focus:border-white/20"
											/>
											
											{#if tempBudget !== monthlyBudget}
												<GlassButton 
													text="Guardar" 
													onclick={askConfirmBudget} 
													class="!px-3 !py-1.5 !text-[10px]" 
												/>
											{/if}
										</div>
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

<ConfirmModal 
    isOpen={isConfirmBudgetOpen}
    title="¿Actualizar presupuesto?"
    message="El nuevo límite mensual será de {tempBudget}€."
    confirmText="Actualizar"
    onConfirm={handleBudgetConfirm}
    onCancel={() => {
        isConfirmBudgetOpen = false;
        tempBudget = monthlyBudget; // Revertimos el cambio visual
    }}
/>

<ChangePinModal isOpen={isPinModalOpen} onComplete={() => isPinModalOpen = false} onTouchOutside={() => isPinModalOpen = false} />
<ConfirmModal isOpen={isConfirmLockOpen} title="¿Bloquear sesión?" confirmText="Bloquear" onConfirm={handleLockConfirm} onCancel={() => isConfirmLockOpen = false} />

<style>
	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
	input[type='number'] { -moz-appearance: textfield; }
</style>