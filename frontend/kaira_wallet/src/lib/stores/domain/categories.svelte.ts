import { browser } from '$app/environment';
import { apiUrl, KAIRA_PIN } from '$lib/config/api';

export interface Category {
	id: number;
	name: string;
	icon?: string;
	transaction_type: 'expense' | 'income' | 'invest';
	subcategories: Category[];
	parent_id: number | null;
}

// 1. Inicializamos con un array vacío para evitar errores de hidratación
let _categories = $state<Category[]>([]);

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

	// 2. Usamos una función que aprovecha la reactividad de _categories
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
					'X-Kaira-PIN': KAIRA_PIN
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

	// 3. Método para inicializar el store (Llamar en el layout o componente raíz)
	init() {
		if (browser) {
			const saved = localStorage.getItem('kaira_categories');
			if (saved) {
				_categories = JSON.parse(saved);
			}
			// Siempre refrescamos para obtener la categoría nueva que añadiste
			this.refresh();
		}
	}
};
