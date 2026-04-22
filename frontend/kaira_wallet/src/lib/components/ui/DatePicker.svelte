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

	<p class="kaira-soft px-2 text-[10px] font-black uppercase tracking-[0.2em]">
		{label}
	</p>

	<div
		class="
			kaira-panel
			flex items-center justify-between
			rounded-2xl px-3 sm:px-4 py-2 sm:py-3
			transition-all
			focus-within:border-primary/40
		"
	>

		<!-- FECHA -->
		<div class="flex flex-1 items-center justify-center gap-2 sm:gap-3">

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
				class="
					w-15 sm:w-15 lg:w-15
					bg-transparent text-center font-black
					text-xs sm:text-sm lg:text-base
					text-main placeholder:text-muted
					outline-none border-0 ring-0
				"
			/>

			<span class="text-muted font-black text-sm sm:text-base">-</span>

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
				class="
					w-15 sm:w-15 lg:w-15
					bg-transparent text-center font-black
					text-xs sm:text-sm lg:text-base
					text-main placeholder:text-muted
					outline-none border-0 ring-0
				"
			/>

			<span class="text-muted font-black text-sm sm:text-base">-</span>

			<input
				bind:this={yRef}
				bind:value={year}
				type="text"
				inputmode="numeric"
				maxlength="4"
				placeholder="AAAA"
				oninput={(e) => autoNext(e, 4)}
				onkeydown={(e) => backNav(e, yRef, mRef)}
				class="
					w-14 sm:w-20 lg:w-25
					bg-transparent text-center font-black
					text-xs sm:text-sm lg:text-xl
					text-main placeholder:text-muted
					outline-none border-0 ring-0
				"
			/>

		</div>

		<!-- CALENDARIO -->
		<button
			type="button"
			onclick={openCalendar}
			class="
				flex h-9 w-9 sm:h-10 sm:w-10 lg:h-11 lg:w-11
				items-center justify-center
				rounded-xl
				bg-primary/10 text-primary
				transition-all
				active:scale-95
				hover:bg-primary/20
			"
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
		<p class="kaira-soft px-2 text-xs">
			Fecha inválida
		</p>
	{/if}

</div>