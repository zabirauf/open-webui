import { CODE_API_BASE_URL} from '$lib/constants';

export const runCode = async (token: string, code: string, language: string) => {
	const data = new FormData();
	data.append('code', code);
	data.append('language', language);

	let error = null;
	const res = await fetch(`${CODE_API_BASE_URL}/run`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		},
		body: data
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};
