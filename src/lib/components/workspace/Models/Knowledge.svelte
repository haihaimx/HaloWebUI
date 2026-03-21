<script lang="ts">
	import { getContext } from 'svelte';
	import Selector from './Knowledge/Selector.svelte';
	import FileItem from '$lib/components/common/FileItem.svelte';

	export let selectedKnowledge = [];
	export let collections = [];

	const i18n = getContext('i18n');
</script>

<div>
	<div class="text-sm font-medium mb-2">{$i18n.t('Knowledge')}</div>

	<div class="text-xs text-gray-500 dark:text-gray-400 mb-3">
		{$i18n.t('To attach knowledge base here, add them to the "Knowledge" workspace first.')}
	</div>

	{#if selectedKnowledge?.length > 0}
		<div class="flex flex-wrap items-center gap-2 mb-3">
			{#each selectedKnowledge as file, fileIdx}
				<FileItem
					{file}
					name={file.name}
					type={file?.legacy
						? `${$i18n.t('Legacy')}${file.type ? ` ${$i18n.t(file.type)}` : ''}`
						: $i18n.t(file?.type ?? 'Collection')}
					dismissible
					on:dismiss={(e) => {
						selectedKnowledge = selectedKnowledge.filter((_, idx) => idx !== fileIdx);
					}}
				/>
			{/each}
		</div>
	{/if}

	<div class="flex flex-wrap text-sm font-medium gap-1.5">
		<Selector
			on:select={(e) => {
				const item = e.detail;

				if (!selectedKnowledge.find((k) => k.id === item.id)) {
					selectedKnowledge = [
						...selectedKnowledge,
						{
							...item
						}
					];
				}
			}}
		>
			<button
				class="px-3.5 py-1.5 font-medium text-sm rounded-xl border border-gray-200/60 dark:border-gray-700/40 bg-gray-100/70 dark:bg-gray-800/60 hover:bg-gray-200/70 dark:hover:bg-gray-700/60 transition-colors"
				type="button">{$i18n.t('Select Knowledge')}</button
			>
		</Selector>
	</div>
</div>
