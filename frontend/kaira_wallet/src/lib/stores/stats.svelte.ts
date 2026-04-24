import { transactionsStore } from '$lib/stores/transactions.svelte';

export type MonthOption = { value: number; label: string };
export type YearOption = { value: number; label: string };

class StatsService {
    selectedYear = $state(new Date().getFullYear());
    selectedMonth = $state(new Date().getMonth());

    availableYears = $derived.by(() => {
        const years = new Set<number>();
        const allTrans = transactionsStore.all ?? [];

        allTrans.forEach(t => {
            if (!t.date) return;
            const d = new Date(t.date);
            if (!isNaN(d.getTime())) years.add(d.getFullYear());
        });

        if (years.size === 0) years.add(new Date().getFullYear());

        return Array.from(years)
            .sort((a, b) => b - a)
            .map(y => ({ value: y, label: String(y) }));
    });

    availableMonths = $derived.by(() => {
        // Si prefieres que siempre salgan todos los meses del año seleccionado:
        return Array.from({ length: 12 }, (_, i) => ({
            value: i,
            label: new Intl.DateTimeFormat('es-ES', { month: 'long' }).format(new Date(2000, i, 1))
        }));
    });
}

export const statsService = new StatsService();