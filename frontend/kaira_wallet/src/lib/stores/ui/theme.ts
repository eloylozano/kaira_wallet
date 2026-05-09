import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const DEFAULT_THEME = 'dark';

// siempre prioriza usuario guardado,
// si no existe => dark
const initialTheme =
	browser
		? localStorage.getItem('theme') || DEFAULT_THEME
		: DEFAULT_THEME;

export const theme = writable(initialTheme);

if (browser) {
	theme.subscribe((value) => {
		document.documentElement.setAttribute(
			'data-theme',
			value
		);

		localStorage.setItem(
			'theme',
			value
		);
	});
}