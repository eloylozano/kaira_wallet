import { writable } from 'svelte/store';
import { PUBLIC_API_URL, KAIRA_PIN } from '$env/static/public';

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
                // Usamos la URL desde la variable de entorno pública
                const response = await fetch(`${PUBLIC_API_URL}/categories/?user_id=${userId}`, {
                    method: 'GET',
                    headers: {
                        'accept': 'application/json',
                        // Usamos el PIN desde la variable de entorno pública
                        'X-Kaira-PIN': KAIRA_PIN 
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    set(data);
                } else {
                    console.error("Error en la respuesta del servidor:", response.status);
                }
            } catch (error) {
                console.error("Error de conexión cargando categorías:", error);
            }
        },
        reset: () => set([])
    };
}

export const categoryStore = createCategoryStore();