<script lang="ts">
	import { Search, X } from 'lucide-svelte';
	let { search = $bindable('') } = $props();
</script>

<div class="relative group">
	<Search class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-white/20 group-focus-within:text-white transition-colors" />
	
	<input
		type="text"
		bind:value={search}
		placeholder="Buscar por nombre, categoría o fecha..."
		class="w-full bg-white/5 border border-white/5 rounded-2xl py-4 pl-11 pr-11 text-sm text-white outline-none ring-0 focus:border-white/40 focus:bg-white/10 transition-all placeholder:text-white/20"
	/>

	{#if search}
		<button 
			onclick={() => (search = '')}
			class="absolute right-4 top-1/2 -translate-y-1/2 text-white/20 hover:text-white"
		>
			<X class="h-4 w-4" />
		</button>
	{/if}
</div>