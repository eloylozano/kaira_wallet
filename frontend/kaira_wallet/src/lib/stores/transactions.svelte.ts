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

		// filtros
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

		// 👇 COUNT query (SIN paginación)
		const countQuery = new URLSearchParams(query);

		// paginación SOLO para data
		query.append('skip', String(params?.skip ?? 0));
		query.append('limit', String(params?.limit ?? 20));

		try {
			const [resData, resCount] = await Promise.all([
				fetch(`${baseUrl}/transactions/?${query.toString()}`, {
					headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
				}),
				fetch(`${baseUrl}/transactions/count?${countQuery.toString()}`, {
					headers: { 'X-Kaira-PIN': PUBLIC_KAIRA_PIN }
				})
			]);

			if (resData.ok) {
				const data = await resData.json();
				this.set(data);
			}

			if (resCount.ok) {
				const json = await resCount.json();
				_total = json.total;
			}
		} catch (err) {
			console.error('❌ Error store transactions:', err);
		}
	}
};