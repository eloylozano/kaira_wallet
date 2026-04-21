<script lang="ts">
    import { auth } from '$lib/stores/auth';
    import { theme } from '$lib/stores/theme'; // Importamos el tema para los colores

    let pin = $state('');
    let error = $state(false);

    function addNumber(n: string) {
        if (error) error = false;
        if (pin.length < 4) {
            pin += n;
        }

        if (pin.length === 4) {
            setTimeout(validate, 200);
        }
    }

    function validate() {
        const savedPin = localStorage.getItem('user_pin') || '1234';

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

<div class="fixed inset-0 z- flex items-center justify-center bg-black/60 p-6 backdrop-blur-md">
    
    <form class="sr-only" aria-hidden="true">
        <input 
            type="password" 
            name="password" 
            autocomplete="current-password" 
            value={pin}
            readonly 
        />
    </form>

    <div
        class="glass-panel relative flex w-full max-w-sm flex-col items-center overflow-hidden rounded-[40px] border border-white/10 p-10 shadow-2xl transition-colors duration-500
        bg-[#020617]/90 dark:bg-[#020617]/90 light:bg-white/95"
    >
        <div class="pointer-events-none absolute inset-0 bg-gradient-to-b from-white/[0.05] to-transparent"></div>

        <div class="mb-6 text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" />
            </svg>
        </div>

        <h2 class="mb-8 text-lg font-bold tracking-tight pin-text">Seguridad Kaira</h2>

        <div class="mb-12 flex gap-5 {error ? 'animate-shake' : ''}">
            {#each Array(4) as _, i}
                <div
                    class="h-3 w-3 rounded-full border-2 transition-all duration-300
                    {pin.length > i
                        ? 'scale-125 border-primary bg-primary shadow-[0_0_10px_var(--primary-glow)]'
                        : 'border-current opacity-20'}"
                ></div>
            {/each}
        </div>

        <div class="grid grid-cols-3 gap-6">
            {#each ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', 'DEL'] as key}
                <button
                    type="button"
                    onclick={() => (key === 'DEL' ? deleteLast() : key !== '' && addNumber(key))}
                    class="h-16 w-16 text-xl font-medium pin-text transition-all active:scale-95
                    {key === '' ? 'pointer-events-none opacity-0' : 'glass-btn-pin flex items-center justify-center rounded-full'}"
                >
                    {#if key === 'DEL'}
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
    /* Color de texto dinámico según el tema */
    .pin-text {
        color: var(--text-main);
    }

    .glass-btn-pin {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        -webkit-tap-highlight-color: transparent;
    }

    /* Adaptación al Modo Claro */
    :global([data-theme="light"]) .glass-btn-pin {
        background: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.08);
    }

    .glass-btn-pin:active {
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary);
    }

    .animate-shake {
        animation: shake 0.4s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
</style>