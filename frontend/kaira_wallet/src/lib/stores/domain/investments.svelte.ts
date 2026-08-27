import { apiUrl } from '$lib/config/api';

export interface InvestmentRules {
    [key: string]: string;
}

class InvestmentStore {
    rules = $state<InvestmentRules>({
        '500': 'S&P 500',
        'World': 'MSCI World',
        'Emerging': 'EM IMI',
        'Nuclear': 'Nuclear Tech',
        'Semiconductor': 'Semiconductor',
        'Health': 'Health',
        'Gold': 'Gold',
        'IONQ': 'IONQ',
        'SanDisk': 'SanDisk',
        'WD Elements': 'WD Elements',
        'Nvidia': 'Nvidia',
        'Tesla': 'Tesla',
        'Googl': 'Google',
        'Amazon': 'Amazon',
        'BTC': 'BTC',
        'Solana': 'Solana',
        'ETH': 'ETH',
    });

    categoryColors = $state<Record<string, string>>({
        'Fondos indexados': '#00d492',
        'ETF': '#0ea5e9',
        'Crypto': '#f59e0b',
        'Acciones': '#8b5cf6',
        'Otros': '#64748b'
    });

    targetSavings = $state<number>(0);

    async fetchSettings(pin: string) {
        if (!pin) return;
        try {
            const res = await fetch(apiUrl('/accounts/me'), {
                headers: { 'X-Kaira-PIN': pin }
            });
            if (res.ok) {
                const data = await res.json();
                
                if (data.inv_target !== null && data.inv_target !== undefined) {
                    this.targetSavings = Number(data.inv_target);
                }

                if (data.inv_rules) {
                    this.rules = typeof data.inv_rules === 'string' ? JSON.parse(data.inv_rules) : data.inv_rules;
                }
                if (data.inv_colors) {
                    this.categoryColors = typeof data.inv_colors === 'string' ? JSON.parse(data.inv_colors) : data.inv_colors;
                }
            }
        } catch (err) {
            console.error('Error cargando inversiones:', err);
        }
    }

    async updateTarget(value: number, pin: string) {
        this.targetSavings = value;
        await this.save(pin, { inv_target: value });
    }

    async addRule(pattern: string, alias: string, pin: string) {
        this.rules[pattern] = alias;
        await this.save(pin, { inv_rules: JSON.stringify(this.rules) });
    }

    async removeRule(pattern: string, pin: string) {
        delete this.rules[pattern];
        await this.save(pin, { inv_rules: JSON.stringify(this.rules) });
    }

    async updateColor(category: string, color: string, pin: string) {
        this.categoryColors[category] = color;
        await this.save(pin, { inv_colors: JSON.stringify(this.categoryColors) });
    }

    private async save(pin: string, payload: Record<string, any>) {
        if (!pin) return;
        try {
            await fetch(apiUrl('/accounts/me'), {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Kaira-PIN': pin
                },
                body: JSON.stringify(payload)
            });
        } catch (err) {
            console.error('Error guardando inversiones:', err);
        }
    }

    getShortName(fullName: string): string {
        const nameUpper = fullName.toUpperCase();
        for (const [key, alias] of Object.entries(this.rules)) {
            if (nameUpper.includes(key.toUpperCase())) {
                return alias;
            }
        }
        return fullName.length > 15 ? fullName.slice(0, 13) + '..' : fullName;
    }
}

export const investmentStore = new InvestmentStore();