import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

function trimTrailingSlash(value: string): string {
    return value.replace(/\/+$/, '');
}

export function getApiBaseUrl(): string {
    const envUrl = (PUBLIC_API_URL ?? '').trim();
    if (envUrl) {
        return trimTrailingSlash(envUrl);
    }

    if (typeof window !== 'undefined') {
        // Si estás desarrollando en tu PC local (localhost)
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return `http://localhost:8000`;
        }
        
        // En producción (LXC), devolvemos la ruta relativa vacía.
        // Así las peticiones irán a '/api/...' bajo el mismo dominio de la barra de navegación.
        return '/api';
    }

    return 'http://localhost:8000';
}

export function apiUrl(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    const baseUrl = getApiBaseUrl();

    // Si es ruta relativa (producción), evitamos que se duplique la barra si 'baseUrl' es '/api' y 'normalizedPath' es '/summary'
    if (baseUrl === '/api') {
        return `/api${normalizedPath}`;
    }

    return `${baseUrl}${normalizedPath}`;
}

export const KAIRA_PIN = PUBLIC_KAIRA_PIN;