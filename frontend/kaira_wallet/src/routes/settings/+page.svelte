<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import GlassCard from '$lib/components/ui/GlassCard.svelte';
	import GlassToggle from '$lib/components/ui/GlassToggle.svelte';

	// Estados para los toggles
	let notifications = $state(true);
	let biometrics = $state(false);

	const themes = [
		{ id: 'dark', name: 'Dark Mode' },
		{ id: 'light', name: 'Light Mode' }
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

	<section class="glass-panel flex gap-2 rounded-3xl p-1.5">
		{#each themes as t}
			<button
				onclick={() => theme.set(t.id)}
				class="flex-1 cursor-pointer rounded-2xl py-3 text-sm font-bold transition-all duration-500
                {$theme === t.id
					? 'bg-primary text-white shadow-lg'
					: 'text-slate-500 hover:text-slate-400'}"
			>
				{t.name}
			</button>
		{/each}
	</section>

	<div class="space-y-8">
		{#each sections as section}
			<div class="flex flex-col gap-3">
				<p class="text-primary/70 px-4 text-[10px] font-black tracking-[0.3em] uppercase">
					{section.name}
				</p>
				<GlassCard class="overflow-hidden !rounded-[32px]">
					<div class="flex flex-col">
						{#each section.items as item, i}
							<div class="group flex items-center justify-between p-5 transition-all">
								<div class="flex items-center gap-4">
									<span class="font-bold opacity-80">{item.label}</span>
								</div>

								{#if item.type === 'toggle'}
									<GlassToggle checked={item.value()} onchange={item.set} />
								{:else}
									<button
										class="opacity-20 transition-all group-hover:translate-x-1 group-hover:opacity-100"
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
								<div
									class="via-primary/10 mx-4 h-[1px] bg-gradient-to-r from-transparent to-transparent"
								></div>
							{/if}
						{/each}
					</div>
				</GlassCard>
			</div>
		{/each}
	</div>

	<button class="active-tap group mt-4">
		<div
			class="flex items-center justify-center gap-3 rounded-[32px] border border-rose-500/20 bg-rose-500/5 py-5 transition-all group-hover:bg-rose-500/10"
		>
			<span class="text-xs font-black tracking-widest text-rose-500 uppercase">Cerrar Sesión</span>
		</div>
	</button>
</div>

<style>
	header {
		padding-top: calc(1rem + var(--safe-area-top));
	}
</style>
