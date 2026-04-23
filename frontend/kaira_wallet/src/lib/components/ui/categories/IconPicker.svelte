<script lang="ts">
	import * as Icons from 'lucide-svelte';
	import { iconGroups } from '$lib/data/iconGroups';

	let { icon = $bindable('') } = $props();

	let activeGroup = $state('money');

	function findGroup(value: string) {
		return Object.entries(iconGroups).find(([_, icons]) =>
			icons.includes(value)
		)?.[0] ?? 'basics';
	}

	function setIcon(i: string) {
		icon = i;
		activeGroup = findGroup(i);
	}

	function toPascal(str: string) {
		return str
			.split('-')
			.map((s) => s.charAt(0).toUpperCase() + s.slice(1))
			.join('');
	}

	function getIcon(name: string) {
		const key = toPascal(name);
		return Icons[key] || Icons.Circle;
	}
</script>

<!-- TABS -->
<div class="mb-3 flex flex-wrap gap-2">
    {#each Object.keys(iconGroups) as g}
        <button
            type="button"
            onclick={() => (activeGroup = g)}
            class="
                /* flex-basis controla el ancho base para que bajen de fila bien */
                flex-grow flex-basis-[calc(50%-8px)] sm:flex-basis-0

                rounded-xl px-2 py-1 text-[10px] font-bold uppercase tracking-widest
                transition text-center
                {activeGroup === g
                    ? 'bg-primary text-white shadow-md'
                    : 'bg-white/5 text-white/40 hover:text-white/70'}
            "
        >
            {g}
        </button>
    {/each}
</div>

<div class="grid grid-cols-5 gap-2">
    {#each iconGroups[activeGroup] as i}
        <button
            type="button"
            onclick={() => setIcon(i)}
            class="
                group flex items-center justify-center
                rounded-xl p-3
                transition-all duration-200
                active:scale-95
                {icon === i
                    ? 'bg-primary text-white shadow-lg scale-105'
                    : 'bg-white/5 text-white/40 hover:bg-white/10 hover:text-white'}
            "
        >
            <svelte:component
                this={getIcon(i)}
                class="h-5 w-5 transition-transform group-hover:scale-110"
            />
        </button>
    {/each}
</div>