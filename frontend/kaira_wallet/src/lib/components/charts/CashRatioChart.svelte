<!-- CashRatioChart.svelte -->
<div class="glass-panel p-6 flex items-center justify-between">
    <div class="flex flex-col">
        <span class="text-3xl font-black italic">25%</span>
        <span class="text-[9px] font-bold opacity-40 uppercase">Efectivo (2% TAE)</span>
    </div>
    
    <div class="relative h-20 w-20">
        <!-- SVG Círculo con dos colores: Sky (Invertido) y Amber (Cash) -->
        <svg viewBox="0 0 36 36" class="h-full w-full">
            <circle cx="18" cy="18" r="16" fill="none" class="stroke-sky-500/20" stroke-width="4"></circle>
            <circle cx="18" cy="18" r="16" fill="none" class="stroke-amber-500" stroke-width="4" stroke-dasharray="25, 100" stroke-linecap="round"></circle>
        </svg>
    </div>
</div>