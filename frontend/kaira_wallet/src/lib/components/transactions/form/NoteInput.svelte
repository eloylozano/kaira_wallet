<script lang="ts">
    let {
        value = $bindable(''),
        label = 'Nota',
        placeholder = 'Añadir detalles...'
    } = $props();
</script>

<div class="space-y-3">
    <p class="kaira-soft px-2 text-[10px] font-black uppercase tracking-[0.2em]">
        {label}
    </p>

    <textarea
        bind:value
        rows="4"
        placeholder={placeholder}
        class="
            kaira-input
            w-full resize-none rounded-[28px] p-5 text-sm leading-relaxed
            transition-all duration-200
            outline-none
            /* Sobrescribimos Tailwind para asegurar que use tus variables CSS */
            appearance-none
        "
    ></textarea>
</div>

<style>
    /* Aseguramos que el estilo que pasaste se aplique 
       incluso si hay conflictos con Tailwind 
    */
    .kaira-input {
        background: var(--input-bg);
        border: 1px solid var(--input-border);
        color: var(--text-main);
    }

    .kaira-input::placeholder {
        color: var(--text-soft);
        opacity: 0.5;
    }

    .kaira-input:focus {
        outline: none;
        border-color: var(--primary) !important; /* El borde blanco/rosa que querías */
        background: rgba(255, 255, 255, 0.05); /* Un toque extra de brillo al escribir */
    }
</style>