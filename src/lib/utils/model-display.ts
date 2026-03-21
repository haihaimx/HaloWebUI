type AnyModel = {
	id?: string;
	name?: string;
	// snake_case from backend
	connection_name?: string;
	// camelCase from some frontend helpers (direct connections)
	connectionName?: string;
};

function escapeRegex(s: string): string {
	return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export function getModelConnectionName(model?: AnyModel | null): string | null {
	if (!model) return null;
	const raw = (model.connection_name ?? model.connectionName ?? '').toString().trim();
	return raw ? raw : null;
}

export function getModelBaseName(model?: AnyModel | null): string {
	if (!model) return '';

	const connectionName = getModelConnectionName(model);
	let name = (model.name ?? model.id ?? '').toString();

	if (connectionName) {
		// Strip a previously-appended connection suffix so "name" remains user-editable and clean.
		// Examples:
		// - "gpt-4o | Proxy A" -> "gpt-4o"
		// - "小艾|OpenAI" -> "小艾"
		const re = new RegExp(`\\s*\\|\\s*${escapeRegex(connectionName)}\\s*$`);
		name = name.replace(re, '').trim();
	}

	return name;
}

export function getModelChatDisplayName(model?: AnyModel | null): string {
	const base = getModelBaseName(model);
	const connectionName = getModelConnectionName(model);
	if (!connectionName) return base;
	if (!base) return connectionName;
	return `${base} | ${connectionName}`;
}
