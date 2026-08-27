import { browser } from '$app/environment';
import { apiUrl, getActivePin } from '$lib/config/api';

class SettingsStore {
    #initialBudget = browser ? Number(localStorage.getItem('monthly_budget')) || 350 : 350;
    #initialBackup = browser ? Number(localStorage.getItem('backup_frequency_days')) || 7 : 7;

    monthlyBudget = $state(this.#initialBudget);
    backupFrequency = $state(this.#initialBackup);

    // Cargar desde la API usando el PIN activo
    async fetchSettings(pin: string) {
        try {
            const res = await fetch(apiUrl('/accounts/me'), {
                headers: { 'X-Kaira-PIN': pin }
            });
            if (res.ok) {
                const data = await res.json();
                this.monthlyBudget = data.monthly_budget ?? 350;
            }
        } catch (err) {
            console.error('Error cargando presupuesto:', err);
        }
    }

    // Guardar hacia la API
    async updateBudget(newValue: number, pin: string) {
        try {
            const res = await fetch(apiUrl('/accounts/me'), {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Kaira-PIN': pin
                },
                body: JSON.stringify({ monthly_budget: newValue })
            });
            if (res.ok) {
                this.monthlyBudget = newValue;
            }
        } catch (err) {
            console.error('Error actualizando presupuesto:', err);
        }
    }

    updateBackupFrequency(days: number) {
        this.backupFrequency = Number(days);
        if (browser) {
            localStorage.setItem('backup_frequency_days', String(days));
            try {
                fetch(apiUrl('/backup'), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Kaira-PIN': getActivePin()
                    },
                    body: JSON.stringify({ frequency_days: Number(days) })
                });
            } catch (e) {
                // ignore
            }
        }
    }
}

export const settingsStore = new SettingsStore();