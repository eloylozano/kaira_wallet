// src/lib/data/settings.data.ts

import { goto } from '$app/navigation';
import { auth } from '$lib/stores/auth';

export type SettingItem =
	| {
			type: 'action';
			label: string;
			btnText?: string;
			variant?: 'normal' | 'danger';
			action: () => void;
	  }
	| {
			type: 'toggle';
			label: string;
			value: () => boolean;
			set: (v: boolean) => void;
	  };

export type SettingsSection = {
	name: string;
	items: SettingItem[];
};

const haptic = () => {
	if (typeof navigator !== 'undefined' && navigator.vibrate) {
		navigator.vibrate(10);
	}
};

export const getSettingsSections = (
	useHaptics: boolean,
	setPinModal: (v: boolean) => void,
	setLockModal: (v: boolean) => void,
	setDeleteModal: (v: boolean) => void
): SettingsSection[] => [
	{
		name: 'Seguridad',
		items: [
			{
				label: 'PIN de acceso',
				type: 'action',
				btnText: 'Cambiar',
				action: () => {
					setPinModal(true);
					if (useHaptics) haptic();
				}
			},
			{
				label: 'Bloquear sesión',
				type: 'action',
				variant: 'danger',
				btnText: 'Bloquear',
				action: () => {
					setLockModal(true);
					if (useHaptics) haptic();
				}
			}
		]
	},
	{
		name: 'Datos',
		items: [
			{
				label: 'Configurar categorías',
				type: 'action',
				btnText: 'Configurar',
				action: () => {
					goto('/categories');
					if (useHaptics) haptic();
				}
			},
			{
				label: 'Exportar historial (CSV)',
				type: 'action',
				btnText: 'Exportar',
				action: () => {
					if (useHaptics) haptic();
				}
			},
			{
				label: 'Borrar todos los gastos',
				type: 'action',
				variant: 'danger',
				btnText: 'Borrar todo',
				action: () => {
					setDeleteModal(true);
					if (useHaptics) haptic();
				}
			}
		]
	}
];