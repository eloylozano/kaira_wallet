<script lang="ts">
	let { sort = $bindable<'desc' | 'asc'>() } = $props();

	function btnClass(active: boolean) {
		return (
			'flex-1 rounded-xl p-3 text-sm transition-all ' +
			(active ? 'bg-white/10' : '')
		);
	}
</script>

<div class="flex gap-2 rounded-2xl bg-white/5 p-1">
	<button
		type="button"
		onclick={() => (sort = 'desc')}
		class={btnClass(sort === 'desc')}
	>
		Más recientes
	</button>

	<button
		type="button"
		onclick={() => (sort = 'asc')}
		class={btnClass(sort === 'asc')}
	>
		Más antiguos
	</button>
</div>