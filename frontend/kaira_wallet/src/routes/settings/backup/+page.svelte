<script lang="ts">
    import { onMount } from 'svelte';
    import { Check, CircleAlert, CloudUpload, DatabaseBackup, Download, RefreshCw } from 'lucide-svelte';
    import GlassCard from '$lib/components/ui/core/GlassCard.svelte';
    import { apiUrl, KAIRA_PIN } from '$lib/config/api';
    import { settingsStore } from '$lib/stores/domain/settings.svelte';

    type BackupLog = {
        timestamp: string;
        file: string;
        balance: number | null;
    };

    const frequencies = [3, 5, 7];
    let frequency = $state(settingsStore.backupFrequency || 7);
    let logs = $state<BackupLog[]>([]);
    let isLoading = $state(true);
    let isSaving = $state(false);
    let isCreating = $state(false);
    let notice = $state<{ type: 'success' | 'error'; text: string } | null>(null);

    const euro = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' });
    const dateTime = new Intl.DateTimeFormat('es-ES', { dateStyle: 'medium', timeStyle: 'short' });

    async function loadLogs() {
        const response = await fetch(apiUrl('/backup/logs'), { headers: { 'X-Kaira-PIN': KAIRA_PIN } });
        if (!response.ok) throw new Error('No se ha podido cargar el registro.');
        logs = (await response.json()).sort(
            (a: BackupLog, b: BackupLog) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        );
    }

    onMount(async () => {
        try {
            const [configResponse] = await Promise.all([
                fetch(apiUrl('/backup'), { headers: { 'X-Kaira-PIN': KAIRA_PIN } }),
                loadLogs()
            ]);
            if (configResponse.ok) {
                const config = await configResponse.json();
                if (config.frequency_days) frequency = Number(config.frequency_days);
            }
        } catch {
            notice = { type: 'error', text: 'No se ha podido cargar toda la información de copias.' };
        } finally {
            isLoading = false;
        }
    });

    async function saveFrequency() {
        isSaving = true;
        notice = null;
        try {
            const response = await fetch(apiUrl('/backup'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Kaira-PIN': KAIRA_PIN },
                body: JSON.stringify({ frequency_days: frequency })
            });
            if (!response.ok) throw new Error();
            settingsStore.backupFrequency = frequency;
            if (typeof localStorage !== 'undefined') localStorage.setItem('backup_frequency_days', String(frequency));
            notice = { type: 'success', text: 'Frecuencia de copias actualizada.' };
        } catch {
            notice = { type: 'error', text: 'No se ha podido guardar la frecuencia.' };
        } finally {
            isSaving = false;
        }
    }

    async function createBackup() {
        isCreating = true;
        notice = null;
        try {
            const response = await fetch(apiUrl('/backup/run'), { method: 'POST', headers: { 'X-Kaira-PIN': KAIRA_PIN } });
            const result = await response.json();
            if (!response.ok || !result.ok) throw new Error(result.detail);
            await loadLogs();
            notice = { type: 'success', text: 'Copia de seguridad creada y añadida al registro.' };
        } catch {
            notice = { type: 'error', text: 'No se ha podido crear la copia. Inténtalo de nuevo.' };
        } finally {
            isCreating = false;
        }
    }

    async function downloadBackup(file: string) {
        try {
            const response = await fetch(`${apiUrl('/backup/download')}?file=${encodeURIComponent(file)}`, {
                headers: { 'X-Kaira-PIN': KAIRA_PIN }
            });
            if (!response.ok) throw new Error();
            const url = URL.createObjectURL(await response.blob());
            const link = document.createElement('a');
            link.href = url;
            link.download = file;
            link.click();
            URL.revokeObjectURL(url);
        } catch {
            notice = { type: 'error', text: 'No se ha podido descargar esta copia.' };
        }
    }
</script>

<div class="mx-auto max-w-xl space-y-6 py-6 md:px-0">
    <header class="space-y-2">
        <div class="flex items-center gap-3">
            <div class="grid h-11 w-11 place-items-center rounded-2xl border border-emerald-400/20 bg-emerald-400/10 text-emerald-400">
                <DatabaseBackup size={21} strokeWidth={2.2} />
            </div>
            <div>
                <p class="text-[10px] font-black tracking-[0.24em] text-emerald-400 uppercase">Protección de datos</p>
                <h1 class="text-3xl font-black tracking-tighter uppercase italic">Copias de seguridad</h1>
            </div>
        </div>
        <p class="max-w-md text-sm leading-6 text-[var(--text-muted)]">Guarda una instantánea de tus datos y consulta el balance que tenías en cada momento.</p>
    </header>

    {#if notice}
        <div class="flex items-center gap-2 rounded-2xl border px-4 py-3 text-xs font-bold {notice.type === 'success' ? 'border-emerald-400/20 bg-emerald-400/10 text-emerald-400' : 'border-rose-400/20 bg-rose-400/10 text-rose-400'}">
            {#if notice.type === 'success'}<Check size={16} />{:else}<CircleAlert size={16} />{/if}
            {notice.text}
        </div>
    {/if}

    <GlassCard class="overflow-hidden !rounded-[28px]">
        <div class="relative p-5">
            <div class="absolute -top-12 -right-8 h-32 w-32 rounded-full bg-emerald-400/10 blur-3xl"></div>
            <div class="relative flex flex-col gap-5">
                <div class="flex items-start justify-between gap-4">
                    <div>
                        <p class="text-sm font-black">Crear una copia ahora</p>
                        <p class="mt-1 text-xs leading-5 text-[var(--text-muted)]">Se guarda el estado actual y su balance neto.</p>
                    </div>
                    <span class="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-2.5 py-1 text-[9px] font-black tracking-wider text-emerald-400 uppercase">Manual</span>
                </div>
                <button onclick={createBackup} disabled={isCreating} class="backup-primary">
                    {#if isCreating}<RefreshCw class="animate-spin" size={16} />{:else}<CloudUpload size={16} />{/if}
                    {isCreating ? 'Creando copia…' : 'Hacer copia ahora'}
                </button>
            </div>
        </div>
    </GlassCard>

    <GlassCard class="!rounded-[28px] p-5">
        <div class="flex flex-col gap-4">
            <div>
                <p class="text-sm font-black">Copia automática</p>
                <p class="mt-1 text-xs leading-5 text-[var(--text-muted)]">Elige cada cuánto tiempo quieres proteger tus datos.</p>
            </div>
            <div class="grid grid-cols-3 gap-2 rounded-2xl bg-black/10 p-1.5">
                {#each frequencies as days}
                    <button onclick={() => (frequency = days)} class:frequency-active={frequency === days} class="frequency-option">
                        <strong>{days}</strong><span>días</span>
                    </button>
                {/each}
            </div>
            <button onclick={saveFrequency} disabled={isSaving} class="backup-secondary">
                {#if isSaving}<RefreshCw class="animate-spin" size={14} />{/if}
                {isSaving ? 'Guardando…' : 'Guardar frecuencia'}
            </button>
        </div>
    </GlassCard>

    <section class="space-y-3">
        <div class="flex items-end justify-between px-2">
            <div>
                <p class="text-[10px] font-black tracking-[0.22em] text-[var(--text-soft)] uppercase">Registro</p>
                <h2 class="mt-1 text-lg font-black">Historial de copias</h2>
            </div>
            {#if logs.length}<span class="text-xs font-bold text-[var(--text-muted)]">{logs.length} {logs.length === 1 ? 'copia' : 'copias'}</span>{/if}
        </div>

        {#if isLoading}
            <div class="py-10 text-center text-xs font-bold text-[var(--text-muted)]">Cargando registro…</div>
        {:else if logs.length}
            <div class="space-y-2">
                {#each logs as log (log.timestamp + log.file)}
                    <GlassCard class="!rounded-[22px] p-4">
                        <div class="flex items-center gap-3">
                            <div class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-emerald-400/10 text-emerald-400"><Check size={18} /></div>
                            <div class="min-w-0 flex-1">
                                <p class="text-sm font-black">Copia completada</p>
                                <p class="mt-0.5 truncate text-[11px] font-medium text-[var(--text-muted)]">{dateTime.format(new Date(log.timestamp))} · {log.file}</p>
                            </div>
                            <button onclick={() => downloadBackup(log.file)} class="download-button" aria-label="Descargar copia"><Download size={17} /></button>
                        </div>
                        <div class="mt-3 flex items-center justify-between rounded-xl bg-black/10 px-3 py-2.5">
                            <span class="text-[10px] font-black tracking-wider text-[var(--text-muted)] uppercase">Balance guardado</span>
                            <span class="text-sm font-black text-emerald-400">{log.balance === null ? 'No disponible' : euro.format(log.balance)}</span>
                        </div>
                    </GlassCard>
                {/each}
            </div>
        {:else}
            <GlassCard class="!rounded-[24px] p-8 text-center">
                <DatabaseBackup class="mx-auto text-[var(--text-soft)]" size={28} />
                <p class="mt-3 text-sm font-black">Aún no hay copias</p>
                <p class="mx-auto mt-1 max-w-xs text-xs leading-5 text-[var(--text-muted)]">Cuando crees la primera, aparecerá aquí con el balance de ese instante.</p>
            </GlassCard>
        {/if}
    </section>
</div>

<style>
    @reference "tailwindcss";

    .backup-primary, .backup-secondary, .frequency-option, .download-button { @apply inline-flex items-center justify-center transition-all active:scale-[0.98] disabled:pointer-events-none disabled:opacity-60; }
    .backup-primary { @apply w-full gap-2 rounded-2xl bg-emerald-500 px-4 py-3.5 text-[10px] font-black tracking-[0.16em] text-white uppercase shadow-[0_10px_24px_rgba(16,185,129,0.2)] hover:bg-emerald-400; }
    .backup-secondary { @apply w-full gap-2 rounded-xl border border-white/10 bg-white/5 py-3 text-[10px] font-black tracking-widest uppercase hover:bg-white/10; color: var(--text-main); }
    .frequency-option { @apply flex flex-col rounded-xl py-2 text-[var(--text-muted)] hover:bg-white/5; }
    .frequency-option strong { @apply text-base font-black leading-4; }
    .frequency-option span { @apply mt-1 text-[9px] font-black tracking-wider uppercase; }
    .frequency-active { @apply bg-emerald-500 text-white shadow-lg shadow-emerald-950/20 hover:bg-emerald-500; }
    .download-button { @apply h-10 w-10 shrink-0 rounded-xl border border-white/10 bg-white/5 text-[var(--text-muted)] hover:border-emerald-400/30 hover:bg-emerald-400/10 hover:text-emerald-400; }
    :global([data-theme='light']) .backup-secondary, :global([data-theme='light']) .download-button { @apply border-black/10 bg-black/[0.04]; }
    :global([data-theme='light']) .frequency-option { @apply hover:bg-black/[0.04]; }
    :global([data-theme='light']) .frequency-active { @apply bg-emerald-600 text-white; }
</style>
