<script>
	import { goto } from '$app/navigation';
	import { WEBUI_NAME, config } from '$lib/stores';
	import { onMount, getContext } from 'svelte';

	const i18n = getContext('i18n');

	let loaded = false;
	let checking = false;

	onMount(async () => {
		if ($config) {
			await goto('/');
		}

		loaded = true;
	});

	const handleRetry = async () => {
		checking = true;
		await new Promise((r) => setTimeout(r, 1000));
		location.href = '/';
	};
</script>

{#if loaded}
	<div class="absolute w-full h-full flex z-50 bg-gray-50 dark:bg-gray-900">
		<div class="m-auto flex flex-col items-center justify-center px-6 max-w-md">
			<!-- 图标 -->
			<div class="relative mb-6">
				<!-- 背景光晕 -->
				<div class="absolute inset-0 w-20 h-20 rounded-full bg-red-500/10 blur-xl"></div>

				<!-- 主图标 -->
				<div
					class="relative w-20 h-20 rounded-2xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center shadow-lg"
				>
					<svg
						class="w-10 h-10 text-white"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.5"
					>
						<rect x="3" y="3" width="18" height="8" rx="2" fill="currentColor" fill-opacity="0.2" />
						<circle cx="6.5" cy="7" r="1.5" fill="currentColor" />
						<path d="M10 7h7" stroke-linecap="round" />
						<rect
							x="3"
							y="13"
							width="18"
							height="8"
							rx="2"
							fill="currentColor"
							fill-opacity="0.2"
						/>
						<circle cx="6.5" cy="17" r="1.5" fill="currentColor" />
						<path d="M10 17h7" stroke-linecap="round" />
					</svg>

					<!-- X 标记 -->
					<div
						class="absolute -bottom-1.5 -right-1.5 w-7 h-7 rounded-full bg-white dark:bg-gray-800 flex items-center justify-center shadow-md border-2 border-white dark:border-gray-800"
					>
						<svg
							class="w-4 h-4 text-red-500"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="3"
							stroke-linecap="round"
						>
							<path d="M18 6L6 18M6 6l12 12" />
						</svg>
					</div>
				</div>
			</div>

			<!-- 标题 -->
			<h1 class="text-xl font-semibold text-gray-900 dark:text-white text-center mb-2">
				{$i18n.t('{{webUIName}} Backend Required', { webUIName: $WEBUI_NAME })}
			</h1>

			<!-- 描述 -->
			<p class="text-sm text-gray-500 dark:text-gray-400 text-center mb-6">
				{$i18n.t(
					"Oops! You're using an unsupported method (frontend only). Please serve the WebUI from the backend."
				)}
			</p>

			<!-- 提示 -->
			<div class="flex items-center gap-2 text-xs text-gray-400 dark:text-gray-500 mb-6">
				<svg
					class="w-4 h-4"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<circle cx="12" cy="12" r="10" />
					<path d="M12 16v-4" />
					<path d="M12 8h.01" />
				</svg>
				<span>{$i18n.t('Make sure the backend service is running and try again.')}</span>
			</div>

			<!-- 重试按钮 -->
			<button
				class="group flex items-center gap-2 px-6 py-2.5 rounded-lg font-medium text-sm
					   bg-gray-900 dark:bg-white text-white dark:text-gray-900
					   hover:bg-gray-800 dark:hover:bg-gray-100
					   transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]
					   disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
				on:click={handleRetry}
				disabled={checking}
			>
				{#if checking}
					<svg class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
						<circle
							cx="12"
							cy="12"
							r="10"
							stroke="currentColor"
							stroke-width="2.5"
							stroke-opacity="0.2"
						/>
						<path
							d="M12 2a10 10 0 0 1 10 10"
							stroke="currentColor"
							stroke-width="2.5"
							stroke-linecap="round"
						/>
					</svg>
					<span>{$i18n.t('Checking...')}</span>
				{:else}
					<svg
						class="w-4 h-4 transition-transform duration-300 group-hover:-rotate-45"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2.5"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path d="M23 4v6h-6" />
						<path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
					</svg>
					<span>{$i18n.t('Check Again')}</span>
				{/if}
			</button>
		</div>
	</div>
{/if}
