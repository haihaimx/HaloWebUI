<script lang="ts">
	import { getContext } from 'svelte';

	import type { Writable } from 'svelte/store';
	import type { WorkspaceTabMeta } from './meta';

	const i18n: Writable<any> = getContext('i18n');

	export let activeTab: WorkspaceTabMeta | null = null;
	export let tabs: WorkspaceTabMeta[] = [];
	export let pathname = '';
</script>

{#if activeTab}
	<section class="glass-section p-5 space-y-5">
		<div class="flex flex-col gap-4">
			<div class="min-w-0">
				<div class="inline-flex h-8 items-center gap-2 whitespace-nowrap rounded-full border border-gray-200/80 bg-white/80 px-3.5 text-xs font-medium leading-none text-gray-600 dark:border-gray-700/80 dark:bg-gray-900/70 dark:text-gray-300">
					<span class="leading-none text-gray-400 dark:text-gray-500">{$i18n.t('Workspace')}</span>
					<span class="leading-none text-gray-300 dark:text-gray-600">/</span>
					<span class="leading-none text-gray-900 dark:text-white">{$i18n.t(activeTab.labelKey)}</span>
				</div>

				<div class="mt-3 flex items-start gap-3">
					<div class="glass-icon-badge shrink-0 {activeTab.badgeColor}">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-[18px] {activeTab.iconColor}">
							{#each activeTab.iconPaths as pathD}
								<path fill-rule="evenodd" d={pathD} clip-rule="evenodd" />
							{/each}
						</svg>
					</div>
					<div class="min-w-0 max-w-3xl">
						<div class="text-base font-semibold text-gray-800 dark:text-gray-100">
							{$i18n.t(activeTab.labelKey)}
						</div>
						<p class="mt-1 text-xs text-gray-400 dark:text-gray-500">
							{$i18n.t(activeTab.descKey)}
						</p>
					</div>
				</div>
			</div>

			<div class="flex w-full justify-end overflow-x-auto scrollbar-hidden">
				<div class="inline-flex min-w-max rounded-2xl bg-gray-100 p-1 dark:bg-gray-850">
					{#each tabs as tab (tab.key)}
						<a
							class={`flex shrink-0 items-center gap-2 rounded-xl px-4 py-2 text-sm font-medium transition-all ${
								tab.activeMatch.some((prefix) => pathname.startsWith(prefix))
									? 'bg-white text-gray-900 shadow-sm dark:bg-gray-800 dark:text-white'
									: 'text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200'
							}`}
							href={tab.href}
						>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-4">
								{#each tab.iconPaths as pathD}
									<path fill-rule="evenodd" d={pathD} clip-rule="evenodd" />
								{/each}
							</svg>
							<span>{$i18n.t(tab.labelKey)}</span>
						</a>
					{/each}
				</div>
			</div>
		</div>
	</section>
{/if}
