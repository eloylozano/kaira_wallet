import { browser } from '$app/environment';
import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

export interface Category {
    id: number;
    name: string;
    transaction_type: 'expense' | 'income' | 'invest';
    subcategories: Category[];
    parent_id: number | null;
}

// Estado reactivo de Svelte 5
let _categories = $state<Category[]>(
    browser && localStorage.getItem('kaira_categories')
        ? JSON.parse(localStorage.getItem('kaira_categories')!)
        : []
);

export const categoriesStore = {
    // Usamos un getter para que la reactividad fluya
    get all() { return _categories; },

    getByType(type: 'expense' | 'income' | 'invest') {
        return _categories.filter(c => c.transaction_type === type);
    },

    async refresh() {
        if (!PUBLIC_API_URL) return;

        // Limpiamos la URL para que siempre termine en /categories/
        const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');
        const targetUrl = `${baseUrl}/categories/`;

        try {
            console.log("Intentando fetch a:", targetUrl);
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'X-Kaira-PIN': PUBLIC_KAIRA_PIN
                }
            });

            if (response.ok) {
                const data = await response.json();
                _categories = data;
                if (browser) {
                    localStorage.setItem('kaira_categories', JSON.stringify(data));
                }
                console.log("✅ Store actualizado con éxito");
            } else {
                const errorText = await response.text();
                console.error(`❌ Error ${response.status}: ${errorText}`);
            }
        } catch (err) {
            console.error("❌ Error de red conectando a la API:", err);
        }
    }
};