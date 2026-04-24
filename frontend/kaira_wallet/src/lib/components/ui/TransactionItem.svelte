<script lang="ts">
    import * as Icons from 'lucide-svelte';

    let { tx } = $props();

    function toPascalCase(str: string) {
        if (!str) return '';
        return str
            .split('-')
            .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
            .join('');
    }

    let IconComponent = $derived(() => {
        if (!tx.category?.icon) return null;
        const key = toPascalCase(tx.category.icon);
        return Icons[key] || null;
    });

    const Icon = $derived(IconComponent());

    // Configuración de colores centralizada
    let theme = $derived(() => {
        switch (tx.type) {
            case 'income':
                return {
                    icon: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
                    amount: 'text-primary',
                    prefix: '+'
                };
            case 'expense':
                return {
                    icon: 'text-red-400 bg-red-400/10 border-red-400/20',
                    amount: 'text-red-400',
                    prefix: '-'
                };
            case 'invest':
                return {
                    icon: 'text-sky-400 bg-sky-400/10 border-sky-400/20',
                    amount: 'text-sky-400',
                    prefix: '≈'
                };
            default:
                return {
                    icon: 'text-white/40 bg-white/5 border-white/10',
                    amount: 'text-white',
                    prefix: ''
                };
        }
    });

    // Formateador de fecha amigable (ej: "24 ene" o "Hoy")
    let formattedDate = $derived(() => {
        if (!tx.date) return '';
        const dateObj = new Date(tx.date);
        const today = new Date();
        
        if (dateObj.toDateString() === today.toDateString()) return 'Hoy';
        
        return dateObj.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: 'short'
        }).replace('.', ''); // Quita el punto del mes abreviado
    });
</script>

<div class="kaira-panel flex items-center gap-4 rounded-3xl p-4 bg-white/5 border border-white/5">
    <div class="flex h-12 w-12 items-center justify-center rounded-2xl border {theme().icon}">
        {#if Icon}
            <Icon class="h-6 w-6"/>
        {:else}
            <Icons.CircleDollarSign class="h-6 w-6 opacity-30"/>
        {/if}
    </div>

    <div class="flex-1 min-w-0">
        <p class="truncate text-sm font-bold text-white">
            {tx.description}
        </p>

        <div class="flex items-center gap-2">
            <p class="text-[10px] font-bold uppercase tracking-wider opacity-40">
                {tx.category?.name}
            </p>
            <span class="h-1 w-1 rounded-full bg-white/10"></span>
            <p class="text-[10px] font-bold text-white/30 uppercase">
                {formattedDate()}
            </p>
        </div>
    </div>

    <div class="text-right">
        <p class="text-lg font-black {theme().amount}">
            {theme().prefix}{tx.amount} €
        </p>
        {#if tx.is_paid === false}
            <p class="text-[9px] font-black uppercase tracking-tighter text-orange-400/70">Pendiente</p>
        {/if}
    </div>
</div>