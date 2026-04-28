<script lang="ts">
    import { onMount } from 'svelte';
    import { transactionsStore } from '$lib/stores/transactions.svelte';

    let scrolled = $state(false);
    let stats = $state<any>(null);

    onMount(async () => {
        stats = await transactionsStore.getGlobalStats();

        const onScroll = () => {
            scrolled = window.scrollY > 20;
        };

        window.addEventListener('scroll', onScroll);
        return () => window.removeEventListener('scroll', onScroll);
    });

    let income = $derived(
        (transactionsStore.all ?? [])
            .filter((t) => t.type === 'income' && t.is_paid)
            .reduce((acc, t) => acc + Number(t.amount || 0), 0)
    );

    let expenses = $derived(
        (transactionsStore.all ?? [])
            .filter((t) => t.type === 'expense' && t.is_paid)
            .reduce((acc, t) => acc + Number(t.amount || 0), 0)
    );

    let investments = $derived(
        (transactionsStore.all ?? [])
            .filter((t) => t.type === 'invest' && t.is_paid)
            .reduce((acc, t) => acc + Number(t.amount || 0), 0)
    );

    let balance = $derived(
        (stats?.total_income ?? 0) - (stats?.total_expense ?? 0) - (stats?.total_invest ?? 0)
    );
</script>

<div 
    class="sticky top-0 z-40 w-full transition-all duration-500 {scrolled ? 'pt-2' : 'pt-4'}"
    style="padding-top: calc({scrolled ? '0.5rem' : '1rem'} + env(safe-area-inset-top, 0px));"
>
    <div class="mx-auto max-w-xl">
        <div
            class="glass-panel relative overflow-hidden border border-white/10 transition-all duration-500"
            class:rounded-[24px]={scrolled}
            class:rounded-[40px]={!scrolled}
            class:p-4={scrolled} 
            class:p-6={!scrolled}
            class:shadow-2xl={scrolled}
        >
            <div class="relative z-10 flex flex-col">
                <div class="flex items-center justify-between">
                    <div class="flex flex-col">
                        <p
                            class="text-[9px] sm:text-[10px] font-black tracking-[0.2em] text-primary/70 uppercase"
                            class:hidden={scrolled}
                        >
                            Balance disponible
                        </p>

                        <h2
                            class="font-black tracking-tight"
                            class:text-lg={scrolled}
                            class:sm:text-xl={scrolled}
                            class:mt-1={!scrolled}
                            class:sm:mt-3={!scrolled}
                            class:text-2xl={!scrolled} 
                            class:sm:text-4xl={!scrolled}
                        >
                            {balance.toFixed(2)}€
                        </h2>
                    </div>

                    <div class="flex items-center gap-2 sm:gap-3">
                        {#if scrolled}
                            <div class="flex gap-2 sm:gap-3 border-r border-white/10 pr-3 sm:pr-4 text-[9px] sm:text-[11px] font-bold">
                                <span class="text-primary">+{income.toFixed(0)}€</span>
                                <span class="text-rose-400">-{expenses.toFixed(0)}€</span>
                                <span class="text-sky-400">≈{investments.toFixed(0)}€</span>
                            </div>
                        {/if}
                        <span class="text-[9px] sm:text-[10px] font-bold text-primary/60">EUR</span>
                    </div>
                </div>

                <div
                    class="grid grid-cols-3 gap-2 sm:gap-4 transition-all duration-500"
                    class:max-h-0={scrolled}
                    class:opacity-0={scrolled}
                    class:mt-0={scrolled}
                    class:max-h-24={!scrolled}
                    class:mt-4={!scrolled}
                    class:sm:mt-6={!scrolled}
                >
                    <div>
                        <p class="text-[8px] sm:text-[10px] font-bold uppercase opacity-40">Ingresos</p>
                        <p class="text-sm sm:text-lg font-black text-primary">
                            +{income.toFixed(2)}€
                        </p>
                    </div>

                    <div class="text-right">
                        <p class="text-[8px] sm:text-[10px] font-bold uppercase opacity-40">Gastos</p>
                        <p class="text-sm sm:text-lg font-black text-rose-400">
                            -{expenses.toFixed(2)}€
                        </p>
                    </div>

                    <div class="text-right">
                        <p class="text-[8px] sm:text-[10px] font-bold uppercase opacity-40">Inversión</p>
                        <p class="text-sm sm:text-lg font-black text-sky-400">
                            ≈ {investments.toFixed(2)}€
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