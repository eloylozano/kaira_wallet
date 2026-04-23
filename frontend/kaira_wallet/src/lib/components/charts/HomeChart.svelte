<script lang="ts">
    import ExpenseChart from '$lib/components/charts/ExpenseChart.svelte';
    import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

    let dailyExpenses = $state<Record<string, number>>({});

    // 🟢 LÓGICA DE RELLENO DE DÍAS
    let chartData = $derived(() => {
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth();
        
        // Obtenemos el último día del mes actual (ej: 30 o 31)
        const lastDay = new Date(year, month + 1, 0).getDate();
        
        const fullMonthData = [];

        for (let day = 1; day <= lastDay; day++) {
            // Construimos la clave YYYY-MM-DD para buscar en el objeto del back
            // Importante: Asegurar el formato "2026-04-02" con ceros a la izquierda
            const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            
            fullMonthData.push({
                date: dateKey,
                value: dailyExpenses[dateKey] || 0 // Si no hay dato, es 0
            });
        }

        // Si quieres que el gráfico solo llegue hasta "Hoy", puedes filtrar aquí:
        const today = now.getDate();
        return fullMonthData.slice(0, today);
        
        return fullMonthData;
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

<div class="mt-4">
    <ExpenseChart data={chartData()} />
</div>