<script lang="ts">
    interface Props {
        children?: import('svelte').Snippet;
        class?: string;
        onclick?: () => void;
    }

    let { children, class: className = '', onclick }: Props = $props();
</script>

<div 
    class="glass-card relative transition-all duration-200 {className}"
    onclick={onclick}
    role={onclick ? "button" : "presentation"}
    tabindex={onclick ? 0 : -1}
>
    <div class="absolute inset-0 bg-gradient-to-b from-white/[0.05] to-transparent pointer-events-none rounded-[inherit]"></div>
    
    <div class="relative z-10">
        {@render children?.()}
    </div>
</div>

<style>
    .glass-card {
        background: var(--glass-bg);
        /* Usamos variables con fallbacks seguros */
        backdrop-filter: blur(var(--glass-blur, 12px));
        -webkit-backdrop-filter: blur(var(--glass-blur, 12px));
        border: 1px solid var(--glass-border);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
        
        /* CRÍTICO: Previene el parpadeo en Safari/iOS al transformar */
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        transform: translateZ(0); 
    }

    /* Ajuste de feedback visual: menos agresivo para evitar "shaking" */
    div[role="button"]:active {
        transform: scale(0.98) translateZ(0);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    @media (hover: hover) {
        div[role="button"]:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }
    }
</style>