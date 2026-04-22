import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

let _transactions = $state<any[]>([]);
let _total = $state(0); // <--- Nuevo estado para el total

export const transactionsStore = {
    get all() { return _transactions; },
    get total() { return _total; },
    set(data: any[]) {
        _transactions = [...data];
    },

    async fetch(params?: {
        transaction_type?: string;
        is_paid?: boolean;
        skip?: number;
        limit?: number;
        sort?: 'asc' | 'desc';
    }) {
        const baseUrl = PUBLIC_API_URL.replace(/\/$/, '');
        const query = new URLSearchParams();

        if (params?.transaction_type) query.append('transaction_type', params.transaction_type);
        if (params?.is_paid !== undefined) query.append('is_paid', String(params.is_paid));
        if (params?.sort) query.append('sort', params.sort);
        // Clonamos los params de filtro para el contador (el contador no usa skip/limit)
        const countQuery = new URLSearchParams(query);

        // Añadimos paginación a la query principal
        query.append('skip', String(params?.skip ?? 0));
        query.append('limit', String(params?.limit ?? 20));

        try {
            // Ejecutamos ambas peticiones (Datos y Total) en paralelo para ir más rápido
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
                const countJson = await resCount.json();
                _total = countJson.total; // Guardamos el total real
            }
        } catch (error) {
            console.error('❌ Error en el store:', error);
        }
    }
};