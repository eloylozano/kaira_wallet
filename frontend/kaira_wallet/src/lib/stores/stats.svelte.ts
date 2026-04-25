import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';
import { transactionsStore } from '$lib/stores/transactions.svelte';

class StatsService {
	selectedYear = $state(new Date().getFullYear());
	selectedMonth = $state(new Date().getMonth());

	monthlyStatsData = $state({
		income: 0,
		expense: 0,
		savings_amount: 0,
		savings_percent: 0
	});

	monthlyBreakdown = $state<any[]>([]);

	// 📊 FETCH COMPLETO
	async fetchMonthlyStats() {
		try {
			const [statsRes, breakdownRes] = await Promise.all([
				fetch(
					`${PUBLIC_API_URL}/stats/monthly?year=${this.selectedYear}&month=${this.selectedMonth}`,
					{
						headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
					}
				),

				fetch(
					`${PUBLIC_API_URL}/stats/monthly-breakdown?year=${this.selectedYear}`,
					{
						headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
					}
				)
			]);

			if (statsRes.ok) {
				this.monthlyStatsData = await statsRes.json();
			}

			if (breakdownRes.ok) {
				this.monthlyBreakdown = await breakdownRes.json();
			}
		} catch (err) {
			console.error('Error cargando stats', err);
		}
	}

	get availableYears() {
		const years = new Set<number>();
		const all = transactionsStore.all ?? [];

		for (const t of all) {
			if (!t.date) continue;
			const d = new Date(t.date);
			if (!isNaN(d.getTime())) years.add(d.getFullYear());
		}

		if (years.size === 0) years.add(new Date().getFullYear());

		return [...years]
			.sort((a, b) => b - a)
			.map((y) => ({ value: y, label: String(y) }));
	}

	get availableMonths() {
		return Array.from({ length: 12 }, (_, i) => ({
			value: i,
			label: new Intl.DateTimeFormat('es-ES', {
				month: 'long'
			}).format(new Date(2000, i, 1))
		}));
	}

    get daysRemaining() {
	const year = Number(this.selectedYear);
	const month = Number(this.selectedMonth);

	if (isNaN(year) || isNaN(month)) {
		return { current: 0, total: 0 };
	}

	const now = new Date();
	const totalDays = new Date(year, month + 1, 0).getDate();

	if (now.getFullYear() === year && now.getMonth() === month) {
		return {
			current: totalDays - now.getDate() + 1,
			total: totalDays
		};
	}

	return {
		current: totalDays,
		total: totalDays
	};
}
}

export const statsService = new StatsService();