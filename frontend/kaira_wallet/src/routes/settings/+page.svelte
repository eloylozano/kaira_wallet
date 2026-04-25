<script lang="ts">
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';
	import GlassButton from '$lib/components/ui/core/GlassButton.svelte';
	import ChangePinModal from '$lib/components/ui/ChangePinModal.svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
	import GlassCard from '$lib/components/ui/core/GlassCard.svelte';
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';

	import { auth } from '$lib/stores/auth';
	import { settingsStore } from '$lib/stores/settings.svelte';
	import { getSettingsSections } from '$lib/data/settings.data';

	type SectionItem =
		| {
				label: string;
				type: 'action';
				btnText: string;
				action: () => void;
				variant?: 'normal' | 'danger';
		  }
		| {
				label: string;
				type: 'input';
		  };

	type Section = {
		name: string;
		items: SectionItem[];
	};

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
	let isConfirmBudgetOpen = $state(false);
	let isConfirmDeleteOpen = $state(false);

	let tempBudget = $state<number>(settingsStore.monthlyBudget);

	$effect(() => {
		tempBudget = settingsStore.monthlyBudget;
	});

	function askConfirmBudget() {
		if (useHaptics) haptics.light();
		isConfirmBudgetOpen = true;
	}

	function handleBudgetConfirm() {
		settingsStore.updateBudget(Number(tempBudget));
		isConfirmBudgetOpen = false;
	}

	function handleLockConfirm() {
		auth.lock();
		isConfirmLockOpen = false;
	}

	let sections = $derived(
		getSettingsSections(
			useHaptics,
			(v) => (isPinModalOpen = v),
			(v) => (isConfirmLockOpen = v),
			(v) => (isConfirmDeleteOpen = v)
		)
	);
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6">
	<header class="ios-header">
		<h1 class="text-4xl font-black tracking-tight uppercase italic">Ajustes</h1>
	</header>

	<SegmentedControl
		options={[
			{ value: 'dark', label: 'Modo Noche' },
			{ value: 'light', label: 'Modo Claro' }
		]}
		bind:selected={$theme}
		{useHaptics}
	/>

	<div class="space-y-6">
		{#each sections as section}
			<div class="section-anim flex flex-col gap-2">
				<p class="px-3 text-[10px] font-black tracking-[0.3em] text-primary uppercase opacity-70">
					{section.name}
				</p>

				<GlassCard class="overflow-hidden !rounded-[24px]">
					<div class="flex flex-col">
						{#each section.items as item, i}
							<div class="flex items-center justify-between px-4 py-3.5">
								<span class="text-sm font-semibold">
									{item.label}
								</span>

								{#if item.type === 'action'}
									<GlassButton
										onclick={item.action}
										text={item.btnText}
										variant={item.variant || 'normal'}
									/>
								{:else if item.type === 'budget'}
									<div class="flex items-center gap-2">
										<span class="text-xs opacity-50">€</span>

										<input
											type="number"
											bind:value={tempBudget}
											class="w-24 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-right text-sm font-bold text-white transition-all outline-none focus:border-white/40 focus:ring-0 focus:outline-none"
										/>
										{#if tempBudget !== settingsStore.monthlyBudget}
											<GlassButton text="Guardar" onclick={askConfirmBudget} />
										{/if}
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
		tempBudget = settingsStore.monthlyBudget;
	}}
/>

<ChangePinModal
	isOpen={isPinModalOpen}
	onComplete={() => (isPinModalOpen = false)}
	onTouchOutside={() => (isPinModalOpen = false)}
/>

<ConfirmModal
	isOpen={isConfirmLockOpen}
	title="¿Bloquear sesión?"
	confirmText="Bloquear"
	onConfirm={handleLockConfirm}
	onCancel={() => (isConfirmLockOpen = false)}
/>

<style>
	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	input[type='number'] {
		-moz-appearance: textfield;
	}
</style>
