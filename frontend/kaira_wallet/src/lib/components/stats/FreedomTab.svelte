<script>
	import { statsService } from "$lib/stores/stats.svelte";
	import DailyBudgetCard from "../charts/DailyBudgetCard.svelte";
	import RemainingDaysCard from "../charts/RemainingDaysCard.svelte";
	import SavingsCircle from "../charts/SavingsCircle.svelte";
	import YearlyFlowChart from "../charts/YearlyFlowChart.svelte";

</script>
<div class="flex flex-col gap-6">
    <SavingsCircle ... />

    <div class="grid grid-cols-2 gap-4">
        <DailyBudgetCard />
        <RemainingDaysCard />
    </div>

    <div class="glass-panel rounded-[28px] border border-white/10 p-5 bg-white/5">
        <h3 class="text-[10px] font-black uppercase tracking-widest opacity-40 mb-4">Salud Financiera</h3>
        <div class="space-y-4">
            <div class="flex justify-between items-end">
                <span class="text-xs font-bold opacity-70">Gastos Fijos</span>
                <span class="text-sm font-black italic">{statsService.monthlyStatsData.fixed_total}€</span>
            </div>
            <div class="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-primary" style="width: 65%"></div>
            </div>
            <p class="text-[9px] opacity-40">Tus costes fijos representan el 42% de tus ingresos.</p>
        </div>
    </div>

    <YearlyFlowChart />
</div>