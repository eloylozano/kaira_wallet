<script lang="ts">
	interface Props {
		children?: import('svelte').Snippet;
		class?: string;
		onclick?: () => void;
	}

	let { children, class: className = '', onclick }: Props = $props();
</script>

<div 
    class="glass-panel overflow-hidden transition-all duration-200 {className}"
    onclick={onclick}
    role={onclick ? "button" : "presentation"}
    tabindex={onclick ? 0 : -1}
>
	{@render children?.()}
</div>

<style>
	.glass-panel {
		/* El sombreado sutil ayuda a separar el cristal del fondo oscuro */
		box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
		
		/* Aseguramos que el contenido no se salga de los bordes redondeados */
		position: relative;
	}

    /* Si la tarjeta es clickeable, añadimos un feedback visual */
	div[role="button"]:active {
		transform: scale(0.98);
		background: rgba(255, 255, 255, 0.12);
	}
</style>