<script lang="ts">
    import ExpenseChart from '$lib/components/charts/ExpenseChart.svelte';
    import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

    let dailyExpenses = $state<Record<string, number>>({});

    // 🟢 LÓGICA DE FILTRADO POR MES ACTUAL
    let chartData = $derived(() => {
        const now = new Date();
        // Primer día del mes actual a las 00:00:00
        const firstDayOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);

        return Object.entries(dailyExpenses)
            .map(([date, value]) => ({
                date,
                value: Number(value || 0),
                timestamp: new Date(date).getTime()
            }))
            // Filtramos solo los que pertenecen al mes actual
            .filter(item => item.timestamp >= firstDayOfMonth.getTime())
            .sort((a, b) => a.timestamp - b.timestamp)
            .map(({ date, value }) => ({ date, value }));
    });

    $effect(() => {
        fetch(`${PUBLIC_API_URL}/stats/daily-expenses`, {
            headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
        })
            .then(r => r.json())
            .then(data => dailyExpenses = data || {})
            .catch(() => dailyExpenses = {});
    });
</script>

<div class="mt-6">
    <ExpenseChart data={chartData()} />
</div>