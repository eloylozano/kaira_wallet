<script lang="ts">
    interface Props {
        children?: import('svelte').Snippet;
        class?: string;
        onclick?: () => void;
    }

    let { children, class: className = '', onclick }: Props = $props();
</script>

<div 
    class="glass-card relative {className}"
    onclick={onclick}
    role={onclick ? "button" : "presentation"}
    tabindex={onclick ? 0 : -1}
>
    <div class="absolute inset-0 bg-gradient-to-b from-white/[0.08] to-transparent pointer-events-none rounded-[inherit] z-0"></div>
    
    <div class="relative z-10">
        {@render children?.()}
    </div>
</div>

<style>
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(var(--glass-blur, 12px));
        -webkit-backdrop-filter: blur(var(--glass-blur, 12px));
        border: 1px solid var(--glass-border);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
        
        /* 1. LIMITAR TRANSICIONES: Evita animar el blur/filtros */
        transition: background-color 0.25s ease, border-color 0.25s ease, transform 0.2s ease;

        /* 2. AISLAMIENTO: Evita artefactos visuales verticales */
        isolation: isolate;
        
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        transform: translateZ(0); 
    }

    /* Feedback de pulsación */
    div[role="button"]:active {
        transform: scale(0.97) translateZ(0);
    }
    
    @media (hover: hover) {
        div[role="button"]:hover {
            /* Cambiamos el color pero sin tocar el filtro de desenfoque */
            background-color: rgba(255, 255, 255, 0.07);
            border-color: rgba(255, 255, 255, 0.15);
        }
    }
</style>