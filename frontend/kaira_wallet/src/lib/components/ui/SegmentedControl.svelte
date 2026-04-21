<script lang="ts">
    interface Option {
        value: string;
        label: string;
    }

    let { 
        options, 
        selected = $bindable(), 
        useHaptics = true 
    } = $props<{
        options: Option[],
        selected: string,
        useHaptics?: boolean
    }>();

    const vibrate = () => {
        if (useHaptics && typeof navigator !== 'undefined' && navigator.vibrate) {
            navigator.vibrate(10);
        }
    };

    let activeIndex = $derived(options.findIndex(o => o.value === selected));
    let widthPercent = $derived(100 / options.length);
</script>

<section
    class="glass-panel relative flex gap-1 rounded-2xl border border-black/5 bg-black/5 p-1 dark:border-white/10 dark:bg-white/5"
>
    <div
        class="absolute top-1 bottom-1 left-1 rounded-xl bg-primary shadow-lg transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
        style="width: calc({widthPercent}% - 4px); transform: translateX({activeIndex * 100}%)"
    ></div>

    {#each options as option}
        <button
            onclick={() => {
                selected = option.value;
                vibrate();
            }}
            class="relative z-10 flex-1 cursor-pointer rounded-xl py-2.5 text-sm font-bold transition-all duration-500
            {selected === option.value 
                ? 'text-white opacity-100' 
                : 'text-current opacity-40 hover:opacity-60'}"
        >
            {option.label}
        </button>
    {/each}
</section>