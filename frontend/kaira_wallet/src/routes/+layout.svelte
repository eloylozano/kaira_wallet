<script>
    import './layout.css';
    import TabBar from '$lib/components/layout/TabBar.svelte';
</script>

<div class="app-container">
    <main class="content-wrapper">
        <slot />
    </main>

    <TabBar />
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