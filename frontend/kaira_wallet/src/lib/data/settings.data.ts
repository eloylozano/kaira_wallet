import { goto } from '$app/navigation';

export type SettingItem =
	| {
		type: 'action';
		label: string;
		btnText?: string;
		variant?: 'normal' | 'danger';
		action: () => void;
	}
	| {
		type: 'budget';
		label: string;
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

export function getSettingsSections(
	useHaptics: boolean,
	setPinModal: (v: boolean) => void,
	setLockModal: (v: boolean) => void,
	setDeleteModal: (v: boolean) => void
): SettingsSection[] {
	return [
		{
			name: 'Seguridad',
			items: [
				{
					type: 'action',
					label: 'PIN de acceso',
					btnText: 'Cambiar',
					action: () => {
						setPinModal(true);
						if (useHaptics) haptic();
					}
				},
				{
					type: 'action',
					label: 'Bloquear sesión',
					btnText: 'Bloquear',
					variant: 'danger',
					action: () => {
						setLockModal(true);
						if (useHaptics) haptic();
					}
				}
			]
		},

		{
			name: 'Finanzas',
			items: [
				{
					type: 'budget',
					label: 'Presupuesto mensual'
				},
				{
					type: 'action',
					label: 'Inversiones',
					btnText: 'Gestionar',
					action: () => goto('/settings/investment-rules')
				}
			]
		},
		{
			name: 'Datos',
			items: [
				{
					type: 'action',
					label: 'Configurar categorías',
					btnText: 'Configurar',
					action: () => {
						goto('/settings/categories');
						if (useHaptics) haptic();
					}
				},
				{
					type: 'action',
					label: 'Exportar historial (CSV)',
					btnText: 'Exportar',
					action: () => {
						if (useHaptics) haptic();
					}
				},
				{
					type: 'action',
					label: 'Borrar todos los gastos',
					btnText: 'Borrar todo',
					variant: 'danger',
					action: () => {
						setDeleteModal(true);
						if (useHaptics) haptic();
					}
				}
			]
		}
	];
}