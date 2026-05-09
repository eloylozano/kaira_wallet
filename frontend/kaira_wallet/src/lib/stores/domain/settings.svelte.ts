// src/lib/stores/domain/settings.svelte.ts
import { browser } from '$app/environment';

class SettingsStore {
    // Leemos el valor inicial de localStorage si existe
    #initialBudget = browser ? Number(localStorage.getItem('monthly_budget')) || 350 : 350;
    
    monthlyBudget = $state(this.#initialBudget);

    updateBudget(newValue: number) {
        this.monthlyBudget = newValue;
        if (browser) {
            localStorage.setItem('monthly_budget', newValue.toString());
        }
    }
}

export const settingsStore = new SettingsStore();
