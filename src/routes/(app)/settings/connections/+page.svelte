<script lang="ts">
	import ConnectionsPreferences from '$lib/components/settings/ConnectionsPreferences.svelte';
	import { getContext } from 'svelte';
	import type { UserSettingsContext } from '$lib/types/user-settings';

	const { saveSettings } = getContext<UserSettingsContext>('user-settings');
</script>

<ConnectionsPreferences {saveSettings} />
