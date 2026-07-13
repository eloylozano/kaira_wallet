<script lang="ts">
    import * as Icons from 'lucide-svelte';
    import type { Component } from 'svelte';
    import { iconGroups } from '$lib/data/iconGroups';

    type TransactionType = 'expense' | 'income' | 'invest';

    let { open = $bindable(false), value = $bindable(''), type = 'expense' } = $props<{
        open: boolean;
        value: string;
        type?: TransactionType;
    }>();

    let calcScreen = $state<string>('0');
    let prevValue = $state<number | null>(null);
    let activeOperator = $state<string | null>(null);
    let resetScreenOnNextKey = $state<boolean>(false);

    const accentText: Record<TransactionType, string> = {
        expense: 'text-rose-400',
        income: 'text-emerald-400',
        invest: 'text-sky-400'
    };

    const accentRing: Record<TransactionType, string> = {
        expense: 'ring-rose-400/30',
        income: 'ring-emerald-400/30',
        invest: 'ring-sky-400/30'
    };

    const safeType = $derived((type ?? 'expense') as TransactionType);

    $effect(() => {
        if (!open) return;

        calcScreen = value && value !== '' ? String(Number.parseFloat(value) || 0) : '0';
        prevValue = null;
        activeOperator = null;
        resetScreenOnNextKey = false;
    });

    function formatToDecimal(val: string): string {
        if (!val) return '';
        const numericValue = Number.parseFloat(val);
        return Number.isNaN(numericValue) ? '' : numericValue.toFixed(2);
    }

    function triggerVibrate(ms: number) {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(ms);
        }
    }

    function handleNum(num: string) {
        triggerVibrate(5);
        if (calcScreen === '0' || resetScreenOnNextKey) {
            calcScreen = num;
            resetScreenOnNextKey = false;
        } else {
            if (num === '.' && calcScreen.includes('.')) return;
            calcScreen += num;
        }
    }

    function handleOp(op: string) {
        triggerVibrate(10);
        const current = Number.parseFloat(calcScreen) || 0;

        if (activeOperator && !resetScreenOnNextKey) {
            calculate();
        } else {
            prevValue = current;
        }

        activeOperator = op;
        resetScreenOnNextKey = true;
    }

    function calculate() {
        if (!activeOperator || prevValue === null) return;

        const current = Number.parseFloat(calcScreen) || 0;
        let result = 0;

        switch (activeOperator) {
            case '+':
                result = prevValue + current;
                break;
            case '-':
                result = prevValue - current;
                break;
            case '*':
                result = prevValue * current;
                break;
            case '/':
                result = current !== 0 ? prevValue / current : 0;
                break;
        }

        calcScreen = String(Math.round(result * 100) / 100);
        prevValue = result;
        activeOperator = null;
        resetScreenOnNextKey = true;
    }

    function handleEqual() {
        triggerVibrate(15);
        calculate();
        activeOperator = null;
        resetScreenOnNextKey = true;
    }

    function clearCalc() {
        triggerVibrate(10);
        calcScreen = '0';
        prevValue = null;
        activeOperator = null;
        resetScreenOnNextKey = false;
    }

    function deleteLastDigit() {
        triggerVibrate(5);
        if (calcScreen.length > 1) {
            calcScreen = calcScreen.slice(0, -1);
        } else {
            calcScreen = '0';
        }
    }

    function applyCalculatedValue() {
        triggerVibrate(20);
        value = formatToDecimal(calcScreen);
        open = false;
    }

    function closeCalculator() {
        triggerVibrate(5);
        open = false;
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

{#if open}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 px-4 backdrop-blur-sm">
        <div class="w-full max-w-xs overflow-hidden rounded-[2.5rem] border border-white/10 bg-[#121212]/95 p-6 shadow-[0_25px_80px_rgba(0,0,0,0.45)]">
            <div class="flex items-center justify-between pb-4">
                <div class="flex items-center gap-3">
                    <div class="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-white">
                        <svelte:component this={getIcon(calculatorIconName)} class="h-5 w-5" />
                    </div>
                    <div>
                        <p class="text-[10px] font-black uppercase tracking-[0.32em] text-white/40">Calculadora</p>
                        <p class="text-sm font-semibold text-white/80">Ajusta el importe</p>
                    </div>
                </div>
                <button
                    type="button"
                    onclick={closeCalculator}
                    class="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-sm font-semibold text-white/60 transition hover:bg-white/10 hover:text-white"
                >
                    ✕
                </button>
            </div>

            <div class="mb-4 rounded-[1.5rem] border border-white/10 bg-black/25 p-4 text-right">
                <div class="mb-1 h-5 text-xs font-semibold uppercase tracking-[0.2em] text-white/30">
                    {prevValue !== null ? `${prevValue} ${activeOperator || ''}` : ''}
                </div>
                <div class="overflow-hidden text-ellipsis whitespace-nowrap text-3xl font-black text-white">
                    {calcScreen}
                </div>
            </div>

            <div class="grid grid-cols-4 gap-2">
                <button type="button" onclick={clearCalc} class="calc-btn bg-white/5 text-rose-400">C</button>
                <button type="button" onclick={deleteLastDigit} class="calc-btn bg-white/5 text-white/70">⌫</button>
                <button type="button" onclick={() => handleOp('/')} class="calc-btn bg-white/5 text-emerald-400 {activeOperator === '/' ? 'ring-1 ring-inset ' + accentRing[safeType] : ''}">÷</button>
                <button type="button" onclick={() => handleOp('*')} class="calc-btn bg-white/5 text-emerald-400 {activeOperator === '*' ? 'ring-1 ring-inset ' + accentRing[safeType] : ''}">×</button>

                <button type="button" onclick={() => handleNum('7')} class="calc-btn bg-white/5">7</button>
                <button type="button" onclick={() => handleNum('8')} class="calc-btn bg-white/5">8</button>
                <button type="button" onclick={() => handleNum('9')} class="calc-btn bg-white/5">9</button>
                <button type="button" onclick={() => handleOp('-')} class="calc-btn bg-white/5 text-emerald-400 {activeOperator === '-' ? 'ring-1 ring-inset ' + accentRing[safeType] : ''}">−</button>

                <button type="button" onclick={() => handleNum('4')} class="calc-btn bg-white/5">4</button>
                <button type="button" onclick={() => handleNum('5')} class="calc-btn bg-white/5">5</button>
                <button type="button" onclick={() => handleNum('6')} class="calc-btn bg-white/5">6</button>
                <button type="button" onclick={() => handleOp('+')} class="calc-btn bg-white/5 text-emerald-400 {activeOperator === '+' ? 'ring-1 ring-inset ' + accentRing[safeType] : ''}">+</button>

                <button type="button" onclick={() => handleNum('1')} class="calc-btn bg-white/5">1</button>
                <button type="button" onclick={() => handleNum('2')} class="calc-btn bg-white/5">2</button>
                <button type="button" onclick={() => handleNum('3')} class="calc-btn bg-white/5">3</button>
                <button type="button" onclick={handleEqual} class="calc-btn bg-emerald-500 font-black text-black">=</button>

                <button type="button" onclick={() => handleNum('0')} class="calc-btn col-span-2 bg-white/5">0</button>
                <button type="button" onclick={() => handleNum('.')} class="calc-btn bg-white/5">.</button>
                <button type="button" onclick={applyCalculatedValue} class="calc-btn bg-white/10 font-bold text-white" title="Aplicar valor">⏎</button>
            </div>
        </div>
    </div>
{/if}

<style>
    .calc-btn {
        display: flex;
        height: 3.25rem;
        align-items: center;
        justify-content: center;
        border-radius: 1rem;
        font-size: 1.125rem;
        font-weight: 700;
        color: white;
        transition-property: all;
        transition-duration: 100ms;
    }

    .calc-btn:active {
        transform: scale(0.92);
    }
</style>
