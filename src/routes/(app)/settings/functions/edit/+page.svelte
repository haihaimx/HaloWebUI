<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	onMount(() => {
		const id = $page.url.searchParams.get('id');
		const target = id
			? `/workspace/functions/edit?id=${encodeURIComponent(id)}`
			: '/workspace/functions';
		goto(target, { replaceState: true });
	});
</script>
