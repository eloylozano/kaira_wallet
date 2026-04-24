export const iconGroups = {
	money: [
		'wallet',
		'credit-card',
		'piggy-bank',
		'banknote',
		'coins',
		'bitcoin',
		'receipt',
		'chart-line',
		'trending-up',
		'trending-down',
		'percent',
		'calculator',
		'landmark',
		'banknote-arrow-up',
		'banknote-arrow-down'
	],

	home: [
		'home',
		'key',
		'door-open',
		'sofa',
		'bed',
		'lamp',
		'building',
		'house',
		'lock',
		'unlock',
		'blinds'
	],

	food: [
		'coffee',
		'utensils',
		'shopping-bag',
		'pizza',
		'apple',
		'cake',
		'beer',
		'wine',
		'ice-cream',
		'cookie',
		'chef-hat'
	],

	work: [
		'briefcase',
		'laptop',
		'code',
		'building',
		'terminal',
		'file',
		'folder',
		'clipboard',
		'chart-bar',
		'globe'
	],

	transport: [
		'car',
		'bike',
		'motorbike',
		'bus',
		'train',
		'plane',
		'ship',
		'truck',
		'scooter',
		'car-taxi-front',
		'rocket'
	],

	life: [
		'heart',
		'activity',
		'brain',
		'stethoscope',
		'pill',
		'dumbbell',
		'leaf',
		'sun',
		'moon',
		'cloud',
		'smile',
        'wrench',
        'shirt',
        'trousers',
	],

	basics: [
		'circle',
		'square',
		'triangle',
		'star',
		'hexagon',
		'diamond',
		'plus',
		'minus',
		'x',
		'zap',
		'flame'
	]
} as const;

export type IconGroup = keyof typeof iconGroups;