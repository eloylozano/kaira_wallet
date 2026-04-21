<script lang="ts">
    import { fade, scale } from 'svelte/transition';
    
    let { isOpen, title, message, confirmText, onConfirm, onCancel } = $props();
</script>

{#if isOpen}
<div 
    transition:fade={{ duration: 200 }} 
    class="fixed inset-0 z- flex items-center justify-center bg-black/60 backdrop-blur-sm p-6"
>
    <button class="absolute inset-0 cursor-default" onclick={onCancel}></button>

    <div 
        transition:scale={{ start: 0.9, duration: 200 }} 
        class="relative w-full max-w-[320px] glass-panel overflow-hidden rounded-[32px] bg-[#1c1c1e]/90 border border-white/10 shadow-2xl"
    >
        <div class="p-8 text-center">
            <h3 class="text-white font-bold text-xl">{title}</h3>
            {#if message}
                <p class="text-white/60 text-sm mt-3 leading-relaxed">{message}</p>
            {/if}
        </div>
        
        <div class="flex flex-col border-t border-white/5">
            <button 
                onclick={onConfirm}
                class="w-full py-4 text-rose-500 font-bold text-base active:bg-white/10 transition-colors border-b border-white/5"
            >
                {confirmText}
            </button>
            
            <button 
                onclick={onCancel}
                class="w-full py-4 text-white/50 font-medium text-base active:bg-white/10 transition-colors"
            >
                Cancelar
            </button>
        </div>
    </div>
</div>
{/if}

<style>
    .glass-panel {
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
</style>