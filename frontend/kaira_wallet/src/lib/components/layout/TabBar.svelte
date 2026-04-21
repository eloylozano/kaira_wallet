<script>
  import { page } from '$app/stores';

  // Función rápida para vibrar al tocar el botón principal
  const playHaptic = () => {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      navigator.vibrate(15);
    }
  };

  const icons = {
    home: `<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>`,
    transactions: `<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>`,
    stats: `<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>`,
    settings: `<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>`
  };

  const navItems = [
    { name: 'Inicio', path: '/', icon: icons.home },
    { name: 'Historial', path: '/transactions', icon: icons.transactions },
    { name: 'spacer', path: '/transactions/new' }, 
    { name: 'Stats', path: '/stats', icon: icons.stats },
    { name: 'Ajustes', path: '/settings', icon: icons.settings }
  ];

  let activePath = $derived($page.url.pathname);
</script>

<nav class="glass-nav fixed-bottom">
  <div class="nav-container">
    {#each navItems as item}
      {#if item.name === 'spacer'}
        <div class="spacer"></div>
      {:else}
        <a href={item.path} class="nav-item {activePath === item.path ? 'active' : ''}">
          <div class="icon-wrapper">
            <svg 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              stroke-width={activePath === item.path ? "2.5" : "2"} 
              stroke-linecap="round" 
              stroke-linejoin="round"
            >
              {@html item.icon}
            </svg>
            {#if activePath === item.path}
              <div class="glow-dot"></div>
            {/if}
          </div>
          <span class="nav-label">{item.name}</span>
        </a>
      {/if}
    {/each}

    <a 
      href="/transactions/new" 
      class="fab-button active-tap" 
      onclick={playHaptic}
      aria-label="Nueva transacción"
    >
        <div class="fab-inner">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
        </div>
    </a>
  </div>
</nav>
<style>
  .fixed-bottom {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: calc(60px + var(--safe-area-bottom));
    padding-bottom: var(--safe-area-bottom);
    z-index: 1000;
    display: flex;
    align-items: center;
    border-top: 1px solid var(--glass-border);
  }

  .nav-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    position: relative;
    height: 100%;
  }

  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: var(--text-muted);
    transition: all 0.3s ease;
    flex: 1;
  }

  .nav-item.active {
    color: var(--primary);
  }

  .icon-wrapper {
    position: relative;
    padding: 4px;
  }

  .icon-wrapper svg {
    width: 22px;
    height: 22px;
  }

  .nav-label {
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 2px;
  }

  .glow-dot {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 5px;
    height: 5px;
    background: var(--primary);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--primary);
  }

  .spacer {
    width: 60px;
  }

  .fab-button {
    position: absolute;
    left: 50%;
    top: -20px;
    transform: translateX(-50%);
    width: 56px;
    height: 56px;
    background: rgba(16, 185, 129, 0.2); /* Fondo suave verde */
    border-radius: 20px;
    padding: 6px;
    border: none;
    cursor: pointer;
    backdrop-filter: blur(10px);
  }

  .fab-inner {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 15px var(--primary-glow);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .active-tap:active {
    transform: translateX(-50%) scale(0.92);
  }
</style>