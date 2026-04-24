<script lang="ts">
    interface Props {
        children?: import('svelte').Snippet;
        class?: string;
        onclick?: () => void;
    }

    let { children, class: className = '', onclick }: Props = $props();
</script>

<div 
    class="glass-card relative overflow-hidden transition-all duration-300 {className}"
    onclick={onclick}
    role={onclick ? "button" : "presentation"}
    tabindex={onclick ? 0 : -1}
>
    <div class="absolute inset-0 bg-gradient-to-b from-white/[0.05] to-transparent pointer-events-none"></div>
    
    {@render children?.()}
</div>

<style>
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(var(--glass-blur));
        -webkit-backdrop-filter: blur(var(--glass-blur));
        border: 1px solid var(--glass-border);
        /* Sombra más profunda y difusa para dar elevación real */
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }

    /* Feedback visual mejorado para Emerald */
    div[role="button"]:active {
        transform: scale(0.97);
        border-color: var(--primary);
        box-shadow: 0 0 20px var(--primary-glow);
    }
    
    /* Hover suave en PC */
    @media (hover: hover) {
        div[role="button"]:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.15);
        }
    }
</style>