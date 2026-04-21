// lib/utils/haptics.ts
export const haptics = {
    light: () => {
        // Verificamos si el navegador soporta vibración
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(10); // Vibración corta de 10ms
        }
    },
    success: () => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(); // Doble pulsación suave
        }
    },
    error: () => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(); // Vibración más intensa
        }
    }
};