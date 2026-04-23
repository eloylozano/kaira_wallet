<script lang="ts">
    import { goto } from '$app/navigation';
    import TransactionItem from '$lib/components/ui/TransactionItem.svelte';
    import { transactionsStore } from '$lib/stores/transactions.svelte';

    let lastFive = $derived(
        (transactionsStore.all ?? [])
            .slice()
            .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
            .slice(0, 5)
    );
</script>

<div class="mt-8">
    <div class="mb-3 flex items-center justify-between">
        <h2 class="text-[10px] font-black tracking-widest uppercase opacity-60">
            Últimos movimientos
        </h2>
        <button
            onclick={() => goto('/transactions')}
            class="kaira-chip rounded-xl px-4 py-2 text-[10px] font-bold uppercase transition-all hover:opacity-80 active:scale-95"
        >
            Ver todo
        </button>
    </div>

    <div class="space-y-3">
        {#each lastFive as tx (tx.id)}
            <button
                onclick={() => goto(`/transactions/${tx.id}`)}
                class="w-full text-left transition-transform active:scale-[0.98]"
            >
                <TransactionItem {tx} />
            </button>
        {/each}
    </div>
</div>