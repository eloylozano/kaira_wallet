<script lang="ts">
	let { checked = $bindable(false), onchange } = $props();

	function toggle() {
		checked = !checked;
		if (onchange) onchange(checked);
	}
</script>

<label class="toggle-switch">
	<input type="checkbox" {checked} onchange={toggle} />
	<div class="toggle-switch-background">
		<div class="toggle-switch-handle"></div>
	</div>
</label>

<style>
	.toggle-switch {
		position: relative;
		display: inline-block;
		/* Tamaño reducido: Proporción clásica 2:1 aproximadamente */
		width: 44px; 
		height: 24px;
		cursor: pointer;
	}

	.toggle-switch input[type='checkbox'] {
		display: none;
	}

	.toggle-switch-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(255, 255, 255, 0.1); /* Estilo Glass */
		border-radius: 20px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.toggle-switch-handle {
		position: absolute;
		top: 2px;
		left: 2px;
		width: 18px;
		height: 18px;
		background-color: #fff;
		border-radius: 50%;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	/* Estado Activo (Checked) */
	input[type='checkbox']:checked + .toggle-switch-background {
		background-color: var(--primary, #6366f1);
		border-color: rgba(255, 255, 255, 0.2);
	}

	input[type='checkbox']:checked + .toggle-switch-background .toggle-switch-handle {
		transform: translateX(20px); /* Ajustado al nuevo ancho */
	}

	/* Pequeño feedback al pulsar */
	.toggle-switch:active .toggle-switch-handle {
		width: 22px; /* Efecto elástico */
	}
</style>