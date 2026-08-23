// src/lib/stores/domain/settings.svelte.ts
import { browser } from '$app/environment';
import { apiUrl, KAIRA_PIN } from '$lib/config/api';

class SettingsStore {
    // Leemos el valor inicial de localStorage si existe
    #initialBudget = browser ? Number(localStorage.getItem('monthly_budget')) || 350 : 350;
    #initialBackup = browser ? Number(localStorage.getItem('backup_frequency_days')) || 7 : 7;
    
    monthlyBudget = $state(this.#initialBudget);
    backupFrequency = $state(this.#initialBackup);

    updateBudget(newValue: number) {
        this.monthlyBudget = newValue;
        if (browser) {
            localStorage.setItem('monthly_budget', newValue.toString());
        }
    }

    updateBackupFrequency(days: number) {
        this.backupFrequency = Number(days);
        if (browser) {
            localStorage.setItem('backup_frequency_days', String(days));
            // Fire-and-forget: try to inform backend
            try {
                fetch(apiUrl('/backup'), { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Kaira-PIN': KAIRA_PIN }, body: JSON.stringify({ frequency_days: Number(days) }) });
            } catch (e) {
                // ignore
            }
        }
    }
}

export const settingsStore = new SettingsStore();
