export const transactionTypeLabel: Record<string, string> = {
	expense: 'Gasto',
	income: 'Ingreso',
	invest: 'Inversión'
};

export const transactionTypeBadge: Record<
	string,
	{ label: string; color: string }
> = {
	expense: { label: 'Gasto', color: '#ef4444' },
	income: { label: 'Ingreso', color: '#22c55e' },
	invest: { label: 'Inversión', color: '#3b82f6' }
};