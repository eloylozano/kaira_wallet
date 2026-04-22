<script lang="ts">
	let { value = $bindable(true) } = $props();
</script>

<div class="grid grid-cols-2 gap-2 rounded-[28px] border border-white/5 bg-white/5 p-1 sm:p-1.5">

	<button
		type="button"
		onclick={() => (value = true)}
		class="
			flex items-center justify-center
			rounded-[22px]
			py-2 sm:py-4
			text-[10px] sm:text-[11px]
			font-black uppercase tracking-widest
			transition-all
			{value ? 'kaira-chip-active' : 'kaira-soft'}
		"
	>
		Pagado
	</button>

	<button
		type="button"
		onclick={() => (value = false)}
		class="
			flex items-center justify-center
			rounded-[22px]
			py-2 sm:py-4
			text-[10px] sm:text-[11px]
			font-black uppercase tracking-widest
			transition-all
			{!value ? 'bg-[color:var(--warning)] text-black shadow-lg' : 'kaira-soft'}
		"
	>
		Pendiente
	</button>

</div>