<script lang="ts">
	let { value = $bindable(), label = 'Fecha' } = $props();

	let day = $state('');
	let month = $state('');
	let year = $state('');

	let dateInput: HTMLInputElement;
	let dRef: HTMLInputElement;
	let mRef: HTMLInputElement;
	let yRef: HTMLInputElement;

	function todayISO() {
		const now = new Date();

		const y = now.getFullYear();
		const m = String(now.getMonth() + 1).padStart(2, '0');
		const d = String(now.getDate()).padStart(2, '0');

		return `${y}-${m}-${d}`;
	}

	function loadFromValue(v: string) {
		if (!v?.includes('-')) return;
		const [y, m, d] = v.split('-');
		year = y;
		month = m;
		day = d;
	}

	// 👉 inicialización segura
	$effect(() => {
		if (!value) {
			value = todayISO();
		}
		loadFromValue(value);
	});

	function validDate() {
		if (day.length !== 2 || month.length !== 2 || year.length !== 4) return false;

		const yy = Number(year);
		const mm = Number(month);
		const dd = Number(day);

		if (mm < 1 || mm > 12) return false;

		const max = new Date(yy, mm, 0).getDate();
		return dd >= 1 && dd <= max;
	}

	$effect(() => {
		if (validDate()) {
			const iso = `${year}-${month}-${day}`;
			if (value !== iso) {
				value = iso;
			}
		}
	});

	$effect(() => {
		loadFromValue(value);
	});

	function numericOnly(e: Event) {
		const t = e.target as HTMLInputElement;
		t.value = t.value.replace(/\D/g, '');
	}

	function autoNext(e: Event, max: number, next?: HTMLInputElement) {
		numericOnly(e);
		const t = e.target as HTMLInputElement;

		if (t.value.length >= max && next) {
			next.focus();
		}
	}

	function backNav(e: KeyboardEvent, current: HTMLInputElement, prev?: HTMLInputElement) {
		if (e.key === 'Backspace' && !current.value && prev) {
			prev.focus();
		}
	}

	function pad(which: 'day' | 'month') {
		if (which === 'day' && day.length === 1) day = `0${day}`;
		if (which === 'month' && month.length === 1) month = `0${month}`;
	}

	function openCalendar() {
		if (!dateInput) return;

		try {
			dateInput.focus();
			dateInput.click();
		} catch {
			// ignore
		}
	}
</script>

<div class="space-y-3">
	<p class="px-2 text-[10px] font-black tracking-[0.2em] uppercase opacity-40">
		{label}
	</p>

	<div
		class="flex items-center rounded-2xl border border-white/6 bg-white/5 px-4 py-3 transition-all focus-within:border-primary/40"
	>
		<!-- bloque fecha centrado -->
		<div class="flex flex-1 items-center justify-center gap-3">
			<input
				bind:this={dRef}
				bind:value={day}
				type="text"
				inputmode="numeric"
				maxlength="2"
				placeholder="DD"
				oninput={(e) => autoNext(e, 2, mRef)}
				onkeydown={(e) => backNav(e, dRef)}
				onblur={() => pad('day')}
				class="w-10 appearance-none border-0 bg-transparent p-0 text-center font-extrabold ring-0 outline-none placeholder:text-white/20 md:text-xl"
			/>

			<span class="text-sm font-black opacity-20">-</span>

			<input
				bind:this={mRef}
				bind:value={month}
				type="text"
				inputmode="numeric"
				maxlength="2"
				placeholder="MM"
				oninput={(e) => autoNext(e, 2, yRef)}
				onkeydown={(e) => backNav(e, mRef, dRef)}
				onblur={() => pad('month')}
				class="w-10 appearance-none border-0 bg-transparent p-0 text-center font-extrabold ring-0 outline-none placeholder:text-white/20 md:text-xl"
			/>

			<span class="text-sm font-black opacity-20">-</span>

			<input
				bind:this={yRef}
				bind:value={year}
				type="text"
				inputmode="numeric"
				maxlength="4"
				placeholder="AAAA"
				oninput={(e) => autoNext(e, 4)}
				onkeydown={(e) => backNav(e, yRef, mRef)}
				class="w-16 appearance-none border-0 bg-transparent p-0 text-center font-extrabold ring-0 outline-none placeholder:text-white/20 md:text-xl"
			/>
		</div>

		<!-- botón calendario -->
		<button
			type="button"
			onclick={openCalendar}
			class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-white/6 text-lg transition-all hover:bg-white/10 active:scale-95"
		>
			📅
		</button>

		<input
			bind:this={dateInput}
			type="date"
			bind:value
			class="pointer-events-none absolute h-1 w-1 opacity-0"
		/>
	</div>

	{#if (day || month || year) && !validDate()}
		<p class="px-2 text-xs opacity-60">Fecha inválida</p>
	{/if}
</div>
