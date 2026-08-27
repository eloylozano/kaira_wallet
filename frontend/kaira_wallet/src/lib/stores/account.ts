import { writable, get } from 'svelte/store';
import { apiUrl, getActivePin } from '$lib/config/api';

export type Account = { 
    id: number; 
    name: string; 
    is_joint?: boolean; 
    pin_code: string; 
    icon?: string 
};

export const activeAccount = writable<Account | null>(null);

export function getAccountPin(): string {
    const acc = get(activeAccount);
    return acc?.pin_code || getActivePin();
}

export async function fetchAccounts() {
    const res = await fetch(apiUrl('/accounts/'), {
        headers: {
            'X-Kaira-PIN': getAccountPin()
        }
    });

    if (!res.ok) throw new Error('Error al obtener cuentas');
    return await res.json();
}

export function setActiveAccount(acc: Account) {
    activeAccount.set(acc);
    try { 
        localStorage.setItem('kaira_active_account', JSON.stringify(acc)); 
    } catch (e) {}
    
    try {
        if (typeof window !== 'undefined' && window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('kaira:account-changed'));
        }
    } catch (e) {}
}

export function loadActiveAccountFromStorage(): Account | null {
    try {
        const raw = localStorage.getItem('kaira_active_account');
        if (raw) {
            const acc: Account = JSON.parse(raw);
            activeAccount.set(acc);
            return acc;
        }
    } catch (e) {}
    return null;
}