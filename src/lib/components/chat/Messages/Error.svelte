<script lang="ts">
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';

	const i18n: Writable<any> = getContext('i18n');

	export let content: any = '';

	// ── Normalise any input into a consistent shape ──────────────
	interface ErrorData {
		type: string;
		title: string;
		reasons: string[];
		suggestion: string;
	}

	function parseError(raw: any): ErrorData {
		if (raw && typeof raw === 'object' && raw.type) {
			return {
				type: raw.type,
				title: raw.content ?? '',
				reasons: Array.isArray(raw.reasons) ? raw.reasons : [],
				suggestion: raw.suggestion ? `error.suggestion.${raw.suggestion}` : ''
			};
		}
		const text = typeof raw === 'string' ? raw : (raw?.content ?? JSON.stringify(raw));
		return { type: 'generic', title: text, reasons: [], suggestion: '' };
	}

	$: err = parseError(content);
	$: hasDetails = err.reasons.length > 0;

	let expanded = false;
</script>

<div
	class="my-2.5 flex rounded-lg border
	bg-red-50 dark:bg-red-950/20
	border-red-200 dark:border-red-800/30
	overflow-hidden"
>
	<!-- Left accent bar -->
	<div class="w-[3px] flex-shrink-0 bg-red-400 dark:bg-red-500" />

	<!-- Content area -->
	<div class="flex-1 px-3.5 py-3 min-w-0">
		<!-- Title row: icon + message -->
		<div class="flex items-start gap-2">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class="size-4 flex-shrink-0 mt-0.5 text-red-500 dark:text-red-400"
			>
				<path
					fill-rule="evenodd"
					d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"
					clip-rule="evenodd"
				/>
			</svg>
			<p
				class="text-sm leading-relaxed text-red-800 dark:text-red-200 break-words whitespace-pre-line"
			>
				{err.title}
			</p>
		</div>

		{#if hasDetails}
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="mt-2 flex items-center gap-1 cursor-pointer select-none group"
				on:click={() => (expanded = !expanded)}
			>
				<span
					class="text-[13px] text-red-500 dark:text-red-400/70
					group-hover:text-red-600 dark:group-hover:text-red-300
					transition-colors duration-150"
				>
					{$i18n.t('Possible causes')}
				</span>
				<div class="transition-transform duration-200" class:rotate-180={expanded}>
					<ChevronDown className="size-3 text-red-500 dark:text-red-400/70" strokeWidth="2.5" />
				</div>
			</div>

			{#if expanded}
				<div transition:slide={{ duration: 200, easing: quintOut, axis: 'y' }}>
					<ul class="mt-1.5 ml-0.5 space-y-1">
						{#each err.reasons as reason}
							<li class="flex items-center gap-1.5 text-[13px] text-red-600 dark:text-red-300">
								<span
									class="inline-block size-1 rounded-full bg-red-400 dark:bg-red-500 flex-shrink-0"
								/>
								{$i18n.t(`error.reason.${reason}`)}
							</li>
						{/each}
					</ul>
				</div>
			{/if}
		{/if}

		{#if err.suggestion}
			<p class="mt-2 text-[13px] text-red-600 dark:text-red-300">
				{$i18n.t(err.suggestion)}
			</p>
		{/if}
	</div>
</div>
