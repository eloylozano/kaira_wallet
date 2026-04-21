export const haptics = {
    // Una vibración muy suave (ideal para botones numéricos)
    light: () => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(10); // 10ms es casi imperceptible pero se siente "físico"
        }
    },
    // Una vibración doble (ideal para cuando algo sale mal/error)
    error: () => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(20);
            navigator.vibrate(0);
            navigator.vibrate(20);
        }
    },
    // Vibración de éxito (algo se guardó correctamente)
    success: () => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(30);
        }
    }
};