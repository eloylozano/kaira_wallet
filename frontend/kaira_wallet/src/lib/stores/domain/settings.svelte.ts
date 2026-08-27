import { browser } from '$app/environment';
import { apiUrl } from '$lib/config/api';

class SettingsStore {
    monthlyBudget = $state<number>(350);

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
}

export const settingsStore = new SettingsStore();