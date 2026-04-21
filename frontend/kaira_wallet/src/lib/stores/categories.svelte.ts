// Archivo: src/lib/stores/categories.svelte.ts
import { browser } from '$app/environment';

// Definimos la interfaz basada en tu JSON
export interface Category {
    id: number;
    name: string;
    transaction_type: 'expense' | 'income' | 'invest';
    subcategories: Category[];
    parent_id: number | null;
}

// Estado persistente
let _categories = $state<Category[]>(
    browser && localStorage.getItem('kaira_categories') 
    ? JSON.parse(localStorage.getItem('kaira_categories')!) 
    : []
);

export const categoriesStore = {
    get all() { return _categories; },
    
    // Filtrar por tipo (Gasto, Ingreso, Inversión)
    getByType(type: string) {
        return _categories.filter(c => c.transaction_type === type);
    },

    // Actualizar desde el servidor
    async refresh(pin: string) {
        try {
            const response = await fetch('http://localhost:8000/categories', {
                headers: { 'X-Kaira-PIN': pin }
            });
            if (!response.ok) throw new Error('Error al cargar categorías');
            
            const data = await response.json();
            _categories = data;
            
            if (browser) {
                localStorage.setItem('kaira_categories', JSON.stringify(data));
            }
        } catch (err) {
            console.error("Fallo al sincronizar categorías:", err);
        }
    }
};