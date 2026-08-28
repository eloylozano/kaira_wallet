import { browser } from '$app/environment';
import { apiUrl, getApiHeaders, getActivePin } from '$lib/config/api';

export interface Category {
	id: number;
	name: string;
	icon?: string;
	transaction_type: 'expense' | 'income' | 'invest';
	subcategories: Category[];
	parent_id: number | null;
	order?: number;
}

let _categories = $state<Category[]>([]);

function getStorageKey() {
	return `kaira_categories_${getActivePin()}`;
}

export const categoriesStore = {
	get all() {
		return _categories;
	},

	set(data: Category[]) {
		_categories = Array.isArray(data) ? data : [];
		if (browser) {
			localStorage.setItem(getStorageKey(), JSON.stringify(_categories));
		}
	},

	getByType(type: Category['transaction_type']) {
		return _categories.filter(c => c.transaction_type === type);
	},

	async refresh() {
		const url = apiUrl('/categories/');
		try {
			const res = await fetch(url, {
				method: 'GET',
				headers: {
					'Accept': 'application/json',
					...getApiHeaders()
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
	},

	async reorder(items: { id: number; order: number }[]) {
		const url = apiUrl('/categories/reorder');
		try {
			const res = await fetch(url, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
					...getApiHeaders()
				},
				body: JSON.stringify({ items })
			});

			if (!res.ok) {
				console.error('❌ Error reordering categories');
				return;
			}

			// Refrescamos para sincronizar el orden exacto del backend
			await this.refresh();
		} catch (err) {
			console.error('❌ Network error during reorder:', err);
		}
	},

	init() {
		if (browser) {
			_categories = [];
			const saved = localStorage.getItem(getStorageKey());
			if (saved) {
				try {
					_categories = JSON.parse(saved);
				} catch (e) {
					_categories = [];
				}
			}
			this.refresh();
		}
	}
};