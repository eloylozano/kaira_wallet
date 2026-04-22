<script lang="ts">
    import { PUBLIC_API_URL } from '$env/static/public';
    import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
    import { categoriesStore } from '$lib/stores/categories.svelte';
    import { onMount } from 'svelte';

    type TransactionType = 'expense' | 'income' | 'invest';

    const typeOptions = [
        { value: 'expense', label: 'Gasto' },
        { value: 'income', label: 'Ingreso' },
        { value: 'invest', label: 'Inversión' }
    ];

    let amount = $state('');
    let description = $state('');
    let type = $state<TransactionType>('expense');

    let selectedParentId = $state<number | null>(null);
    let selectedCategoryId = $state<number | null>(null);

    const iconMap: Record<string, string> = {
        Transporte: '🚗', Coche: '🚘', Moto: '🏍️', Gasolina: '⛽',
        Alimentación: '🍎', Supermercado: '🛒', Restaurante: '🍔',
        Vivienda: '🏠', Alquiler: '🔑', Servicios: '⚡', Mantenimiento: '🛠️',
        Ocio: '🍿', Cine: '🎬', Suscripciones: '📺',
        Salario: '💰', Freelance: '💻', 'Otros Ingresos': '✨',
        Inversiones: '📈', Bolsa: '📊', Criptomonedas: '₿'
    };

    let currentCategories = $derived(categoriesStore.getByType(type));
    let selectedParent = $derived(currentCategories.find((c) => c.id === selectedParentId));

    // Corrección Svelte 5: Manejo de arrays en efecto
    $effect(() => {
        if (currentCategories && currentCategories.length > 0) {
            const firstParent = currentCategories; 
            selectedParentId = firstParent.id;

            if (firstParent.subcategories && firstParent.subcategories.length > 0) {
                selectedCategoryId = firstParent.subcategories.id;
            } else {
                selectedCategoryId = firstParent.id;
            }
        }
    });

    onMount(async () => {
        if (categoriesStore.all.length === 0) {
            // Aquí usamos el PIN hardcodeado o una variable PUBLIC_
            await categoriesStore.refresh('8061');
        }
    });

    const vibrate = (ms: number) => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) navigator.vibrate(ms);
    };

    function handleParentSelect(id: number) {
        selectedParentId = id;
        vibrate(10);
        const parent = currentCategories.find((c) => c.id === id);
        if (parent) {
            selectedCategoryId =
                parent.subcategories && parent.subcategories.length > 0
                    ? parent.subcategories.id
                    : parent.id;
        }
    }

    async function handleSubmit() {
        if (!amount || parseFloat(amount) <= 0 || !selectedCategoryId) {
            vibrate(100);
            return;
        }

        const newTransaction = {
            type,
            amount: parseFloat(amount),
            description: description || "Nueva transacción",
            category_id: selectedCategoryId,
            notes: "",
            frequency: "variable"
        };

        try {
            vibrate(30);
            
            // URL corregida con variable de entorno y protocolo http
            const response = await fetch(`${PUBLIC_API_URL}/transactions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json',
                    'X-Kaira-PIN': '8061' 
                },
                body: JSON.stringify(newTransaction)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('✅ Guardado:', result);
                amount = '';
                description = '';
            } else {
                const errorData = await response.json();
                console.error('❌ Error servidor:', errorData);
                throw new Error('Error en el servidor');
            }
        } catch (error) {
            console.error('Error al guardar:', error);
            alert('No se pudo conectar con el servidor.');
        }
    }
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 px-4 pb-32">
    <header class="py-6 pt-10">
        <h1 class="h1-kaira">Nuevo Movimiento</h1>
    </header>

    <SegmentedControl options={typeOptions} bind:selected={type} />

    <div
        class="glass-panel relative rounded-[32px] border border-white/10 p-8 transition-colors duration-500
        {type === 'expense' ? 'bg-red-500/5' : type === 'income' ? 'bg-emerald-500/5' : 'bg-blue-500/5'}"
    >
        <p class="text-center text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Importe</p>
        <div class="mt-2 flex items-center justify-center gap-1">
            <span
                class="text-4xl font-bold opacity-50"
                class:text-red-400={type === 'expense'}
                class:text-emerald-400={type === 'income'}
                class:text-blue-400={type === 'invest'}>€</span
            >
            <input
                type="number"
                inputmode="decimal"
                placeholder="0.00"
                bind:value={amount}
                class="w-full bg-transparent text-center text-6xl font-black outline-none placeholder:opacity-10
                {type === 'expense' ? 'text-red-500' : type === 'income' ? 'text-emerald-500' : 'text-blue-500'}"
            />
        </div>
    </div>

    <div class="space-y-3">
        <p class="px-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">Grupo</p>
        <div class="no-scrollbar flex gap-2 overflow-x-auto px-1 pb-2">
            {#each currentCategories as parent}
                <button
                    onclick={() => handleParentSelect(parent.id)}
                    class="flex-none rounded-2xl border px-5 py-3 text-[11px] font-bold transition-all
                    {selectedParentId === parent.id
                        ? 'border-white bg-white text-black'
                        : 'border-white/10 bg-white/5 text-white/50'}"
                >
                    {parent.name}
                </button>
            {/each}
        </div>
    </div>

    <div class="space-y-4">
        <p class="px-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
            Detalle de {selectedParent?.name || '...'}
        </p>

        <div class="grid grid-cols-3 gap-3">
            {#if selectedParent && selectedParent.subcategories?.length > 0}
                {#each selectedParent.subcategories as sub}
                    <button
                        onclick={() => {
                            selectedCategoryId = sub.id;
                            vibrate(10);
                        }}
                        class="flex flex-col items-center gap-2 rounded-[24px] border p-4 transition-all active:scale-95
                        {selectedCategoryId === sub.id
                            ? 'border-primary bg-primary/20 text-primary shadow-[0_0_20px_rgba(var(--primary-rgb),0.3)]'
                            : 'border-white/5 bg-white/5 opacity-60'}"
                    >
                        <span class="text-2xl">{iconMap[sub.name] || '✨'}</span>
                        <span class="text-center text-[9px] font-black tracking-tighter uppercase">{sub.name}</span>
                    </button>
                {/each}
            {:else if selectedParent}
                <button
                    onclick={() => {
                        selectedCategoryId = selectedParentId;
                        vibrate(10);
                    }}
                    class="col-span-3 flex items-center justify-center gap-3 rounded-[24px] border border-primary bg-primary/10 p-6 text-primary"
                >
                    <span class="text-2xl">{iconMap[selectedParent.name] || '✨'}</span>
                    <span class="text-xs font-black tracking-widest uppercase">Usar {selectedParent.name}</span>
                </button>
            {/if}
        </div>
    </div>

    <div class="space-y-6">
        <input
            type="text"
            placeholder="Nota opcional..."
            bind:value={description}
            class="w-full rounded-2xl border border-white/5 bg-white/5 p-5 text-sm transition-colors outline-none focus:border-primary/40"
        />

        <button
            onclick={handleSubmit}
            class="w-full rounded-[24px] bg-primary py-5 text-sm font-black tracking-[0.3em] text-white uppercase shadow-2xl transition-all active:scale-[0.97]"
        >
            Confirmar {typeOptions.find((o) => o.value === type)?.label}
        </button>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
</style>