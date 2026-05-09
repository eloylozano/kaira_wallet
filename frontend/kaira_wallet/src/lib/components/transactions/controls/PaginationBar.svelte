<script lang="ts">
	let { page = $bindable(0), onNext, onPrev } = $props();
</script>

<div class="flex items-center justify-between rounded-2xl border border-white/5 bg-white/5 px-4 py-3">
	<button
		onclick={onPrev}
		disabled={page === 0}
		class="rounded-xl bg-white/5 px-4 py-2 text-xs font-bold transition disabled:opacity-30"
	>
		← Anterior
	</button>

	<div class="flex items-center gap-2">
		<span class="text-[11px] font-black uppercase tracking-widest opacity-60">
			Página {page + 1}
		</span>
	</div>

	<button
		onclick={onNext}
		class="rounded-xl bg-emerald-500/10 px-4 py-2 text-xs font-bold text-emerald-300 hover:bg-emerald-500/20 transition"
	>
		Siguiente →
	</button>
</div>