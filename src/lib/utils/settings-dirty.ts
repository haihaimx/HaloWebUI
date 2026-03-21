export const cloneSettingsSnapshot = <T>(value: T): T => JSON.parse(JSON.stringify(value));

export const isSettingsSnapshotEqual = (a: unknown, b: unknown) =>
	JSON.stringify(a) === JSON.stringify(b);
