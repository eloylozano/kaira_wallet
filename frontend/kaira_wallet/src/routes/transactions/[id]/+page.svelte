<script lang="ts">
    import { onMount } from 'svelte';
    import {
        getTransaction,
        getTransactionHistory,
        deleteTransaction,
        type TransactionHistoryEntry
    } from '$lib/api/transactions';
    import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
    import { goto } from '$app/navigation';
    import TransactionForm from '$lib/components/transactions/form/TransactionForm.svelte';
    import { History, RefreshCw } from 'lucide-svelte';

    let { data } = $props();
    let tx = $state<any>(null);
    let loading = $state(true);
    let isDeleteModalOpen = $state(false);
    let historyOpen = $state(false);
    let historyLoading = $state(false);
    let history = $state<TransactionHistoryEntry[]>([]);
    let historyError = $state(false);

    const euros = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' });
    const dateTime = new Intl.DateTimeFormat('es-ES', { dateStyle: 'medium', timeStyle: 'short' });
    const fieldLabels: Record<string, string> = {
        amount: 'Importe',
        description: 'Descripción',
        category_id: 'Categoría',
        date: 'Fecha',
        type: 'Tipo',
        frequency: 'Frecuencia',
        is_paid: 'Estado'
    };

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
        window.history.back();
    }

    async function toggleHistory() {
        historyOpen = !historyOpen;
        if (!historyOpen || historyLoading || history.length) return;
        historyLoading = true;
        historyError = false;
        try {
            history = await getTransactionHistory(data.id);
        } catch {
            historyError = true;
        } finally {
            historyLoading = false;
        }
    }

    function displayValue(field: string, value: unknown, label?: string | null) {
        if (field === 'category_id' && label) return label;
        if (field === 'amount' && typeof value === 'number') return euros.format(value);
        if (field === 'is_paid') return value ? 'Pagado' : 'Pendiente';
        if (field === 'date' && typeof value === 'string')
            return new Date(value).toLocaleDateString('es-ES');
        if (field === 'type')
            return (
                ({ expense: 'Gasto', income: 'Ingreso', invest: 'Inversión' } as Record<string, string>)[
                    String(value)
                ] ?? String(value)
            );
        if (field === 'frequency') return value === 'fixed' ? 'Fijo' : 'Variable';
        if (field === 'category_id') return `Categoría #${value}`;
        return value === null || value === '' ? 'Sin valor' : String(value);
    }
</script>

<div class="mx-auto max-w-xl pb-32">
    <header class="mb-8">
        <div class="mb-4 flex items-center justify-between">
            <button
                onclick={goBack}
                class="flex items-center gap-2 text-[10px] font-black tracking-widest uppercase opacity-50 transition-opacity hover:opacity-100"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"><path d="m15 18-6-6 6-6" /></svg
                >
                Volver
            </button>
            <div class="flex items-center gap-2">
                <button
                    onclick={toggleHistory}
                    class="flex items-center gap-1 rounded-full px-3 py-1.5 text-[10px] font-black tracking-widest uppercase transition-all active:scale-95 {historyOpen ? 'bg-primary text-white' : 'bg-primary/10 text-primary hover:bg-primary/20'}"
                    aria-expanded={historyOpen}
                    aria-label="Ver historial de cambios"
                >
                    <History size={14} /><span>Registro</span>
                </button>
                <button
                    onclick={() => (isDeleteModalOpen = true)}
                    class="flex items-center gap-1 rounded-full bg-rose-500/10 px-3 py-1.5 text-[10px] font-black tracking-widest text-rose-500 uppercase transition-all hover:bg-rose-500/20 active:scale-95"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="12"
                        height="12"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        ><path d="M3 6h18" /><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" /><path
                            d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"
                        /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /></svg
                    >
                    Borrar
                </button>
            </div>
        </div>
        <h1 class="h1-kaira text-4xl font-black uppercase italic">Editar movimiento</h1>
        <p class="text-[10px] font-bold tracking-widest uppercase opacity-30">
            Ajusta los detalles de este registro
        </p>

        {#if historyOpen}
            <aside class="mt-5 rounded-2xl border border-primary/15 bg-primary/[0.04] p-4">
                <div class="mb-3 flex items-center justify-between text-[10px] font-black tracking-widest text-primary uppercase">
                    <p>Historial de cambios</p>
                    <History size={15} />
                </div>
                {#if historyLoading}
                    <div class="flex items-center gap-2 text-xs opacity-60">
                        <RefreshCw class="animate-spin" size={14} /> Cargando…
                    </div>
                {:else if historyError}
                    <p class="text-xs text-rose-400">No se ha podido cargar el historial.</p>
                {:else if !history.length}
                    <p class="text-xs opacity-60">Todavía no hay cambios registrados.</p>
                {:else}
                    <div class="space-y-3">
                        {#each history as entry (entry.id)}
                            <div class="rounded-xl bg-black/[0.04] p-3 text-xs leading-5">
                                <time class="mb-1 block text-[10px] font-bold opacity-50">{dateTime.format(new Date(entry.created_at))}</time>
                                {#each Object.entries(entry.changes) as [field, change]}
                                    <p class="break-words">
                                        <strong>{fieldLabels[field] ?? field}:</strong>
                                        <span class="opacity-60">{displayValue(field, change.from, change.from_label)}</span>
                                        <b class="mx-1 opacity-40">→</b>
                                        <span class="font-medium">{displayValue(field, change.to, change.to_label)}</span>
                                    </p>
                                {/each}
                            </div>
                        {/each}
                    </div>
                {/if}
            </aside>
        {/if}
    </header>

    {#if loading}
        <div class="flex justify-center py-20">
            <div
                class="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent"
            ></div>
        </div>
    {:else if tx}
        {#key tx.id}<TransactionForm mode="edit" id={data.id} initial={tx} />{/key}
    {:else}
        <div class="py-20 text-center">
            <p class="font-bold text-rose-400">No se encontró el movimiento</p>
            <button onclick={goBack} class="mt-4 text-sm underline opacity-50">Regresar</button>
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
