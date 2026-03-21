import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getTerminalConfig = async (token: string) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/config`, {
		method: 'GET',
		headers: { authorization: `Bearer ${token}` }
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const updateTerminalConfig = async (token: string, enabled: boolean) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/config?enabled=${enabled}`, {
		method: 'POST',
		headers: { authorization: `Bearer ${token}` }
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const listDirectory = async (token: string, path: string = '') => {
	const params = path ? `?path=${encodeURIComponent(path)}` : '';
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/files${params}`, {
		method: 'GET',
		headers: { authorization: `Bearer ${token}` }
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const readFileContent = async (token: string, path: string) => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/terminal/files/content?path=${encodeURIComponent(path)}`,
		{
			method: 'GET',
			headers: { authorization: `Bearer ${token}` }
		}
	);
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const readFileBinary = async (token: string, path: string): Promise<ArrayBuffer> => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/terminal/files/binary?path=${encodeURIComponent(path)}`,
		{
			method: 'GET',
			headers: { authorization: `Bearer ${token}` }
		}
	);
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Failed to fetch binary file' }));
		throw err.detail;
	}
	return res.arrayBuffer();
};

export const writeFileContent = async (token: string, path: string, content: string) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/files/content`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ path, content })
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const createDirectory = async (token: string, path: string) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/files/mkdir`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ path })
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const deletePath = async (token: string, path: string) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/files?path=${encodeURIComponent(path)}`, {
		method: 'DELETE',
		headers: { authorization: `Bearer ${token}` }
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const renamePath = async (token: string, oldPath: string, newPath: string) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/files/rename`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ old_path: oldPath, new_path: newPath })
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const uploadFile = async (token: string, path: string, file: File) => {
	const formData = new FormData();
	formData.append('file', file);
	const params = path ? `?path=${encodeURIComponent(path)}` : '';
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/files/upload${params}`, {
		method: 'POST',
		headers: { authorization: `Bearer ${token}` },
		body: formData
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const getSqliteTables = async (token: string, path: string) => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/terminal/sqlite/tables?path=${encodeURIComponent(path)}`,
		{
			method: 'GET',
			headers: { authorization: `Bearer ${token}` }
		}
	);
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

export const executeSqlQuery = async (
	token: string,
	path: string,
	query: string,
	limit: number = 100
) => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/sqlite/query`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ path, query, limit })
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};

/**
 * Fetch a raw file as a Blob (for creating object URLs for media players).
 */
export const readFileRaw = async (token: string, path: string): Promise<Blob> => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/terminal/files/raw?path=${encodeURIComponent(path)}`,
		{
			method: 'GET',
			headers: { authorization: `Bearer ${token}` }
		}
	);
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Failed to fetch raw file' }));
		throw err.detail;
	}
	return res.blob();
};

export interface PortInfo {
	port: number;
	pid: number;
	process_name: string;
	address: string;
}

export const listPorts = async (token: string): Promise<PortInfo[]> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/terminal/ports`, {
		method: 'GET',
		headers: { authorization: `Bearer ${token}` }
	});
	if (!res.ok) throw (await res.json()).detail;
	return res.json();
};
