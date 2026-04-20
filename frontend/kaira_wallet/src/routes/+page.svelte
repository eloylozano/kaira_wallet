<script lang="ts">
    import { onMount } from 'svelte';
    import GlassCard from '$lib/components/ui/GlassCard.svelte';
    import { categoryStore } from '$lib/stores/categories';

    onMount(() => {
        categoryStore.fetchCategories(1);
    });
</script>

<div class="flex flex-col gap-8">
    <header class="pt-4">
        <h1 class="text-3xl font-extrabold tracking-tight text-white">Karia Wallet</h1>
        <p class="text-slate-400 text-sm font-medium">Hola, Eloy 👋</p>
    </header>

    <GlassCard class="p-8 text-center bg-gradient-to-b from-white/10 to-transparent">
        <span class="text-xs uppercase tracking-widest text-slate-400 font-bold">Balance Total</span>
        <h2 class="text-5xl font-black mt-3 tracking-tighter text-white">2.450,00€</h2>
        
        <div class="flex justify-between items-center mt-8 pt-6 border-t border-white/5">
            <div class="flex-1 text-left">
                <p class="text-[10px] uppercase font-bold text-slate-500 mb-1">Ingresos</p>
                <p class="text-emerald-400 font-bold text-lg">+3.000€</p>
            </div>
            
            <div class="h-8 w-[1px] bg-white/10"></div>
            
            <div class="flex-1 text-right">
                <p class="text-[10px] uppercase font-bold text-slate-500 mb-1">Gastos</p>
                <p class="text-rose-400 font-bold text-lg">-550€</p>
            </div>
        </div>
    </GlassCard>

    <section>
        <div class="flex justify-between items-center mb-5">
            <h3 class="text-lg font-bold text-white/90">Tus Categorías</h3>
            <button class="text-xs text-primary font-semibold">Ver todas</button>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
            {#each $categoryStore as category}
                <GlassCard class="p-4 active-tap flex flex-col gap-2 border-l-4 border-l-primary/40">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-tighter">
                        {category.transaction_type}
                    </span>
                    <p class="text-sm font-bold text-white leading-tight">{category.name}</p>
                </GlassCard>
            {/each}
        </div>
    </section>
</div>