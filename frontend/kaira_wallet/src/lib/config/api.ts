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
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000/api';
        }
        return '/api';
    }

    return 'http://localhost:8000/api';
}

export function apiUrl(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    const baseUrl = getApiBaseUrl();
    return `${baseUrl}${normalizedPath}`;
}

export function getActivePin(): string {
    if (typeof window !== 'undefined') {
        try {
            const rawAccount = localStorage.getItem('kaira_active_account');
            if (rawAccount) {
                const account = JSON.parse(rawAccount);
                if (account?.pin_code) {
                    return account.pin_code;
                }
            }
        } catch (e) {
            console.error('Error leyendo PIN de localStorage', e);
        }
    }
    return PUBLIC_KAIRA_PIN || '8825';
}

export function getApiHeaders(extraHeaders: Record<string, string> = {}): Record<string, string> {
    return {
        'Content-Type': 'application/json',
        'X-Kaira-PIN': getActivePin(),
        ...extraHeaders
    };
}

export const KAIRA_PIN = getActivePin();