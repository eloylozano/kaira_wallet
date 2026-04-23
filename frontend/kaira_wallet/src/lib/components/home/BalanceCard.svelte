<script lang="ts">
    import { onMount } from 'svelte';
    import { transactionsStore } from '$lib/stores/transactions.svelte';

    let scrolled = $state(false);
    
    // Simplificamos los derived (quitando el exceso de funciones anidadas)
    let income = $derived(
        (transactionsStore.all ?? [])
            .filter((t) => t.type === 'income')
            .reduce((acc, t) => acc + Number(t.amount || 0), 0)
    );

    let expenses = $derived(
        (transactionsStore.all ?? [])
            .filter((t) => t.type === 'expense')
            .reduce((acc, t) => acc + Number(t.amount || 0), 0)
    );

    let balance = $derived(income + expenses);

    onMount(() => {
        const onScroll = () => {
            scrolled = window.scrollY > 20;
        };
        window.addEventListener('scroll', onScroll);
        return () => window.removeEventListener('scroll', onScroll);
    });
</script>

<div class="sticky top-0 z-40 w-full transition-all duration-500 {scrolled ? 'pt-2' : 'pt-4'}">
    <div class="mx-auto max-w-xl">
        <div
            class="glass-panel relative overflow-hidden border border-white/10 transition-all px-6 duration-500 ease-[cubic-bezier(0.23,1,0.32,1)]"
            class:rounded-[24px]={scrolled}
            class:rounded-[40px]={!scrolled}
            class:p-3={scrolled}
            class:p-6={!scrolled}
            class:shadow-2xl={scrolled}
        >
            <div
                class="absolute -top-24 -right-24 h-48 w-48 rounded-full bg-primary/10 blur-[80px] transition-opacity duration-500"
                class:opacity-0={scrolled}
            ></div>

            <div class="relative z-10 flex flex-col transition-all duration-500">
                
                <div class="flex items-center justify-between" class:flex-row={scrolled}>
                    
                    <div class="flex flex-col transition-all">
                        <p class="text-[10px] font-black tracking-[0.2em] text-primary/70 uppercase transition-all"
                           class:hidden={scrolled}>
                            Balance disponible
                        </p>
                        
                        <h2 class="font-black tracking-tight transition-all duration-500"
                            class:text-xl={scrolled}
                            class:mt-3={!scrolled}
                            class:text-4xl={!scrolled}>
                            {balance.toFixed(2)}€
                        </h2>
                    </div>

                    <div class="flex items-center gap-3">
                        {#if scrolled}
                            <div class="flex gap-3 pr-4 border-r border-white/10 text-[11px] font-bold">
                                <span class="text-primary">+{income.toFixed(0)}€</span>
                                <span class="text-rose-400">{expenses.toFixed(0)}€</span>
                            </div>
                        {/if}
                        <span class="text-[10px] font-bold text-primary/60">EUR</span>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 overflow-hidden transition-all duration-500"
                     class:max-h-0={scrolled}
                     class:opacity-0={scrolled}
                     class:mt-0={scrolled}
                     class:max-h-20={!scrolled}
                     class:mt-6={!scrolled}>
                    <div>
                        <p class="text-[10px] font-bold uppercase opacity-40">Ingresos</p>
                        <p class="text-lg font-black text-primary">
                            +{income.toFixed(2)}€
                        </p>
                    </div>

                    <div class="text-right">
                        <p class="text-[10px] font-bold uppercase opacity-40">Gastos</p>
                        <p class="text-lg font-black text-rose-400">
                            {expenses.toFixed(2)}€
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
</style>