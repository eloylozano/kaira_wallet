// $lib/stores/session/auth.ts
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const PIN_TIMEOUT = 15 * 60 * 1000; 
const PIN_KEY = 'kaira_user_pin';
const ACCESS_KEY = 'last_pin_access';

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
        // Verifica si el PIN introducido coincide con el guardado
        verifyPin: (inputPin: string) => {
            if (!browser) return false;
            const savedPin = localStorage.getItem(PIN_KEY) || '1234';
            return inputPin === savedPin;
        },
        // Permite cambiar el PIN desde otra parte de la app
        updatePin: (newPin: string) => {
            if (browser && newPin.length === 4) {
                localStorage.setItem(PIN_KEY, newPin);
                return true;
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