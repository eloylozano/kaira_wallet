<script lang="ts">
    import { onMount } from 'svelte';
    import GlassCard from '$lib/components/ui/GlassCard.svelte';
    import { categoryStore } from '$lib/stores/categories';

    onMount(() => {
        categoryStore.fetchCategories(1);
    });

    // Datos ficticios para rellenar el diseño
    const recentTransactions = [
        { name: 'Apple Music', category: 'Entretenimiento', amount: -10.99, icon: '🎵' },
        { name: 'Sueldo Nómina', category: 'Ingresos', amount: 2500.00, icon: '💰' },
        { name: 'Starbucks', category: 'Comida', amount: -5.50, icon: '☕' }
    ];
</script>

<div class="flex flex-col gap-8 pb-24 max-w-xl mx-auto px-4">
    <header class="pt-8 flex justify-between items-end">
        <div>
            <p class="text-xs font-black uppercase tracking-[0.2em] text-primary/80">Karia Wallet</p>
            <h1 class="text-3xl font-black italic tracking-tighter uppercase">Hola, Eloy</h1>
        </div>
        <div class="w-10 h-10 rounded-2xl glass-panel border border-primary/20 flex items-center justify-center text-xl">
            👤
        </div>
    </header>

    <GlassCard class="!rounded-[40px] p-8 relative overflow-hidden group">
        <div class="absolute -top-24 -right-24 w-48 h-48 bg-primary/10 rounded-full blur-[80px]"></div>
        
        <div class="relative z-10">
            <div class="flex justify-between items-start">
                <span class="text-[10px] uppercase font-black tracking-widest opacity-50">Balance Disponible</span>
                <div class="px-2 py-1 rounded-lg bg-primary/10 border border-primary/20 text-[10px] font-bold text-primary italic">EUR</div>
            </div>
            
            <h2 class="text-5xl font-black mt-4 tracking-tighter drop-shadow-2xl">
                2.450,00<span class="text-2xl opacity-50 font-medium">€</span>
            </h2>

            <div class="grid grid-cols-2 gap-4 mt-10">
                <div class="flex flex-col gap-1">
                    <div class="flex items-center gap-2">
                        <div class="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_var(--primary)]"></div>
                        <p class="text-[10px] uppercase font-bold opacity-40">Ingresos</p>
                    </div>
                    <p class="text-xl font-bold tracking-tight text-primary">+3.000€</p>
                </div>
                
                <div class="flex flex-col gap-1 text-right">
                    <div class="flex items-center gap-2 justify-end">
                        <p class="text-[10px] uppercase font-bold opacity-40">Gastos</p>
                        <div class="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_8px_#f43f5e]"></div>
                    </div>
                    <p class="text-xl font-bold tracking-tight text-rose-400">-550€</p>
                </div>
            </div>
        </div>
    </GlassCard>

    <section>
        <div class="flex justify-between items-end mb-4 px-2">
            <h3 class="text-xs font-black uppercase tracking-widest opacity-60">Categorías</h3>
            <button class="text-[10px] font-black uppercase tracking-tighter text-primary border-b border-primary/30">Ver todas</button>
        </div>
        
        <div class="flex gap-4 overflow-x-auto pb-4 no-scrollbar">
            {#each $categoryStore.slice(0, 4) as category}
                <GlassCard class="p-4 min-w-[140px] !rounded-3xl flex flex-col gap-3 active-tap">
                    <div class="w-10 h-10 rounded-2xl bg-white/5 flex items-center justify-center text-lg">
                        📂
                    </div>
                    <div>
                        <p class="text-xs font-black opacity-80 leading-none mb-1">{category.name}</p>
                        <span class="text-[9px] uppercase font-bold text-primary/60">{category.transaction_type}</span>
                    </div>
                </GlassCard>
            {/each}
        </div>
    </section>

    <section>
        <h3 class="text-xs font-black uppercase tracking-widest opacity-60 mb-4 px-2">Movimientos Recientes</h3>
        <div class="space-y-3">
            {#each recentTransactions as tx}
                <div class="flex items-center justify-between p-4 glass-panel !rounded-[24px] border border-white/5 transition-all hover:bg-white/5">
                    <div class="flex items-center gap-4">
                        <div class="w-11 h-11 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-xl shadow-inner">
                            {tx.icon}
                        </div>
                        <div>
                            <p class="text-sm font-bold opacity-90">{tx.name}</p>
                            <p class="text-[10px] font-bold opacity-40 uppercase tracking-tighter">{tx.category}</p>
                        </div>
                    </div>
                    <p class="font-black text-sm {tx.amount > 0 ? 'text-primary' : 'text-white'}">
                        {tx.amount > 0 ? '+' : ''}{tx.amount.toFixed(2)}€
                    </p>
                </div>
            {/each}
        </div>
    </section>
</div>

<style>
    /* Ocultar barra de scroll para el carrusel de categorías */
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
    .no-scrollbar {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>