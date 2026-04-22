import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

let _transactions = $state<any[]>([]);

export const transactionsStore = {
	get all() {
		return _transactions;
	},

	set(data: any[]) {
		_transactions = [...data]; 
	},

	async fetch(params?: { type?: string; is_paid?: boolean }) {
		const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');

		const query = new URLSearchParams();

		if (params?.type) query.append('type', params.type);
		if (params?.is_paid !== undefined)
			query.append('is_paid', String(params.is_paid));

		const url = `${baseUrl}/transactions/?${query.toString()}`;

		const res = await fetch(url, {
			headers: {
				'Accept': 'application/json',
				'X-Kaira-PIN': PUBLIC_KAIRA_PIN
			}
		});

		if (!res.ok) {
			console.error('❌ Error fetching transactions', await res.text());
			return;
		}

		const data = await res.json();

		console.log('🔥 transactions recibidas:', data);

		this.set(data);
	}
};