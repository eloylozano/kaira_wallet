<script>
    import './layout.css';
    import TabBar from '$lib/components/layout/TabBar.svelte';
    import { auth } from '$lib/stores/auth'; 
    import PinLock from '$lib/components/layout/PinLock.svelte';

    // Estado para controlar el parpadeo de hidratación
    let isChecking = $state(true);

    // Este efecto solo se ejecuta en el cliente (navegador)
    $effect(() => {
        isChecking = false;
    });
</script>

<div class="app-container">
    {#if isChecking}
        <div class="loading-overlay"></div>
    {:else if !$auth}
        <PinLock />
    {:else}
        <main class="content-wrapper">
            <slot />
        </main>

        <TabBar />
    {/if}
</div>

<style>
    /* Estilos para el overlay de carga (opcional) */
    .loading-overlay {
        position: fixed;
        inset: 0;
        background-color: var(--bg-color, #000); /* Ajusta según tu tema */
        z-index: 9999;
    }

    .app-container {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        width: 100%;
        align-items: center;
    }

    .content-wrapper {
        width: 100%;
        max-width: 1200px; 
        
        padding-left: 20px;
        padding-right: 20px;
        
        padding-top: calc(20px + var(--safe-area-top));
        padding-bottom: calc(100px + var(--safe-area-bottom));
        
        flex: 1;
    }

    @media (min-width: 1024px) {
        .content-wrapper {
            padding-top: 40px;
            padding-bottom: 40px;
        }
    }
</style>