<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAccounts, setActiveAccount, loadActiveAccountFromStorage } from '$lib/stores/account';
    import type { Account } from '$lib/stores/account';
    import { activeAccount } from '$lib/stores/account';
    import { auth } from '$lib/stores/session/auth';
    import * as Icons from 'lucide-svelte';

    function kebabToPascal(name: string) {
        return name ? name.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('') : '';
    }
    import { goto } from '$app/navigation';

    let accounts = $state<Account[]>([]);
    let loading = $state(true);
    let error = $state<string | null>(null);

    onMount(async () => {
        // Load persisted active account if any
        loadActiveAccountFromStorage();
        try {
            accounts = await fetchAccounts();
        } catch (e) {
            // If backend not available, fallback to local storage only
            console.warn('No se pudieron obtener cuentas', e);
            accounts = [];
        }
        // If backend returned no accounts, fallback to statically mapped accounts (pins)
        if (accounts.length === 0) {
            try {
                const mapped = auth.getAllMappedAccounts?.();
                if (mapped && mapped.length > 0) accounts = mapped as Account[];
            } catch (e) {
                // ignore
            }
        }
        loading = false;
    });

    function selectAccount(acc: Account) {
        setActiveAccount(acc);
        // Los stores se vuelven a cargar con la cabecera de la nueva cuenta.
        window.location.assign('/');
    }

    function signOut() {
        try { localStorage.removeItem('kaira_active_account'); } catch (e) {}
        activeAccount.set(null);
        auth.lock();
        goto('/');
    }
</script>

<main class="mx-auto max-w-xl p-4">
    <header class="mb-6">
        <h1 class="text-3xl font-black">Perfil</h1>
        <p class="text-sm opacity-60">Gestiona cuentas y sesión</p>
    </header>

    {#if loading}
        <p>Cargando cuentas...</p>
    {:else}
        {#if accounts.length === 0}
            <p class="mb-4">No hay cuentas disponibles. Puedes usar la aplicación con la cuenta local.</p>
        {/if}

        <div class="mb-6">
            <div class="flex gap-3 overflow-x-auto py-2">
                {#each accounts as acc}
                    <div class="min-w-[160px] flex-shrink-0">
                        <div class="flex flex-col gap-2 rounded-xl border p-3 bg-white/2 transition { $activeAccount?.id === acc.id ? 'ring-2 ring-emerald-400' : '' }">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center">
                                        {#if (Icons as any)[kebabToPascal(acc.icon || 'user')]}
                                            <svelte:component this={(Icons as any)[kebabToPascal(acc.icon || 'user')]} width="20" height="20" />
                                        {:else}
                                            <span class="text-sm">{acc.name?.charAt(0) || '?'}</span>
                                        {/if}
                                    </div>
                                    <div>
                                        <div class="font-semibold">{acc.name}</div>
                                        <div class="text-xs opacity-60">{acc.description || ''}</div>
                                    </div>
                                </div>
                                <div>
                                    <button class="px-3 py-1 rounded bg-emerald-500 text-white" onclick={() => selectAccount(acc)}>Seleccionar</button>
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <div class="mt-6">
            <button class="px-4 py-2 rounded bg-red-600 text-white" onclick={signOut}>Cerrar sesión</button>
        </div>
    {/if}
</main>
