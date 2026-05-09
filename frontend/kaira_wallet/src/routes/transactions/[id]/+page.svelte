<script lang="ts">
    import { onMount } from 'svelte';
    import { getTransaction, deleteTransaction } from '$lib/api/transactions';
    import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
    import { goto } from '$app/navigation';
	import TransactionForm from '$lib/components/transactions/form/TransactionForm.svelte';

    let { data } = $props();

    let tx = $state<any>(null);
    let loading = $state(true);
    let isDeleteModalOpen = $state(false);

    onMount(async () => {
        try {
            tx = await getTransaction(data.id);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    async function handleDelete() {
        try {
            await deleteTransaction(data.id);
            goto('/'); 
        } catch (e) {
            alert('Error al eliminar');
        } finally {
            isDeleteModalOpen = false;
        }
    }

    function goBack() {
        history.back();
    }
</script>

<div class="mx-auto max-w-xl pb-32">
    <header class="mb-8">
        <div class="mb-4 flex items-center justify-between">
            <button 
                onclick={goBack}
                class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest opacity-50 hover:opacity-100 transition-opacity"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                Volver
            </button>

            <button 
                onclick={() => (isDeleteModalOpen = true)}
                class="flex items-center gap-1.5 rounded-full bg-rose-500/10 px-3 py-1.5 text-[10px] font-black uppercase tracking-widest text-rose-500 transition-all active:scale-95 hover:bg-rose-500/20"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                Borrar
            </button>
        </div>

        <h1 class="h1-kaira text-4xl font-black italic uppercase">Editar movimiento</h1>
        <p class="text-[10px] font-bold tracking-widest uppercase opacity-30">
            Ajusta los detalles de este registro
        </p>
    </header>

    {#if loading}
        <div class="flex justify-center py-20">
            <div class="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
        </div>
    {:else if tx}
        {#key tx.id}
            <TransactionForm mode="edit" id={data.id} initial={tx} />
        {/key}
    {:else}
        <div class="text-center py-20">
            <p class="text-rose-400 font-bold">No se encontró el movimiento</p>
            <button onclick={goBack} class="mt-4 text-sm opacity-50 underline">Regresar</button>
        </div>
    {/if}
</div>

<ConfirmModal 
    isOpen={isDeleteModalOpen}
    title="¿Eliminar registro?"
    message="Esta acción no se puede deshacer."
    confirmText="Eliminar"
    onConfirm={handleDelete}
    onCancel={() => (isDeleteModalOpen = false)}
/>