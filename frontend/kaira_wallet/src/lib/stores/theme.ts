import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// 1. Función para obtener el tema del sistema
const getSystemTheme = () => {
    if (!browser) return 'dark';
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
};

// 2. Crear el store con el valor inicial del sistema
export const theme = writable(browser ? (localStorage.getItem('theme') || getSystemTheme()) : 'dark');

// 3. Suscribirse para aplicar el cambio al documento y guardarlo
if (browser) {
    theme.subscribe((value) => {
        document.documentElement.setAttribute('data-theme', value);
        localStorage.setItem('theme', value);
    });

    // 4. ESCUCHAR CAMBIOS EN TIEMPO REAL
    // Si el usuario cambia el modo del sistema mientras usa la app
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
        const newTheme = e.matches ? 'light' : 'dark';
        theme.set(newTheme);
    });
}