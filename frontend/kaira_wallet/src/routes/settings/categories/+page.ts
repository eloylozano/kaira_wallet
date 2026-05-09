import { categoriesStore } from '$lib/stores/domain/categories.svelte';
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    // Esto llena el store antes de que la página cargue
    await categoriesStore.refresh();
    return {};
};