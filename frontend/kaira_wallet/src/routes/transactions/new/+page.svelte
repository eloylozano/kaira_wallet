<script lang="ts">
	import SegmentedControl from '$lib/components/ui/SegmentedControl.svelte';
    import { categoriesStore } from '$lib/stores/categories.svelte';
    import { onMount } from 'svelte';

    type TransactionType = 'expense' | 'income' | 'invest';
    
    // Opciones para el nuevo componente SegmentedControl
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
        'Transporte': '🚗', 'Coche': '🚘', 'Moto': '🏍️', 'Gasolina': '⛽',
        'Alimentación': '🍎', 'Supermercado': '🛒', 'Restaurante': '🍔',
        'Vivienda': '🏠', 'Alquiler': '🔑', 'Servicios': '⚡', 'Mantenimiento': '🛠️',
        'Ocio': '🍿', 'Cine': '🎬', 'Suscripciones': '📺',
        'Salario': '💰', 'Freelance': '💻', 'Otros Ingresos': '✨',
        'Inversiones': '📈', 'Bolsa': '📊', 'Criptomonedas': '₿'
    };

    let currentCategories = $derived(categoriesStore.getByType(type));
    let selectedParent = $derived(currentCategories.find(c => c.id === selectedParentId));

    // Corrección del efecto: Manejo de IDs correcto
    $effect(() => {
        if (currentCategories.length > 0) {
            const firstParent = currentCategories;
            selectedParentId = firstParent.id;
            
            // Si tiene hijos, seleccionamos el primer hijo. Si no, al padre.
            selectedCategoryId = (firstParent.subcategories && firstParent.subcategories.length > 0)
                ? firstParent.subcategories.id 
                : firstParent.id;
        }
    });

    onMount(async () => {
        if (categoriesStore.all.length === 0) {
            await categoriesStore.refresh('8061');
        }
    });

    const vibrate = (ms: number) => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) navigator.vibrate(ms);
    };

    function handleParentSelect(id: number) {
        selectedParentId = id;
        vibrate(10);
        const parent = currentCategories.find(c => c.id === id);
        if (parent) {
            selectedCategoryId = (parent.subcategories && parent.subcategories.length > 0)
                ? parent.subcategories.id 
                : parent.id;
        }
    }

    function handleSubmit() {
        if (!amount || parseFloat(amount) <= 0 || !selectedCategoryId) return;
        
        const newTransaction = {
            id: crypto.randomUUID(),
            type,
            amount: parseFloat(amount),
            description,
            category_id: selectedCategoryId,
            date: new Date().toISOString()
        };

        vibrate(30);
        console.log('Guardando en Kaira...', newTransaction);
        
        amount = '';
        description = '';
    }
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-6 px-4 pb-32">
    <header class="py-6 pt-10">
        <h1 class="h1-kaira">Nuevo Movimiento</h1>
    </header>

    <SegmentedControl options={typeOptions} bind:selected={type} />

    <div class="glass-panel relative rounded-[32px] border border-white/10 p-8 transition-colors duration-500
        {type === 'expense' ? 'bg-red-500/5' : type === 'income' ? 'bg-emerald-500/5' : 'bg-blue-500/5'}">
        <p class="text-center text-[10px] font-black uppercase tracking-[0.2em] opacity-40">Importe</p>
        <div class="mt-2 flex items-center justify-center gap-1">
            <span class="text-4xl font-bold opacity-50" 
                class:text-red-400={type === 'expense'} 
                class:text-emerald-400={type === 'income'}
                class:text-blue-400={type === 'invest'}>€</span>
            <input 
                type="number" inputmode="decimal" placeholder="0.00"
                bind:value={amount}
                class="w-full bg-transparent text-center text-6xl font-black outline-none placeholder:opacity-10
                {type === 'expense' ? 'text-red-500' : type === 'income' ? 'text-emerald-500' : 'text-blue-500'}"
            />
        </div>
    </div>

    <div class="space-y-3">
        <p class="px-2 text-[10px] font-black uppercase tracking-[0.2em] opacity-40">Grupo</p>
        <div class="flex gap-2 overflow-x-auto pb-2 no-scrollbar px-1">
            {#each currentCategories as parent}
                <button 
                    onclick={() => handleParentSelect(parent.id)}
                    class="flex-none rounded-2xl px-5 py-3 border text-[11px] font-bold transition-all
                    {selectedParentId === parent.id ? 'bg-white text-black border-white' : 'bg-white/5 border-white/10 text-white/50'}"
                >
                    {parent.name}
                </button>
            {/each}
        </div>
    </div>

    <div class="space-y-4">
        <p class="px-2 text-[10px] font-black uppercase tracking-[0.2em] opacity-40">
            Detalle de {selectedParent?.name || '...'}
        </p>
        
        <div class="grid grid-cols-3 gap-3">
            {#if selectedParent && selectedParent.subcategories?.length > 0}
                {#each selectedParent.subcategories as sub}
                    <button 
                        onclick={() => { selectedCategoryId = sub.id; vibrate(10); }}
                        class="flex flex-col items-center gap-2 rounded-[24px] border p-4 transition-all active:scale-95
                        {selectedCategoryId === sub.id 
                            ? 'border-primary bg-primary/20 text-primary shadow-[0_0_20px_rgba(var(--primary-rgb),0.3)]' 
                            : 'border-white/5 bg-white/5 opacity-60'}"
                    >
                        <span class="text-2xl">{iconMap[sub.name] || '✨'}</span>
                        <span class="text-[9px] font-black uppercase tracking-tighter text-center">{sub.name}</span>
                    </button>
                {/each}
            {:else if selectedParent}
                <button 
                    onclick={() => { selectedCategoryId = selectedParentId; vibrate(10); }}
                    class="col-span-3 flex items-center justify-center gap-3 rounded-[24px] border border-primary bg-primary/10 p-6 text-primary"
                >
                    <span class="text-2xl">{iconMap[selectedParent.name] || '✨'}</span>
                    <span class="font-black uppercase tracking-widest text-xs">Usar {selectedParent.name}</span>
                </button>
            {/if}
        </div>
    </div>

    <div class="space-y-6">
        <input 
            type="text" placeholder="Nota opcional..." bind:value={description}
            class="w-full rounded-2xl border border-white/5 bg-white/5 p-5 text-sm outline-none focus:border-primary/40 transition-colors"
        />

        <button 
            onclick={handleSubmit}
            class="w-full rounded-[24px] bg-primary py-5 text-sm font-black uppercase tracking-[0.3em] text-white shadow-2xl active:scale-[0.97] transition-all"
        >
            Confirmar {typeOptions.find(o => o.value === type)?.label}
        </button>
    </div>
</div>

<style>
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
</style>