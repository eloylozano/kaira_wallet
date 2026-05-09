<script lang="ts">
    import { theme } from '$lib/stores/ui/theme';
    import GlassButton from '$lib/components/ui/core/GlassButton.svelte';
    import ChangePinModal from '$lib/components/settings/ChangePinModal.svelte';
    import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
    import GlassCard from '$lib/components/ui/core/GlassCard.svelte';
    import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';

    import { auth } from '$lib/stores/session/auth';
    import { settingsStore } from '$lib/stores/domain/settings.svelte';
    import { investmentStore } from '$lib/stores/domain/investments.svelte';
    import { getSettingsSections } from '$lib/data/settings.data';

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
    let isConfirmTargetOpen = $state(false);

    let tempBudget = $state<number>(settingsStore.monthlyBudget);
    let tempTarget = $state<number>(investmentStore.targetSavings);

    $effect(() => { tempBudget = settingsStore.monthlyBudget; });
    $effect(() => { tempTarget = investmentStore.targetSavings; });

    function handleBudgetConfirm() {
        settingsStore.updateBudget(Number(tempBudget));
        isConfirmBudgetOpen = false;
    }

    function handleTargetConfirm() {
        investmentStore.updateTarget(Number(tempTarget));
        isConfirmTargetOpen = false;
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
            () => {} 
        )
    );
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 px-4 md:px-0">
    <header class="pt-6">
        <h1 class="text-4xl font-black tracking-tighter text-white uppercase italic">Ajustes</h1>
    </header>

    <SegmentedControl
        options={[
            { value: 'dark', label: 'Modo Noche' },
            { value: 'light', label: 'Modo Claro' }
        ]}
        bind:selected={$theme}
        {useHaptics}
    />

    <div class="space-y-8 pb-10">
        {#each sections as section}
            <div class="section-anim flex flex-col gap-2">
                <p class="px-3 text-[10px] font-black tracking-[0.3em] text-white uppercase opacity-50">
                    {section.name}
                </p>

                <GlassCard class="overflow-hidden !rounded-[24px]">
                    <div class="flex flex-col">
                        {#each section.items as item, i}
                            <div class="flex items-center justify-between px-4 py-3.5">
                                <div class="flex flex-col">
                                    <span class="text-sm font-semibold">{item.label}</span>
                                    {#if item.type === 'target'}
                                        <!-- <span class="text-[9px] font-black tracking-widest uppercase text-emerald-400/60">Libertad Financiera</span> -->
                                    {/if}
                                </div>

                                {#if item.type === 'action'}
                                    <GlassButton
                                        onclick={item.action}
                                        text={item.btnText}
                                        variant={item.variant || 'normal'}
                                    />
                                {:else if item.type === 'budget'}
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs font-bold opacity-50">€</span>
                                        <input type="number" bind:value={tempBudget} class="kaira-input-settings" />
                                        {#if tempBudget !== settingsStore.monthlyBudget}
                                            <GlassButton text="Guardar" onclick={() => (isConfirmBudgetOpen = true)} />
                                        {/if}
                                    </div>
                                {:else if item.type === 'target'}
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs font-bold opacity-50 text-white">€</span>
                                        <input type="number" bind:value={tempTarget} class="kaira-input-settings focus:border-emerald-500/50" />
                                        {#if tempTarget !== investmentStore.targetSavings}
                                            <GlassButton text="Meta" onclick={() => (isConfirmTargetOpen = true)} />
                                        {/if}
                                    </div>
                                {/if}
                            </div>

                            {#if i < section.items.length - 1}
                                <div class="mx-4 h-[1px] bg-white opacity-5"></div>
                            {/if}
                        {/each}
                    </div>
                </GlassCard>
            </div>
        {/each}
    </div>
</div>

<ConfirmModal
    isOpen={isConfirmTargetOpen}
    title="¿Cambiar objetivo anual?"
    message="Tu nueva meta de independencia para diciembre será de {tempTarget?.toLocaleString()}€."
    confirmText="Confirmar Meta"
    onConfirm={handleTargetConfirm}
    onCancel={() => ((tempTarget = investmentStore.targetSavings), (isConfirmTargetOpen = false))}
/>

<ConfirmModal
    isOpen={isConfirmBudgetOpen}
    title="¿Actualizar presupuesto?"
    message="El nuevo límite de gasto mensual será de {tempBudget}€."
    confirmText="Actualizar"
    onConfirm={handleBudgetConfirm}
    onCancel={() => ((tempBudget = settingsStore.monthlyBudget), (isConfirmBudgetOpen = false))}
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
    @reference "tailwindcss";

    .kaira-input-settings {
        @apply w-28 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-right text-sm font-black text-white transition-all outline-none focus:border-white/40 focus:bg-white/10 focus:ring-0;
    }

    input[type='number']::-webkit-outer-spin-button,
    input[type='number']::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    input[type='number'] {
        -moz-appearance: textfield;
    }
</style>