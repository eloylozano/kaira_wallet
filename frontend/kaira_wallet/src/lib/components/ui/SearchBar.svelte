<script lang="ts">
	import { Search,X } from 'lucide-svelte';
	let { search=$bindable('') } = $props();
</script>

<div class="relative group">
	<Search class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 kaira-soft"/>

	<input
		type="text"
		bind:value={search}
		placeholder="Buscar movimientos..."
		class="kaira-input w-full rounded-2xl py-4 pl-11 pr-11 text-sm transition-all"
	/>

	{#if search}
	<button
		onclick={() => search=''}
		class="absolute right-4 top-1/2 -translate-y-1/2 kaira-soft"
	>
		<X class="h-4 w-4"/>
	</button>
	{/if}
</div>