<script lang="ts">
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');
</script>

<div class="h-full flex flex-col justify-between text-sm">
	<div class="px-1.5 py-2">
		<div class="font-medium">{$i18n.t('Connections')}</div>
		<div class="mt-1 text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
			{$i18n.t('Manage your connections in Settings > Connections.')}
		</div>

		<div class="mt-3">
			<a
				href="/settings/connections"
				class="inline-flex items-center gap-2 px-3.5 py-2 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
			>
				<span>{$i18n.t('Settings')} &gt; {$i18n.t('Connections')}</span>
			</a>
		</div>
	</div>

	<!-- Keep spacing consistent with other chat settings panels -->
	<div class="h-10" />
</div>
