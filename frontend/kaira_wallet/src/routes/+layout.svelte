<script>
    import './layout.css';
    import TabBar from '$lib/components/layout/TabBar.svelte';
    // CAMBIO: Importamos 'auth' en lugar de 'isUnlocked'
    import { auth } from '$lib/stores/auth'; 
    import PinLock from '$lib/components/layout/PinLock.svelte';
</script>

<div class="app-container">
    {#if !$auth}
        <PinLock />
    {:else}
        <main class="content-wrapper">
            <slot />
        </main>

        <TabBar />
    {/if}
</div>
<style>
    .app-container {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        width: 100%;
        align-items: center;
    }

    .content-wrapper {
        width: 100%;
        /* En móvil es el 100%, en PC llega hasta 1200px */
        max-width: 1200px; 
        
        padding-left: 20px;
        padding-right: 20px;
        
        /* Ajuste de márgenes */
        padding-top: calc(20px + var(--safe-area-top));
        padding-bottom: calc(100px + var(--safe-area-bottom));
        
        flex: 1;
    }

    /* En pantallas grandes (PC), el TabBar puede ser lateral o más discreto */
    @media (min-width: 1024px) {
        .content-wrapper {
            padding-top: 40px;
            padding-bottom: 40px;
        }
    }
</style>