import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { apiUrl, setActivePin } from '$lib/config/api';
import { setActiveAccount } from '$lib/stores/account';

const PIN_TIMEOUT = 15 * 60 * 1000;
const ACCESS_KEY = 'last_pin_access';

// Lista de claves globales que deben desvincularse del uso compartido
const SHARED_KEYS = ['monthly_budget', 'inv_target', 'inv_rules', 'inv_colors'];

function cleanAndMigrateAccountStorage(pin: string) {
    if (!browser) return;

    SHARED_KEYS.forEach((key) => {
        const value = localStorage.getItem(key);
        if (value !== null) {
            const scopedKey = `account_${pin}_${key}`;
            // Si la cuenta aún no tiene su propia clave, migramos el valor actual
            if (!localStorage.getItem(scopedKey)) {
                localStorage.setItem(scopedKey, value);
            }
            // Borramos la clave global compartida
            localStorage.removeItem(key);
        }
    });
}

function createAuthStore() {
    let initialState = false;

    if (browser) {
        const lastAccess = localStorage.getItem(ACCESS_KEY);
        if (lastAccess) {
            initialState = (Date.now() - parseInt(lastAccess)) < PIN_TIMEOUT;
        }
    }

    const { subscribe, set } = writable(initialState);

    return {
        subscribe,
        verifyPinAsync: async (inputPin: string): Promise<boolean> => {
            if (!browser) return false;

            try {
                const res = await fetch(apiUrl('/accounts/'), {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Kaira-PIN': inputPin
                    }
                });

                if (res.ok) {
                    const accounts = await res.json();
                    if (Array.isArray(accounts) && accounts.length > 0) {
                        const matchedAccount = accounts.find((a: any) => String(a.pin_code) === String(inputPin)) || accounts[0];

                        const accountToSave = {
                            ...matchedAccount,
                            pin_code: inputPin
                        };

                        // 1. Limpiamos y desacoplamos el localStorage global
                        cleanAndMigrateAccountStorage(inputPin);

                        // 2. Persistimos la cuenta activa y el PIN
                        setActiveAccount(accountToSave);
                        setActivePin(inputPin, accountToSave);

                        return true;
                    }
                }
            } catch (e) {
                console.error('Error al validar PIN:', e);
            }
            return false;
        },
        unlock: () => {
            if (browser) localStorage.setItem(ACCESS_KEY, Date.now().toString());
            set(true);
        },
        lock: () => {
            if (browser) localStorage.removeItem(ACCESS_KEY);
            set(false);
        }
    };
}

export const auth = createAuthStore();