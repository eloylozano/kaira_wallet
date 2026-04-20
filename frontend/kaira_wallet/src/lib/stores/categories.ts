import { writable } from 'svelte/store';

// Definimos la interfaz según tus schemas de FastAPI
export interface Category {
    id: number;
    name: string;
    description: string | null;
    transaction_type: 'income' | 'expense' | 'invest';
    parent_id: number | null;
    subcategories?: Category[];
}

function createCategoryStore() {
    const { subscribe, set, update } = writable<Category[]>([]);

    return {
        subscribe,
        fetchCategories: async (userId: number) => {
            try {
                // Usamos la URL de tu backend
                const response = await fetch(`http://localhost:8000/categories/?user_id=${userId}`);
                if (response.ok) {
                    const data = await response.json();
                    set(data);
                }
            } catch (error) {
                console.error("Error cargando categorías:", error);
            }
        },
        reset: () => set([])
    };
}

export const categoryStore = createCategoryStore();