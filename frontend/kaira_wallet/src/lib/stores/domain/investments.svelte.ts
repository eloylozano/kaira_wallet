// src/lib/stores/domain/investments.svelte.ts
import { browser } from '$app/environment';

export interface InvestmentRules {
    [key: string]: string;
}

class InvestmentStore {
    // Estado reactivo para las reglas y colores
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

    targetSavings = $state<number>(50000);
    constructor() {
        if (browser) {
            const savedRules = localStorage.getItem('inv_rules');
            const savedColors = localStorage.getItem('inv_colors');
            const savedTarget = localStorage.getItem('inv_target');
            if (savedTarget) this.targetSavings = Number(savedTarget);
            if (savedRules) this.rules = JSON.parse(savedRules);
            if (savedColors) this.categoryColors = JSON.parse(savedColors);
        }
    }

    addRule(pattern: string, alias: string) {
        this.rules[pattern] = alias;
        this.save();
    }

    removeRule(pattern: string) {
        delete this.rules[pattern];
        this.save();
    }

    updateColor(category: string, color: string) {
        this.categoryColors[category] = color;
        this.save();
    }

    updateTarget(value: number) {
        this.targetSavings = value;
        this.save();
    }

    private save() {
        if (browser) {
            localStorage.setItem('inv_rules', JSON.stringify(this.rules));
            localStorage.setItem('inv_colors', JSON.stringify(this.categoryColors));
            localStorage.setItem('inv_target', this.targetSavings.toString());
        }
    }

    // La función que usarás en tus componentes para limpiar nombres
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
