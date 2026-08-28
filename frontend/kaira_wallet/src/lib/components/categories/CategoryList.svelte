<script lang="ts">
	import { flip } from 'svelte/animate';
	import { cubicOut } from 'svelte/easing';
	import { fade } from 'svelte/transition';

	import CategoryItem from './CategoryItem.svelte';
	import type { Category } from '$lib/stores/domain/categories.svelte';

	let {
		items = [],
		onEdit,
		onReorder
	} = $props<{
		items: Category[];
		onEdit: (cat: Category) => void;
		onReorder: (parentId: number | null, reorderedIds: number[]) => void;
	}>();

	let draggedId = $state<number | null>(null);
	let overId = $state<number | null>(null);

	function handleDragStart(e: DragEvent, id: number) {
		draggedId = id;

		if (e.dataTransfer) {
			e.dataTransfer.effectAllowed = 'move';
			e.dataTransfer.setData('text/plain', String(id));
		}
	}

	function handleDragOver(e: DragEvent, id: number) {
		e.preventDefault();

		if (e.dataTransfer) {
			e.dataTransfer.dropEffect = 'move';
		}

		if (draggedId !== id) {
			overId = id;
		}

		// Auto-scroll cuando estás cerca de los bordes de la ventana
		const threshold = 80; // Píxeles desde el borde para activar el scroll
		const speed = 15; // Velocidad del desplazamiento

		if (e.clientY < threshold + 60) {
			window.scrollBy({ top: -speed, behavior: 'smooth' });
		} else if (e.clientY > window.innerHeight - threshold) {
			window.scrollBy({ top: speed, behavior: 'smooth' });
		}
	}

	function handleDragLeave(e: DragEvent) {
		const current = e.currentTarget as HTMLElement;
		const related = e.relatedTarget as Node | null;

		if (related && current?.contains(related)) return;

		overId = null;
	}

	function handleDrop(e: DragEvent, targetId: number, list: Category[], parentId: number | null) {
		e.preventDefault();

		overId = null;

		if (draggedId === null || draggedId === targetId) {
			draggedId = null;
			return;
		}

		const copy = [...list];

		const draggedIndex = copy.findIndex((c) => c.id === draggedId);
		const targetIndex = copy.findIndex((c) => c.id === targetId);

		if (draggedIndex === -1 || targetIndex === -1) {
			draggedId = null;
			return;
		}

		const [movedItem] = copy.splice(draggedIndex, 1);

		copy.splice(targetIndex, 0, movedItem);

		onReorder(
			parentId,
			copy.map((c) => c.id)
		);

		draggedId = null;
	}

	function handleDragEnd() {
		draggedId = null;
		overId = null;
	}
</script>

<div class="mb-22 space-y-3">
	{#each items as cat (cat.id)}
		<div
			animate:flip={{
				duration: 300,
				easing: cubicOut
			}}
		>
			<div class="relative">
				{#if overId === cat.id && draggedId !== cat.id}
					<div
						in:fade={{ duration: 120 }}
						out:fade={{ duration: 120 }}
						class="absolute -top-1 right-3 left-3 z-30"
					>
						<div
							class="h-[3px] rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.45)]"
						/>
					</div>
				{/if}

				<div
					draggable="true"
					ondragstart={(e) => handleDragStart(e, cat.id)}
					ondragover={(e) => handleDragOver(e, cat.id)}
					ondragleave={handleDragLeave}
					ondrop={(e) => handleDrop(e, cat.id, items, null)}
					ondragend={handleDragEnd}
					class="
					cursor-grab
					rounded-2xl
					transition-all
					duration-300
					ease-[cubic-bezier(.22,1,.36,1)]
					active:cursor-grabbing
				"
					class:dragging={draggedId === cat.id}
					class:drop-target={overId === cat.id && draggedId !== cat.id}
				>
					<CategoryItem {cat} {onEdit} />
				</div>
			</div>

			{#if cat.subcategories?.length}
				<div class="mt-2 ml-5 space-y-2 border-l border-white/10 pl-3">
					{#each cat.subcategories as sub (sub.id)}
						<div
							animate:flip={{
								duration: 300,
								easing: cubicOut
							}}
							class="relative"
						>
							{#if overId === sub.id && draggedId !== sub.id}
								<div
									in:fade={{ duration: 120 }}
									out:fade={{ duration: 120 }}
									class="absolute -top-1 right-3 left-3 z-30"
								>
									<div
										class="h-[3px] rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.45)]"
									/>
								</div>
							{/if}

							<div
								draggable="true"
								ondragstart={(e) => handleDragStart(e, sub.id)}
								ondragover={(e) => handleDragOver(e, sub.id)}
								ondragleave={handleDragLeave}
								ondrop={(e) => handleDrop(e, sub.id, cat.subcategories!, cat.id)}
								ondragend={handleDragEnd}
								class="
								cursor-grab
								rounded-2xl
								transition-all
								duration-300
								ease-[cubic-bezier(.22,1,.36,1)]
								active:cursor-grabbing
							"
								class:dragging={draggedId === sub.id}
								class:drop-target={overId === sub.id && draggedId !== sub.id}
							>
								<CategoryItem cat={sub} {onEdit} isChild={true} />
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	.dragging {
		opacity: 0.75;
		transform: scale(1.01);

		box-shadow:
			0 10px 25px rgb(0 0 0 / 0.15),
			0 20px 50px rgb(0 0 0 / 0.2);

		filter: brightness(1.03);
		z-index: 20;
	}

	.drop-target {
		border-radius: 1rem;

		box-shadow:
			0 0 0 1px rgb(16 185 129 / 0.2),
			0 8px 24px rgb(16 185 129 / 0.08);

		background: rgb(16 185 129 / 0.04);
	}
</style>
