<script lang="ts">
	let { type=$bindable(''), isPaid=$bindable('') } = $props();

	const types = [
	{value:'',label:'Todos'},
	{value:'expense',label:'Gastos'},
	{value:'income',label:'Ingresos'},
	{value:'invest',label:'Inversión'}
	];
</script>

<div class="space-y-4">

<div class="flex gap-2 overflow-x-auto py-1">
{#each types as t}
<button
onclick={() => type=t.value}
class="flex-none rounded-xl px-4 py-2 text-[10px] font-bold uppercase border transition-all
{type===t.value ? 'kaira-chip-active' : 'kaira-chip'}"
>
{t.label}
</button>
{/each}
</div>


<div class="flex items-center justify-between px-2">
<span class="text-[10px] font-black uppercase tracking-widest kaira-soft">
Estado de pago
</span>

<div class="kaira-panel flex rounded-xl p-1">

{#each ['',true,false] as val}
<button
onclick={() => isPaid=val}
class="px-3 py-1.5 rounded-lg text-[9px] font-bold uppercase transition-all
{isPaid===val ? 'kaira-chip-active' : 'kaira-soft'}"
>
{val==='' ? 'Todos' : val ? 'Pagado':'Pendiente'}
</button>
{/each}

</div>
</div>

</div>