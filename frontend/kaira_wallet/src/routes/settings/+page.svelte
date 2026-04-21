<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import GlassCard from '$lib/components/ui/GlassCard.svelte';
	import GlassToggle from '$lib/components/ui/GlassToggle.svelte';

	// Estados para los toggles
	let notifications = $state(true);
	let biometrics = $state(false);

	const themes = [
		{ id: 'dark', name: 'Dark Mode' },
		{ id: 'light', name: 'Light Mode' },
		
	];

	const sections = [
		{
			name: 'Cuenta',
			items: [
				{ label: 'Perfil', type: 'link' },
				{ label: 'Seguridad', type: 'link' }
			]
		},
		{
			name: 'App',
			items: [
				{
					label: 'Notificaciones',
					type: 'toggle',
					value: () => notifications,
					set: (v: boolean) => (notifications = v)
				},
				{
					label: 'Face ID / Huella',
					type: 'toggle',
					value: () => biometrics,
					set: (v: boolean) => (biometrics = v)
				},
				{ label: 'Exportar Datos', type: 'link' }
			]
		}
	];
</script>

<div class="mx-auto flex w-full max-w-xl flex-col gap-8 px-4 py-10">
	<header class="mb-4">
		<h1 class="text-4xl font-bold tracking-tight uppercase">Settings</h1>
	</header>

	<section class="glass-panel relative flex gap-2 rounded-3xl p-1.5">
		<div
			class="absolute top-1.5 bottom-1.5 left-1.5 w-[calc(50%-6px)] rounded-2xl bg-primary shadow-lg transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
			style="transform: translateX({$theme === 'light' ? '100%' : '0%'})"
		></div>

		{#each themes as t}
			<button
				onclick={() => theme.set(t.id)}
				class="relative z-10 flex-1 cursor-pointer rounded-2xl py-3 text-sm font-bold transition-colors duration-500
            {$theme === t.id ? 'text-white' : 'opacity-50 hover:opacity-100'}"
			>
				{t.name}
			</button>
		{/each}
	</section>

	<div class="space-y-8">
		{#each sections as section}
			<div class="flex flex-col gap-3">
				<p class="px-4 text-[10px] font-black tracking-[0.3em] text-primary uppercase opacity-70">
					{section.name}
				</p>

				<GlassCard class="overflow-hidden !rounded-[32px]">
					<div class="flex flex-col">
						{#each section.items as item, i}
							<div class="group flex items-center justify-between p-5 transition-all">
								<div class="flex items-center gap-4">
									<span class="font-bold">{item.label}</span>
								</div>

								{#if item.type === 'toggle'}
									<GlassToggle checked={item.value()} onchange={item.set} />
								{:else}
									<button
										class="opacity-40 transition-all group-hover:translate-x-1 group-hover:opacity-100"
									>
										<svg
											viewBox="0 0 24 24"
											width="18"
											height="18"
											fill="none"
											stroke="currentColor"
											stroke-width="3"
										>
											<path d="m9 18 6-6-6-6" />
										</svg>
									</button>
								{/if}
							</div>

							{#if i < section.items.length - 1}
								<div class="mx-4 h-[1px] bg-current opacity-10"></div>
							{/if}
						{/each}
					</div>
				</GlassCard>
			</div>
		{/each}
	</div>
</div>

<style>
    header {
        padding-top: calc(1rem + var(--safe-area-top));
    }

    /* Animación suave para que las secciones aparezcan al cargar */
    .space-y-8 > div {
        animation: slideIn 0.6s ease forwards;
        opacity: 0;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Retraso progresivo para cada sección */
    .space-y-8 > div:nth-child(1) { animation-delay: 0.1s; }
    .space-y-8 > div:nth-child(2) { animation-delay: 0.2s; }
</style>