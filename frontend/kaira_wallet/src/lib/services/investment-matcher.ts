// src/lib/services/investment-matcher.ts

export function matchInvestment(description: string, rules: Record<string, string>) {
    const desc = description.toUpperCase();
    
    // Buscamos coincidencia en el diccionario de usuario
    for (const [pattern, alias] of Object.entries(rules)) {
        if (desc.includes(pattern.toUpperCase())) {
            return alias;
        }
    }
    return null;
}