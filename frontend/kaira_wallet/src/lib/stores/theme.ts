import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// 1. Definimos el tema inicial
// Si estamos en el navegador, buscamos en localStorage. 
// Si no hay nada o estamos en el servidor (SSR), por defecto es 'dark'.
const initialTheme = browser ? (localStorage.getItem('theme') ?? 'dark') : 'dark';

export const theme = writable<string>(initialTheme);

// 2. Suscripción para reaccionar a los cambios de tema
theme.subscribe((value) => {
    if (browser) {
        // Guardamos la preferencia del usuario
        localStorage.setItem('theme', value);
        
        // Aplicamos el atributo al elemento raíz (html)
        // Esto activará las variables CSS de [data-theme="light"] en tu layout.css
        document.documentElement.setAttribute('data-theme', value);
    }
});