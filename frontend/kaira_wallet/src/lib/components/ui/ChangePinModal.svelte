<script lang="ts">
    import { fade, scale } from 'svelte/transition';
    let { isOpen, onTouchOutside, onComplete } = $props();

    let step = $state(1); // 1: PIN actual, 2: Nuevo PIN
    let pin = $state('');
    let oldPinVerified = $state('');
    let error = $state(false);

    const savedPin = typeof localStorage !== 'undefined' ? localStorage.getItem('user_pin') || '1234' : '1234';

    function addNumber(n: string) {
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
            onComplete(); // Cerramos el modal
        }
    }

    function triggerError() {
        error = true;
        pin = '';
        setTimeout(() => error = false, 500);
    }
</script>

{#if isOpen}
<div transition:fade class="fixed inset-0 z- flex items-end sm:items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <button class="absolute inset-0 cursor-default" onclick={onTouchOutside}></button>

    <div transition:scale={{start: 0.9, duration: 300}} 
         class="glass-panel relative w-full max-w-sm rounded-[32px] p-8 border border-white/10 shadow-2xl bg-[#020617]/90 mb-10 sm:mb-0">
        
        <div class="text-center mb-8">
            <h3 class="text-white font-bold text-lg">
                {step === 1 ? 'Verifica PIN Actual' : 'Nuevo PIN de Acceso'}
            </h3>
            <p class="text-white/40 text-xs mt-1 uppercase tracking-widest">
                {step === 1 ? 'Introduce tu código actual' : 'Elige 4 nuevos dígitos'}
            </p>
        </div>

        <div class="flex justify-center gap-4 mb-10 {error ? 'animate-shake' : ''}">
            {#each Array(4) as _, i}
                <div class="h-3 w-3 rounded-full border-2 transition-all 
                    {pin.length > i ? 'bg-primary border-primary shadow-[0_0_10px_var(--primary-glow)]' : 'border-white/20'}">
                </div>
            {/each}
        </div>

        <div class="grid grid-cols-3 gap-4">
            {#each ['1','2','3','4','5','6','7','8','9','','0','DEL'] as key}
                <button 
                    onclick={() => key === 'DEL' ? pin = pin.slice(0, -1) : (key !== '' && addNumber(key))}
                    class="h-14 w-full text-xl text-white glass-button rounded-2xl flex items-center justify-center active:bg-primary transition-colors"
                >
                    {#if key === 'DEL'}
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/></svg>
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
    .glass-button { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
    .animate-shake { animation: shake 0.4s ease-in-out; }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-6px); }
        75% { transform: translateX(6px); }
    }
</style>