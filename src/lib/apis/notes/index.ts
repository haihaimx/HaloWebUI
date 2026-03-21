import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getNotes = async (token: string = '') => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/notes/`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const getNoteById = async (token: string, noteId: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/notes/${noteId}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const createNewNote = async (token: string, note: object) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/notes/create`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ ...note })
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const updateNoteById = async (token: string, noteId: string, note: object) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/notes/${noteId}/update`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ ...note })
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const deleteNoteById = async (token: string, noteId: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/notes/${noteId}/delete`, {
		method: 'DELETE',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};
