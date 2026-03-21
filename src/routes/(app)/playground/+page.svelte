<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount, getContext } from 'svelte';
	import { WEBUI_NAME, user } from '$lib/stores';

	const i18n = getContext('i18n');

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
		}
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Playground')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if $user?.role === 'admin'}
	<div class="flex flex-col gap-4 p-4 max-w-4xl mx-auto">
		<div class="text-2xl font-semibold">{$i18n.t('Playground')}</div>

		<div class="grid gap-3 sm:grid-cols-2">
			<a
				href="/playground/completions"
				class="flex flex-col gap-2 p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-850 transition"
			>
				<div class="flex items-center gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0021 18V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v12a2.25 2.25 0 002.25 2.25z"
						/>
					</svg>
					<div class="font-semibold">{$i18n.t('Completions')}</div>
				</div>
				<div class="text-sm text-gray-500 dark:text-gray-400">
					{$i18n.t('Test text completions with any model')}
				</div>
			</a>

			<a
				href="/playground/images"
				class="flex flex-col gap-2 p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-850 transition"
			>
				<div class="flex items-center gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="m2.25 15.75 5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z"
						/>
					</svg>
					<div class="font-semibold">{$i18n.t('Images')}</div>
				</div>
				<div class="text-sm text-gray-500 dark:text-gray-400">
					{$i18n.t('Generate images with AI models')}
				</div>
			</a>
		</div>
	</div>
{/if}
