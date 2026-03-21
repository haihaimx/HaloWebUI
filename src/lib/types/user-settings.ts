export type UserSettingsContext = {
	saveSettings: (updated: any, options?: { refreshModels?: boolean }) => Promise<void>;
	getModels: () => Promise<any>;
};
