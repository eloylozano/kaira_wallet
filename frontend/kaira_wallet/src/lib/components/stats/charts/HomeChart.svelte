<script lang="ts">
	import ExpenseChart from '$lib/components/stats/charts/ExpenseChart.svelte';
	import { apiUrl, getApiHeaders } from '$lib/config/api';

	let dailyExpenses = $state<Record<string, number>>({});

	// 🟢 LÓGICA DE RELLENO DE DÍAS
	let chartData = $derived(() => {
		const now = new Date();
		const year = now.getFullYear();
		const month = now.getMonth();
		
		const lastDay = new Date(year, month + 1, 0).getDate();
		const fullMonthData = [];

		for (let day = 1; day <= lastDay; day++) {
			const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
			
			fullMonthData.push({
				date: dateKey,
				value: dailyExpenses[dateKey] || 0
			});
		}

		const today = now.getDate();
		return fullMonthData.slice(0, today);
	});

	$effect(() => {
		fetch(apiUrl('/stats/daily-expenses'), {
			headers: getApiHeaders()
		})
			.then(r => r.json())
			.then(data => dailyExpenses = data || {})
			.catch(() => dailyExpenses = {});
	});
</script>

<div class="mt-4">
	<ExpenseChart data={chartData()} />
</div>