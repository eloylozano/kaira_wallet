import { browser } from '$app/environment';
import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

export interface Category {
	id: number;
	name: string;
	transaction_type: 'expense' | 'income' | 'invest';
	subcategories: Category[];
	parent_id: number | null;
}

let _categories = $state<Category[]>(
	browser && localStorage.getItem('kaira_categories')
		? JSON.parse(localStorage.getItem('kaira_categories')!)
		: []
);

export const categoriesStore = {
	get all() {
		return _categories;
	},

	set(data: Category[]) {
		_categories = Array.isArray(data) ? data : [];

		if (browser) {
			localStorage.setItem('kaira_categories', JSON.stringify(_categories));
		}
	},

	getByType(type: Category['transaction_type']) {
		return _categories.filter(c => c.transaction_type === type);
	},

	async refresh() {
		if (!PUBLIC_API_URL) return;

		const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');
		const url = `${baseUrl}/categories/`;

		try {
			const res = await fetch(url, {
				method: 'GET',
				headers: {
					'Accept': 'application/json',
					'X-Kaira-PIN': PUBLIC_KAIRA_PIN
				}
			});

			if (!res.ok) {
				console.error('❌ Error API categories');
				return;
			}

			const data = await res.json();

			this.set(data);

			console.log('✅ Categories loaded:', data.length);
		} catch (err) {
			console.error('❌ Network error:', err);
		}
	}
};