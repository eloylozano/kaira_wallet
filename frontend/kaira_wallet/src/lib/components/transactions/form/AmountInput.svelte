<script lang="ts">
    import * as Icons from 'lucide-svelte';
    import type { Component } from 'svelte';
    import { iconGroups } from '$lib/data/iconGroups';
    import CalculatorModal from './CalculatorModal.svelte';

    type TransactionType = 'expense' | 'income' | 'invest';

    let { value = $bindable(''), type = 'expense' } = $props<{
        value: string;
        type?: TransactionType;
    }>();

    let displayValue = $state<string>('');
    let showCalc = $state<boolean>(false);

    $effect(() => {
        if (value === undefined || value === null || value === '') {
            displayValue = '';
            return;
        }
        displayValue = String(value);
    });

    $effect(() => {
        value = displayValue;
    });

    const colors: Record<TransactionType, string> = {
        expense: 'text-red-500',
        income: 'text-emerald-500',
        invest: 'text-blue-500'
    };

    const bgColors: Record<TransactionType, string> = {
        expense: 'bg-red-500/5',
        income: 'bg-emerald-500/5',
        invest: 'bg-blue-500/5'
    };

    const safeType = $derived((type ?? 'expense') as TransactionType);

    function formatToDecimal(val: string): string {
        if (!val) return '';
        const numericValue = Number.parseFloat(val);
        return Number.isNaN(numericValue) ? '' : numericValue.toFixed(2);
    }

    function handleInput(e: Event) {
        const target = e.target as HTMLInputElement;
        displayValue = target.value;
    }

    function handleBlur() {
        displayValue = formatToDecimal(displayValue);
        triggerVibrate(5);
    }

    function triggerVibrate(ms: number) {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(ms);
        }
    }

    function openCalculator() {
        showCalc = true;
        triggerVibrate(10);
    }

    function toPascal(str: string) {
        return str
            .split('-')
            .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
            .join('');
    }

    function getIcon(name: string) {
        const key = toPascal(name);
        const iconSet = Icons as unknown as Record<string, Component>;
        return iconSet[key] || Icons.Circle;
    }

    const calculatorIconName = iconGroups.money.includes('calculator') ? 'calculator' : 'circle';
</script>

<div
    class="glass-panel relative rounded-[32px] border border-white/10 p-8 transition-colors duration-500 {bgColors[safeType]}"
>
    <p class="text-center text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Importe</p>

    <div class="mt-2 flex items-center justify-center gap-1">
        <input
            type="number"
            inputmode="decimal"
            step="0.01"
            placeholder="0.00"
            value={displayValue}
            oninput={handleInput}
            onblur={handleBlur}
            class="amount-input w-full bg-transparent text-center text-4xl font-black placeholder:opacity-10 sm:text-6xl {colors[safeType]}"
        />

        <span class="text-3xl font-bold opacity-50 sm:text-5xl {colors[safeType]}">€</span>
    </div>

    <div class="absolute left-4 top-4">
        <button
            type="button"
            onclick={openCalculator}
            class="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-white/5 text-base transition-all active:scale-90 hover:bg-white/10 text-emerald-300"
            title="Abrir calculadora"
        >
            <svelte:component this={getIcon(calculatorIconName)} class="h-4 w-4" />
        </button>
    </div>
</div>

<CalculatorModal bind:open={showCalc} bind:value={displayValue} type={safeType} />

<style>
    .amount-input {
        appearance: none;
        -moz-appearance: textfield;
        border: none !important;
        background: none !important;
        box-shadow: none !important;
        outline: none !important;
        -webkit-tap-highlight-color: transparent;
    }

    .amount-input:focus,
    .amount-input:active,
    .amount-input:focus-visible {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }

    .amount-input::-webkit-outer-spin-button,
    .amount-input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
</style>