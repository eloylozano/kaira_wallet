export function groupByMonth(transactions: any[]) {
	const grouped: Record<string, any[]> = {};

	for (const tx of transactions) {
		const date = new Date(tx.date);

		const key = date.toLocaleDateString('es-ES', {
			month: 'long',
			year: 'numeric'
		});

		if (!grouped[key]) grouped[key] = [];
		grouped[key].push(tx);
	}

	return grouped;
}