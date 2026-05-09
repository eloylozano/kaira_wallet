<script lang="ts">
	let { sort = $bindable() } = $props();
</script>

<div class="kaira-panel flex rounded-2xl p-1">
	<button
		onclick={() => (sort = 'desc')}
		class="flex-1 rounded-xl py-2 text-[10px] font-black uppercase transition-all
{sort === 'desc' ? 'kaira-chip-active' : 'kaira-soft'}"
	>
		Recientes
	</button>

	<button
		onclick={() => (sort = 'asc')}
		class="flex-1 rounded-xl py-2 text-[10px] font-black uppercase transition-all
{sort === 'asc' ? 'kaira-chip-active' : 'kaira-soft'}"
	>
		Antiguos
	</button>
</div>
