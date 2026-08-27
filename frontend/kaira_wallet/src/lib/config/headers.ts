import { getApiHeaders, getActivePin } from '$lib/config/api';

export function authHeaders(contentType: string | null = 'application/json'): Record<string, string> {
    const headers: Record<string, string> = {};
    if (contentType) headers['Content-Type'] = contentType;
    
    // Obtiene dinámicamente el PIN de la cuenta activa desde localStorage / env
    headers['X-Kaira-PIN'] = getActivePin();

    return headers;
}