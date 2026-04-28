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
		const protocol = window.location.protocol || 'http:';
		const hostname = window.location.hostname || 'localhost';
		return `${protocol}//${hostname}:8000`;
	}

	return 'http://localhost:8000';
}

export function apiUrl(path: string): string {
	const normalizedPath = path.startsWith('/') ? path : `/${path}`;
	return `${getApiBaseUrl()}${normalizedPath}`;
}

export const KAIRA_PIN = PUBLIC_KAIRA_PIN;
