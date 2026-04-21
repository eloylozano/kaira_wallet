<script lang="ts">
    interface Props {
        onclick: () => void;
        text: string;
        variant?: 'normal' | 'danger';
    }

    let { onclick, text, variant = 'normal' }: Props = $props();
</script>

<button 
    {onclick}
    class="relative overflow-hidden text-[10px] font-black uppercase tracking-widest px-5 py-2.5 rounded-full 
    border transition-all active:scale-95
    {variant === 'danger' 
        ? 'bg-rose-500/10 border-rose-500/30 text-rose-500 hover:bg-rose-500/20' 
        : 'btn-glass-normal'
    }"
>
    <span class="absolute inset-0 bg-gradient-to-b from-white/10 to-transparent pointer-events-none opacity-50"></span>
    <span class="relative z-10">{text}</span>
</button>

<style>
    button {
        -webkit-tap-highlight-color: transparent;
        will-change: transform;
        /* Usamos el color de texto principal definido en el CSS global */
        color: inherit; 
    }

    .btn-glass-normal {
        /* En modo oscuro (default) */
        background-color: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        color: var(--text-main);
        opacity: 0.8;
    }

    .btn-glass-normal:hover {
        opacity: 1;
        background-color: rgba(255, 255, 255, 0.1);
    }

    /* Ajuste específico para el tema claro usando el atributo de datos */
    :global([data-theme="light"]) .btn-glass-normal {
        background-color: rgba(0, 0, 0, 0.05);
        border-color: rgba(0, 0, 0, 0.1);
        color: var(--text-main); /* Aquí usará el color oscuro del tema claro */
    }

    :global([data-theme="light"]) .btn-glass-normal:hover {
        background-color: rgba(0, 0, 0, 0.08);
    }
</style>