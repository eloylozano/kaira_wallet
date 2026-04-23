<script lang="ts">
    import { transactionsStore } from '$lib/stores/transactions.svelte';

    let { budget = 350 } = $props();

    let spent = $derived(
        (transactionsStore.all ?? [])
            .filter((t) => t.type === 'expense')
            .reduce((acc, t) => acc + Number(t.amount || 0), 0)
    );

    let remaining = $derived(budget - spent);
    let percentage = $derived(budget <= 0 ? 0 : Math.min((spent / budget) * 100, 100));
    let isOverBudget = $derived(remaining < 0);
</script>

<div class="mt-4">
    <div class="glass-panel relative overflow-hidden rounded-[32px] border border-white/10 p-5 transition-all">
        
        <div class="absolute -top-12 -right-12 h-24 w-24 rounded-full bg-rose-500/10 blur-[40px]"></div>

        <div class="relative z-10 flex flex-col gap-3">
            
            <div class="flex items-end justify-between">
                <div class="flex flex-col">
                    <p class="text-[9px] font-black tracking-[0.15em] text-rose-400/60 uppercase">
                        Presupuesto
                    </p>
                    <div class="flex items-baseline gap-2">
                        <h2 class="text-2xl font-black tracking-tighter">
                            {percentage.toFixed(0)}%
                        </h2>
                        <span class="text-[10px] font-bold opacity-30 uppercase">utilizado</span>
                    </div>
                </div>
                
                <div class="text-right">
                    <p class="text-[9px] font-bold uppercase opacity-30">Restante</p>
                    <p class="text-sm font-black {isOverBudget ? 'text-rose-500' : 'text-emerald-400'}">
                        {remaining.toFixed(2)}€
                    </p>
                </div>
            </div>

            <div class="relative h-1.5 w-full overflow-hidden rounded-full bg-white/5">
                <div
                    class="h-full bg-rose-500 transition-all duration-1000 ease-out"
                    style="width: {percentage}%"
                ></div>
            </div>

            <div class="flex justify-between text-[9px] font-bold uppercase tracking-tight opacity-40">
                <span>{spent.toFixed(0)}€ gastados</span>
                <span>Meta: {budget}€</span>
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