<script lang="ts">
    import { iconGroups } from '$lib/data/iconGroups';
    import type { IconGroup } from '$lib/data/iconGroups';
    import { createEventDispatcher } from 'svelte';
    import * as Icons from 'lucide-svelte';

    let { isOpen = false, selected = null }: { isOpen?: boolean; selected?: string | null } = $props();
    let activeGroup = $state<IconGroup>('basics');

    const dispatch = createEventDispatcher();

    function pick(icon: string) {
        dispatch('select', icon);
    }

    function kebabToPascal(name: string) {
        return name.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('');
    }

    function iconComponent(name: string): any {
        return Icons[kebabToPascal(name) as keyof typeof Icons] as any;
    }

    function close() {
        dispatch('close');
    }

    $effect(() => {
        if (selected) {
            activeGroup = (Object.entries(iconGroups).find(([, icons]) => (icons as readonly string[]).includes(selected))?.[0] as IconGroup) ?? 'basics';
        }
    });
</script>

{#if isOpen}
<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6 backdrop-blur-sm">
    <div class="glass-panel w-full max-w-2xl rounded-[28px] border border-white/10 bg-[#020617]/95 p-5 shadow-2xl">
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold">Seleccionar icono de perfil</h3>
            <button type="button" class="text-sm opacity-60 hover:opacity-100" onclick={close}>Cerrar</button>
        </div>

        <div class="mb-4 flex flex-wrap gap-2">
            {#each Object.keys(iconGroups) as group}
                <button type="button" onclick={() => (activeGroup = group as IconGroup)} class="rounded-xl px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest transition {activeGroup === group ? 'bg-primary text-white shadow-md' : 'bg-white/5 text-white/40 hover:bg-white/10 hover:text-white'}">{group}</button>
            {/each}
        </div>

        <div class="grid max-h-[55vh] grid-cols-5 gap-2 overflow-auto pr-1">
            {#each iconGroups[activeGroup] as icon}
                <button type="button" title={icon} onclick={() => pick(icon)} class="group flex aspect-square items-center justify-center rounded-xl p-3 transition-all active:scale-95 {selected === icon ? 'scale-105 bg-primary text-white shadow-lg' : 'bg-white/5 text-white/40 hover:bg-white/10 hover:text-white'}">
                    {#if iconComponent(icon)}
                        <svelte:component this={iconComponent(icon)} class="h-5 w-5 transition-transform group-hover:scale-110" />
                    {:else}
                        <span class="text-xs">{icon}</span>
                    {/if}
                </button>
            {/each}
        </div>
    </div>
</div>
{/if}

