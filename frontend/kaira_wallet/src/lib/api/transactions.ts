import { apiUrl, KAIRA_PIN } from '$lib/config/api';

export type TransactionType =
	| 'expense'
	| 'income'
	| 'invest';

export type FrequencyType =
	| 'fixed'
	| 'variable';

export interface TransactionPayload {
	type: TransactionType;
	amount: number;
	description?: string;
	category_id: number;
	date: string;
	is_paid: boolean;
	frequency: FrequencyType;
	user_id?: number;
}

function headers() {
	return {
		'Content-Type': 'application/json',
		'X-Kaira-PIN': KAIRA_PIN
	};
}

function authHeaders() {
	return {
		'X-Kaira-PIN': KAIRA_PIN
	};
}


/* =========================
   GET ONE
========================= */

export async function getTransaction(
	id: number
) {
	const res = await fetch(
		apiUrl(`/transactions/${id}`),
		{
			headers: authHeaders()
		}
	);

	if (!res.ok) {
		throw new Error(
			'Error cargando transacción'
		);
	}

	return res.json();
}


/* =========================
   UPDATE
========================= */

export async function updateTransaction(
	id: number,
	payload: TransactionPayload
) {
	const res = await fetch(
		apiUrl(`/transactions/${id}`),
		{
			method: 'PUT',
			headers: headers(),
			body: JSON.stringify(payload)
		}
	);

	if (!res.ok) {
		throw new Error(
			'Error actualizando transacción'
		);
	}

	return res.json();
}


/* =========================
   DELETE
========================= */

export async function deleteTransaction(
	id: number
) {
	const res = await fetch(
		apiUrl(`/transactions/${id}`),
		{
			method: 'DELETE',
			headers: authHeaders()
		}
	);

	if (!res.ok) {
		throw new Error(
			'Error borrando transacción'
		);
	}

	return true;
}


/* =========================
   CREATE
(ya te vale para Add Transaction)
========================= */

export async function createTransaction(
	payload: TransactionPayload
) {
	const res = await fetch(
		apiUrl('/transactions'),
		{
			method: 'POST',
			headers: headers(),
			body: JSON.stringify(payload)
		}
	);

	if (!res.ok) {
		throw new Error(
			'Error creando transacción'
		);
	}

	return res.json();
}


