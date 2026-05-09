import { apiUrl, KAIRA_PIN } from '$lib/config/api';
import { transactionsStore } from '$lib/stores/transactions.svelte';

class StatsService {
    selectedYear = $state(new Date().getFullYear());
    selectedMonth = $state(new Date().getMonth());

    // 🔥 Estado principal (NORMALIZADO)
    monthlyStatsData = $state({
        income: 0,
        expense: 0,
        invest: 0,
        savings: 0,
        net: 0,

        fixed_total: 0,
        variable_total: 0,
        total_expense: 0,
        fixed_ratio: 0,

        cash_ratio: 0,
        invested_ratio: 0
    });

    monthlyBreakdown = $state<any[]>([]);

    // 🔥 distribución separada (más clara)
    distributionData = $state({
        expenses: [] as any[],
        pareto: [] as any[],
        investments: {
            cash_ratio: {
                cash: 0,
                invested: 0,
                ratio: 0
            },
            allocation: [] as any[]
        }
    });

    async fetchMonthlyStats() {
        try {
            const sqlMonth = this.selectedMonth + 1;

            const [boxesRes, breakdownRes, structureRes] = await Promise.all([
                fetch(
                    apiUrl(`/stats/monthly-boxes?year=${this.selectedYear}&month=${sqlMonth}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                ),

                fetch(
                    apiUrl(`/stats/monthly-breakdown?year=${this.selectedYear}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                ),

                fetch(
                    apiUrl(`/stats/expense-structure?year=${this.selectedYear}&month=${sqlMonth}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                )
            ]);

            if (boxesRes.ok) {
                const boxes = await boxesRes.json();

                this.monthlyStatsData = {
                    ...this.monthlyStatsData,
                    ...boxes
                };
            }

            if (breakdownRes.ok) {
                this.monthlyBreakdown = await breakdownRes.json();
            }

            if (structureRes.ok) {
                const structure = await structureRes.json();

                this.monthlyStatsData = {
                    ...this.monthlyStatsData,
                    ...structure
                };
            }
        } catch (err) {
            console.error('Error cargando estadísticas:', err);
        }
    }

    async fetchDistributionData() {
        try {
            const sqlMonth = this.selectedMonth + 1;

            const [expRes, paretoRes, investRes] = await Promise.all([
                fetch(
                    apiUrl(`/stats/distribution/expenses?year=${this.selectedYear}&month=${sqlMonth}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                ),
                fetch(
                    apiUrl(`/stats/distribution/pareto?year=${this.selectedYear}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                ),
                fetch(
                    apiUrl(`/stats/distribution/investments?year=${this.selectedYear}&month=${sqlMonth}`),
                    { headers: { 'X-Kaira-PIN': KAIRA_PIN } }
                )
            ]);

            if (expRes.ok) {
                const data = await expRes.json();
                this.distributionData.expenses = Array.isArray(data) ? data : [];
            }

            if (paretoRes.ok) {
                this.distributionData.pareto = await paretoRes.json();
            }

            if (investRes.ok) {
                const data = await investRes.json();

                // ✅ Sincronizamos con el nuevo objeto del Backend
                this.distributionData.investments = {
                    cash_ratio: data.cash_ratio || { cash: 0, invested: 0 },
                    allocation: Array.isArray(data.allocation) ? data.allocation : []
                };
            }
        } catch (err) {
            console.error('Error en distribución:', err);
        }
    }

    // utilidades UI
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
        const now = new Date();

        const totalDays = new Date(year, month + 1, 0).getDate();

        if (now.getFullYear() === year && now.getMonth() === month) {
            return {
                current: totalDays - now.getDate() + 1,
                total: totalDays
            };
        }

        return { current: totalDays, total: totalDays };
    }

    summaryData = $state({
        total_income: 0,
        total_expense: 0,
        total_invest: 0
    });

    globalBalance = $state(0);

    // 2. Método para traer ambos datos
    async fetchHomeData(year: number) {
        try {
            const [summaryRes, globalRes] = await Promise.all([
                fetch(apiUrl(`/stats/summary?year=${year}`), {
                    headers: { 'X-Kaira-PIN': KAIRA_PIN }
                }),
                fetch(apiUrl('/stats/summary'), {
                    headers: { 'X-Kaira-PIN': KAIRA_PIN }
                })
            ]);

            if (summaryRes.ok) {
                this.summaryData = await summaryRes.json();
            }

            if (globalRes.ok) {
                const global = await globalRes.json();
                this.globalBalance = Number(global.total_income) -
                    Number(global.total_expense) -
                    Number(global.total_invest);
            }
        } catch (err) {
            console.error('Error cargando datos del Home:', err);
        }
    }

    equityEvolution = $state<any[]>([]);
    assetTypes = $state<any[]>([]);
    equityLoading = $state(false);

    // 2. Nuevo método para cargar todo lo referente a Patrimonio
    async fetchEquityData() {
        this.equityLoading = true;
        try {
            const headers = { 'X-Kaira-PIN': KAIRA_PIN };
            const [resEvolution, resAssets, resGlobal] = await Promise.all([
                fetch(apiUrl('/stats/equity/evolution'), { headers }),
                fetch(apiUrl('/stats/equity/asset-types'), { headers }),
                fetch(apiUrl('/stats/'), { headers }) // Para los totales generales
            ]);

            if (resEvolution.ok) this.equityEvolution = await resEvolution.json();
            if (resAssets.ok) this.assetTypes = await resAssets.json();
            if (resGlobal.ok) {
                const global = await resGlobal.json();
                // Aprovechamos para actualizar summaryData si lo necesitas
                this.summaryData = {
                    total_income: global.total_income,
                    total_expense: global.total_expense,
                    total_invest: global.total_invest
                };
            }
        } catch (err) {
            console.error('Error en fetchEquityData:', err);
        } finally {
            this.equityLoading = false;
        }
    }
}

export const statsService = new StatsService();