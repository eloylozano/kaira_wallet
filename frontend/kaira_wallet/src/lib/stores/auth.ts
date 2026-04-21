// $lib/stores/auth.ts
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const PIN_TIMEOUT = 15 * 60 * 1000; 

function createAuthStore() {
    let initialState = false;
    
    if (browser) {
        const lastAccess = localStorage.getItem('last_pin_access');
        if (lastAccess) {
            initialState = (Date.now() - parseInt(lastAccess)) < PIN_TIMEOUT;
        }
    }

    const { subscribe, set } = writable(initialState);

    return {
        subscribe,
        unlock: () => {
            if (browser) localStorage.setItem('last_pin_access', Date.now().toString());
            set(true);
        },
        lock: () => {
            if (browser) localStorage.removeItem('last_pin_access');
            set(false);
        }
    };
}

export const auth = createAuthStore();