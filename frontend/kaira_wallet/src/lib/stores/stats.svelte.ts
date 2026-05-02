import { apiUrl, KAIRA_PIN } from '$lib/config/api';
import { transactionsStore } from '$lib/stores/transactions.svelte';

class StatsService {
    selectedYear = $state(new Date().getFullYear());
    selectedMonth = $state(new Date().getMonth());

    // Inicializamos el objeto con la estructura exacta que devuelven tus endpoints
    monthlyStatsData = $state({
        income: 0,
        expense: 0,
        invest: 0,
        savings: 0,
        net: 0,
        fixed_total: 0,
        variable_total: 0,
        total_expense: 0,
        fixed_ratio: 0
    });

    monthlyBreakdown = $state<any[]>([]);

    async fetchMonthlyStats() {
        try {
            // Sincronizamos el mes: JS (0-11) -> API (1-12)
            const sqlMonth = this.selectedMonth + 1;

            const [boxesRes, breakdownRes, structureRes] = await Promise.all([
                // 1. Usamos tu nuevo endpoint de cajas
                fetch(
                    apiUrl(`/stats/monthly-boxes?year=${this.selectedYear}&month=${sqlMonth}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                ),
                // 2. Gráfico anual
                fetch(
                    apiUrl(`/stats/monthly-breakdown?year=${this.selectedYear}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                ),
                // 3. Estructura de fijos vs variables
                fetch(
                    apiUrl(`/stats/expense-structure?year=${this.selectedYear}&month=${sqlMonth}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                )
            ]);

            // Procesamos las cajas (Totales)
            if (boxesRes.ok) {
                const boxes = await boxesRes.json();
                this.monthlyStatsData = { ...this.monthlyStatsData, ...boxes };
            }

            // Procesamos el desglose anual
            if (breakdownRes.ok) {
                this.monthlyBreakdown = await breakdownRes.json();
            }

            // Procesamos la estructura de gasto
            if (structureRes.ok) {
                const structure = await structureRes.json();
                this.monthlyStatsData = { ...this.monthlyStatsData, ...structure };
            }
        } catch (err) {
            console.error('Error cargando estadísticas:', err);
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
        return [...years].sort((a, b) => b - a).map((y) => ({ value: y, label: String(y) }));
    }

    get availableMonths() {
        return Array.from({ length: 12 }, (_, i) => ({
            value: i,
            label: new Intl.DateTimeFormat('es-ES', { month: 'long' }).format(new Date(2000, i, 1))
        }));
    }

    get daysRemaining() {
        const year = Number(this.selectedYear);
        const month = Number(this.selectedMonth);
        const now = new Date();
        const totalDays = new Date(year, month + 1, 0).getDate();

        if (now.getFullYear() === year && now.getMonth() === month) {
            return { current: totalDays - now.getDate() + 1, total: totalDays };
        }
        return { current: totalDays, total: totalDays };
    }


    distributionData = $state({
        expenses: [] as any[], // Aquí ahora llegarán objetos tipo {name, value, children}
        pareto: [] as any[],
        investments: {
            cash_ratio: { invested: 0, cash: 0 },
            allocation: [] as any[]
        }
    });

    async fetchDistributionData() {
        try {
            const sqlMonth = this.selectedMonth + 1;
            const [expRes, paretoRes, investRes] = await Promise.all([
                fetch(apiUrl(`/stats/distribution/expenses?year=${this.selectedYear}&month=${sqlMonth}`), { headers: { 'X-Kaira-PIN': KAIRA_PIN } }),
                fetch(apiUrl(`/stats/distribution/pareto?year=${this.selectedYear}`), { headers: { 'X-Kaira-PIN': KAIRA_PIN } }),
                fetch(apiUrl(`/stats/distribution/investments`), { headers: { 'X-Kaira-PIN': KAIRA_PIN } })
            ]);

            if (expRes.ok) this.distributionData.expenses = await expRes.json();
            if (paretoRes.ok) this.distributionData.pareto = await paretoRes.json();
            if (investRes.ok) this.distributionData.investments = await investRes.json();

        } catch (err) {
            console.error('Error en distribución:', err);
        }
    }
}

export const statsService = new StatsService();