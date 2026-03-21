<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import type { Writable } from 'svelte/store';

	import Images from '$lib/components/admin/Settings/Images.svelte';
	import { user } from '$lib/stores';

	const i18n: Writable<any> = getContext('i18n');
</script>

{#if $user?.role === 'admin'}
	<Images
		on:save={() => {
			toast.success($i18n.t('Settings saved successfully!'));
		}}
	/>
{/if}
