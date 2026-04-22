<script lang="ts">
	let {
		value = $bindable(''),
		label = 'Nota',
		placeholder = 'Añadir detalles...'
	} = $props();
</script>

<div class="space-y-3">

	<p class="kaira-soft px-2 text-[10px] font-black uppercase tracking-[0.2em]">
		{label}
	</p>

	<div class="kaira-panel rounded-[28px] transition-all focus-within:border-primary/40">

		<textarea
			bind:value
			rows="4"
			placeholder={placeholder}
			class="
				w-full resize-none bg-transparent p-5 text-sm leading-relaxed
				text-main placeholder:text-muted
				outline-none ring-0 border-0
				focus:outline-none focus:ring-0
				appearance-none
			"
		/>

	</div>

</div>