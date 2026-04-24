import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

let _transactions = $state<any[]>([]);
let _total = $state(0);

export const transactionsStore = {
	get all() {
		return _transactions;
	},

	get total() {
		return _total;
	},

	set(data: any[]) {
		_transactions = Array.isArray(data) ? [...data] : [];
	},

	findLocal(id: number) {
		return _transactions.find(t => t.id === id);
	},

	async getById(id: number) {
		const local = this.findLocal(id);

		if (local) return local;

		try {
			const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');

			const res = await fetch(
				`${baseUrl}/transactions/${id}`,
				{
					headers: {
						'X-Kaira-PIN': PUBLIC_KAIRA_PIN
					}
				}
			);

			if (!res.ok) return null;

			return await res.json();

		} catch (err) {
			console.error('Error loading transaction', err);
			return null;
		}
	},


	// Dentro de transactionsStore
	async getGlobalStats() {
		try {
			const res = await fetch(`${PUBLIC_API_URL}/stats/`, {
				headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
			});
			if (res.ok) {
				return await res.json(); // Esto devuelve total_income, total_expense, etc.
			}
		} catch (err) {
			console.error("Error cargando stats globales", err);
		}
		return null;
	},
	
	async update(id: number, payload: any) {
		try {
			const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');

			const res = await fetch(
				`${baseUrl}/transactions/${id}`,
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'X-Kaira-PIN': PUBLIC_KAIRA_PIN
					},
					body: JSON.stringify(payload)
				}
			);

			if (!res.ok) {
				throw new Error('Error updating transaction');
			}

			const updated = await res.json();

			_transactions = _transactions.map(t =>
				t.id === id ? updated : t
			);

			return updated;

		} catch (err) {
			console.error(err);
			return null;
		}
	},

	async fetch(params?: {
		transaction_type?: string;
		is_paid?: boolean;
		search?: string;
		skip?: number;
		limit?: number;
		sort?: 'asc' | 'desc';
	}) {

		const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');

		const query = new URLSearchParams();

		if (params?.transaction_type) {
			query.append('transaction_type', params.transaction_type);
		}

		if (params?.is_paid !== undefined) {
			query.append('is_paid', String(params.is_paid));
		}

		if (params?.sort) {
			query.append('sort', params.sort);
		}

		if (params?.search) {
			query.append('search', params.search);
		}

		const countQuery = new URLSearchParams(query);

		query.append('skip', String(params?.skip ?? 0));
		query.append('limit', String(params?.limit ?? 20));

		try {

			const [resData, resCount] = await Promise.all([
				fetch(
					`${baseUrl}/transactions/?${query}`,
					{
						headers: {
							'X-Kaira-PIN': PUBLIC_KAIRA_PIN
						}
					}
				),

				fetch(
					`${baseUrl}/transactions/count?${countQuery}`,
					{
						headers: {
							'X-Kaira-PIN': PUBLIC_KAIRA_PIN
						}
					}
				)
			]);

			if (resData.ok) {
				this.set(await resData.json());
			}

			if (resCount.ok) {
				const json = await resCount.json();
				_total = json.total;
			}

		} catch (err) {
			console.error('Store error:', err);
		}


	}


	// D
};