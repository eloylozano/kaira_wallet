<script lang="ts">
    import { onMount } from 'svelte';
    import flatpickr from 'flatpickr';
    import 'flatpickr/dist/flatpickr.css';
    import 'flatpickr/dist/themes/dark.css';

    let { value = $bindable(''), label = 'Fecha' } = $props<{
        value: string;
        label?: string;
    }>();

    let day = $state('');
    let month = $state('');
    let year = $state('');

    let dateInput: HTMLInputElement;
    let calendarBtn: HTMLButtonElement;
    let dRef: HTMLInputElement;
    let mRef: HTMLInputElement;
    let yRef: HTMLInputElement;

    let isMobile = $state(false);

    function todayISO() {
        const now = new Date();
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const d = String(now.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    function loadFromValue(v: string) {
        if (!v?.includes('-')) return;
        const [y, m, d] = v.split('-');
        year = y;
        month = m;
        day = d;
    }

    // Inicialización y sincronización
    $effect(() => {
        if (!value) value = todayISO();
        loadFromValue(value);
    });

    function validDate() {
        if (day.length !== 2 || month.length !== 2 || year.length !== 4) return false;
        const yy = Number(year), mm = Number(month), dd = Number(day);
        if (mm < 1 || mm > 12) return false;
        const max = new Date(yy, mm, 0).getDate();
        return dd >= 1 && dd <= max;
    }

    $effect(() => {
        if (validDate()) {
            const iso = `${year}-${month}-${day}`;
            if (value !== iso) value = iso;
        }
    });

    onMount(() => {
        isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

        if (!isMobile) {
            // Configuración de Flatpickr para Escritorio
            flatpickr(calendarBtn, {
                defaultDate: value,
                disableMobile: true,
                dateFormat: 'Y-m-d',
                onChange: (selectedDates, dateStr) => {
                    value = dateStr;
                }
            });
        }
    });

    function handleCalendarClick() {
        if (isMobile && dateInput) {
            // En móvil usamos el showPicker nativo que es superior
            const input = dateInput as HTMLInputElement & { showPicker?: () => void };
            if (input.showPicker) {
                input.showPicker();
            } else {
                input.click();
            }
        }
        // En PC, flatpickr se encarga solo gracias al onMount
    }

    // Helpers de teclado y formato
    function numericOnly(e: Event) {
        const t = e.target as HTMLInputElement;
        t.value = t.value.replace(/\D/g, '');
    }

    function autoNext(e: Event, max: number, next?: HTMLInputElement) {
        numericOnly(e);
        const t = e.target as HTMLInputElement;
        if (t.value.length >= max && next) next.focus();
    }

    function backNav(e: KeyboardEvent, current: HTMLInputElement, prev?: HTMLInputElement) {
        if (e.key === 'Backspace' && !current.value && prev) prev.focus();
    }

    function pad(which: 'day' | 'month') {
        if (which === 'day' && day.length === 1) day = `0${day}`;
        if (which === 'month' && month.length === 1) month = `0${month}`;
    }
</script>

<div class="space-y-3">
    <p class="kaira-soft px-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
        {label}
    </p>

    <div class="kaira-panel flex items-center justify-between rounded-2xl px-3 py-2 transition-all focus-within:border-primary/40 sm:px-4 sm:py-3">
        
        <div class="flex flex-1 items-center justify-center gap-2 sm:gap-3">
            <input
                bind:this={dRef}
                bind:value={day}
                type="text"
                inputmode="numeric"
                maxlength="2"
                placeholder="DD"
                oninput={(e) => autoNext(e, 2, mRef)}
                onkeydown={(e) => backNav(e, dRef)}
                onblur={() => pad('day')}
                class="w-12 border-0 bg-transparent text-center text-sm font-black text-white ring-0 outline-none placeholder:opacity-20 sm:w-12 sm:text-base"
            />

            <span class="opacity-20">-</span>

            <input
                bind:this={mRef}
                bind:value={month}
                type="text"
                inputmode="numeric"
                maxlength="2"
                placeholder="MM"
                oninput={(e) => autoNext(e, 2, yRef)}
                onkeydown={(e) => backNav(e, mRef, dRef)}
                onblur={() => pad('month')}
                class="w-12 border-0 bg-transparent text-center text-sm font-black text-white ring-0 outline-none placeholder:opacity-20 sm:w-12 sm:text-base"
            />

            <span class="opacity-20">-</span>

            <input
                bind:this={yRef}
                bind:value={year}
                type="text"
                inputmode="numeric"
                maxlength="4"
                placeholder="AAAA"
                oninput={(e) => autoNext(e, 4)}
                onkeydown={(e) => backNav(e, yRef, mRef)}
                class="w-16 border-0 bg-transparent text-center text-sm font-black text-white ring-0 outline-none placeholder:opacity-20 sm:w-20 sm:text-base"
            />
        </div>

        <button
            bind:this={calendarBtn}
            type="button"
            onclick={handleCalendarClick}
            class="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5 text-lg transition-all active:scale-90 hover:bg-white/10"
        >
            📅
        </button>

        <input
            bind:this={dateInput}
            type="date"
            bind:value
            class="invisible absolute h-0 w-0"
        />
    </div>

    {#if (day || month || year) && !validDate()}
        <p class="px-2 text-[10px] font-bold text-red-400/80 uppercase">Fecha inválida</p>
    {/if}
</div>

<style>
    /* Estilos para que flatpickr encaje con Kaira */
    :global(.flatpickr-calendar) {
        background: #171717 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.5) !important;
        border-radius: 1.5rem !important;
        font-family: inherit;
    }
    :global(.flatpickr-day.selected) {
        background: #10b981 !important; /* Tu verde esmeralda */
        border-color: #10b981 !important;
    }
</style>
