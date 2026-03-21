<script>
	import { onMount } from 'svelte';
	import { models } from '$lib/stores';
	import { ensureModels } from '$lib/services/models';
	import Models from '$lib/components/workspace/Models.svelte';

	onMount(async () => {
		await ensureModels(localStorage.token, { reason: 'workspace-models' });
	});
</script>

{#if $models !== null}
	<Models />
{/if}
