<script lang="ts">
	let { sort = $bindable() } = $props();
</script>

<div class="flex rounded-2xl bg-black/20 p-1 border border-white/5">
	<button
		onclick={() => (sort = 'desc')}
		class="flex-1 py-2 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all
		{sort === 'desc' ? 'bg-white/5 text-primary' : 'text-white/20'}"
	>
		Recientes
	</button>
	<button
		onclick={() => (sort = 'asc')}
		class="flex-1 py-2 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all
		{sort === 'asc' ? 'bg-white/5 text-primary' : 'text-white/20'}"
	>
		Antiguos
	</button>
</div>