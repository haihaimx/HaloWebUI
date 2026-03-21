const normalizeTextScale = (scale: unknown): number => {
	if (scale === null || scale === undefined || scale === '') {
		return 1;
	}

	const parsed = Number(scale);
	if (!Number.isFinite(parsed)) {
		return 1;
	}

	// Keep aligned with UI slider bounds in Interface settings.
	if (parsed < 1 || parsed > 1.5) {
		return 1;
	}

	return parsed;
};

export const setTextScale = (scale: unknown) => {
	if (typeof document === 'undefined') {
		return;
	}

	document.documentElement.style.setProperty('--app-text-scale', `${normalizeTextScale(scale)}`);
};
