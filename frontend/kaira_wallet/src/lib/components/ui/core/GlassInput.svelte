<script lang="ts">
    let { 
        value = $bindable(), 
        label = '', 
        placeholder = '', 
        type = 'text',
        ...rest 
    } = $props<{
        value: string | number;
        label?: string;
        placeholder?: string;
        type?: string;
        [key: string]: any;
    }>();
</script>

<div class="w-full">
    {#if label}
        <label class="mb-1.5 block text-[10px] font-bold uppercase tracking-widest opacity-60 ml-1">
            {label}
        </label>
    {/if}
    
    <input
        {type}
        bind:value={value}
        {placeholder}
        {...rest}
        class="
            w-full rounded-2xl
            bg-white/5 px-4 py-3
            text-sm font-semibold text-white
            transition-all duration-200
            placeholder:opacity-20
            
            /* Quitamos el azul del sistema */
            outline-none
            
            /* Borde base sutil */
            border border-white/5
            
            /* 🟢 EFECTO FOCUS: Borde blanco */
            focus:border-white/40
            focus:bg-white/10
            focus:ring-1 focus:ring-white/20
        "
    />
</div>