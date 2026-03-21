<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import type { Writable } from 'svelte/store';

	import type { UserSettingsContext } from '$lib/types/user-settings';
	import Account from '$lib/components/chat/Settings/Account.svelte';

	const i18n: Writable<any> = getContext('i18n');
	const { saveSettings } = getContext<UserSettingsContext>('user-settings');
</script>

<Account
	{saveSettings}
	saveHandler={() => {
		toast.success($i18n.t('Settings saved successfully!'));
	}}
/>
