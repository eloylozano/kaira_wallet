<script lang="ts">
    let { data = [] } = $props<{ data: { date: string; value: number }[] }>();

    let normalizedData = $derived(
        (data ?? []).reduce((acc, curr) => {
            const d = new Date(curr.date);
            const key = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
            acc[key] = Math.abs(curr.value || 0);
            return acc;
        }, {} as Record<string, number>)
    );

    let chartItems = $derived(() => {
        const now = new Date();
        const today = now.getDate();
        const year = now.getFullYear();
        const month = now.getMonth();
        const fullSeries = [];

        for (let i = 1; i <= today; i++) {
            const key = `${year}-${month + 1}-${i}`;
            const val = normalizedData[key] || 0;
            fullSeries.push({ day: i, displayValue: val });
        }
        return fullSeries;
    });

    let max = $derived(Math.max(...chartItems().map((d) => d.displayValue), 10));

    function getBarHeight(value: number) {
        if (value === 0) return '2px';
        const percentage = (value / max) * 100;
        return `clamp(8px, ${percentage}%, 100%)`;
    }
</script>

<div class="glass-panel relative overflow-hidden rounded-[32px] border border-white/10 p-5">
    <div class="absolute -top-20 -right-20 h-40 w-40 rounded-full bg-rose-500/10 blur-[70px]"></div>

    <div class="relative z-10 mb-8 flex items-center justify-between">
        <p class="text-[10px] font-black uppercase tracking-widest opacity-60">Gastos del mes</p>
        <p class="text-[10px] font-bold text-rose-400/70 uppercase text-right leading-tight">
            Hoy<br/><span class="text-xs">Día {chartItems().length}</span>
        </p>
    </div>

    <div class="relative flex h-44 w-full gap-2">
        
        <div class="flex h-full flex-col justify-between pb-10 text-[7px] font-bold opacity-30 w-8">
            <span>{max.toFixed(0)}€</span>
            <span>{(max / 2).toFixed(0)}€</span>
            <span>0€</span>
        </div>

        <div class="relative flex-1 h-full flex items-end gap-[2px] pb-10">
            {#each chartItems() as d}
                <div class="group relative flex flex-1 flex-col justify-end items-center h-full">
                    
                    <div
                        class="w-full rounded-t-[2px] transition-all duration-500 group-hover:bg-rose-500/80 
                        {d.displayValue > 0 ? 'bg-rose-500/30' : 'bg-white/5'}"
                        style="height: {getBarHeight(d.displayValue)}"
                    ></div>

                    {#if d.day === 1 || d.day % 5 === 0 || d.day === chartItems().length}
                        <span class="absolute -bottom-2 text-[7px] font-bold opacity-40 translate-y-full">
                            {d.day}
                        </span>
                    {/if}

                    {#if d.displayValue > 0}
                        <div class="absolute -top-2 left-1/2 -translate-x-1/2 -translate-y-full scale-75 opacity-0 transition-all duration-300 group-hover:scale-100 group-hover:opacity-100 z-30 pointer-events-none">
                            <div class="whitespace-nowrap rounded-lg bg-white px-2 py-1 text-[10px] font-black text-slate-900 shadow-2xl">
                                {d.displayValue.toFixed(2)}€
                            </div>
                            <div class="w-2 h-2 bg-white rotate-45 mx-auto -mt-1"></div>
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    </div>

    <div class="relative z-10 mt-2 flex justify-between px-10 text-[9px] font-bold uppercase opacity-30 tracking-tighter">
        <span>1 {new Date().toLocaleString('es', {month: 'short'})}</span>
        <span>Corte Hoy</span>
    </div>
</div>

<style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
</style>