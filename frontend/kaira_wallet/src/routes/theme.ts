import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Leemos de localStorage si existe, si no, 'dark' por defecto
const initialTheme = browser ? (localStorage.getItem('theme') ?? 'dark') : 'dark';

export const theme = writable(initialTheme);

theme.subscribe((value) => {
    if (browser) {
        localStorage.setItem('theme', value);
        // Aplicamos el atributo al HTML
        document.documentElement.setAttribute('data-theme', value);
    }
});