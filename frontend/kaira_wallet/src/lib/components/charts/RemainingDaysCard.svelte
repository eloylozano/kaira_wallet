<script lang="ts">
    import { statsService } from '$lib/stores/stats.svelte';
    
    // Obtenemos los datos del store
    let stats = $derived(statsService.daysRemaining);
    
    // Calculamos el progreso como el tiempo transcurrido
    // Si quedan 2 días de 30, el progreso será (30 - 2) / 30 = 93%
    let daysPassed = $derived(stats.total - stats.current);
    let progress = $derived(stats.total > 0 ? (daysPassed / stats.total) * 100 : 0);

    // Color dinámico: si queda muy poco (ej. menos de 3 días), el color cambia sutilmente
    let isEnding = $derived(stats.current <= 3 && stats.current > 0);
</script>

<div class="glass-panel flex flex-col justify-between rounded-[32px] border border-white/10 bg-white/5 p-5">
    <div>
        <p class="text-[8px] font-black tracking-[0.2em] uppercase opacity-40">Días restantes</p>
        
        <div class="flex items-baseline gap-1">
            <p class="mt-2 text-3xl font-black">
                {stats.current}
            </p>
            <p class="text-[10px] font-bold italic opacity-30">
                de {stats.total} {stats.total === 1 ? 'día' : 'días'}
            </p>
        </div>
    </div>

    <div class="mt-4">
        <div class="flex justify-between mb-1.5 px-1">
             <span class="text-[8px] font-bold uppercase opacity-30">Progreso del mes</span>
             <span class="text-[8px] font-bold opacity-40">{Math.round(progress)}%</span>
        </div>
        
        <div class="h-1.5 overflow-hidden rounded-full bg-white/10">
            <div 
                class="h-full transition-all duration-1000 ease-out {isEnding ? 'bg-amber-400' : 'bg-primary'}" 
                style="width: {progress}%"
            >
                <div class="h-full w-full bg-white/20 blur-sm"></div>
            </div>
        </div>
    </div>
</div>