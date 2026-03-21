<script lang="ts">
	import Models from '$lib/components/admin/Settings/Models.svelte';
	import { user } from '$lib/stores';
</script>

{#if $user?.role === 'admin'}
	<Models />
{/if}
