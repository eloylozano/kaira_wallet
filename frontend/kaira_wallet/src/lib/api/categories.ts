import { PUBLIC_API_URL, PUBLIC_KAIRA_PIN } from '$env/static/public';

function headers() {
	return {
		'Content-Type': 'application/json',
		'X-Kaira-PIN': PUBLIC_KAIRA_PIN
	};
}

// 🟢 CREATE
export async function createCategory(data: any) {
	const res = await fetch(`${PUBLIC_API_URL}/categories/`, {
		method: 'POST',
		headers: headers(),
		body: JSON.stringify(data)
	});

	if (!res.ok) {
		throw new Error((await res.json()).detail);
	}

	return res.json();
}

// 🟡 UPDATE (PUT explícito)
export async function updateCategory(id: number, data: any) {
	const res = await fetch(`${PUBLIC_API_URL}/categories/${id}`, {
		method: 'PUT',
		headers: headers(),
		body: JSON.stringify(data)
	});

	if (!res.ok) {
		throw new Error((await res.json()).detail);
	}

	return res.json();
}

// 🔴 DELETE
export async function deleteCategory(id: number) {
	const res = await fetch(`${PUBLIC_API_URL}/categories/${id}`, {
		method: 'DELETE',
		headers: {
			'X-Kaira-PIN': PUBLIC_KAIRA_PIN
		}
	});

	if (!res.ok) {
		const err = await res.json();
		throw new Error(err.detail);
	}
}