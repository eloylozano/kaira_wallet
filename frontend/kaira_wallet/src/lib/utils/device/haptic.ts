export const haptics = {
	enabled: true,

	init(state: boolean) {
		this.enabled = state;
	},

	vibrate(ms: number | number[]) {
		if (!this.enabled) return;
		if (typeof navigator === 'undefined') return;

		// iOS only allows simple patterns
		if ('vibrate' in navigator) {
			navigator.vibrate(ms);
		}
	},

	light() {
		this.vibrate(10);
	},

	success() {
		this.vibrate(20);
	},

	error() {
		this.vibrate(50);
	},

	tap() {
		this.vibrate(5);
	}
};