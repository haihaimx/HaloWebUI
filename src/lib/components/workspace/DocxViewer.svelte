<script lang="ts">
	import { onMount, onDestroy, getContext, createEventDispatcher } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';

	const i18n = getContext<Writable<i18nType>>('i18n');
	const dispatch = createEventDispatcher();

	// ── Props ──────────────────────────────────────────────
	export let data: ArrayBuffer;
	export let filePath: string = '';

	// ── State ──────────────────────────────────────────────
	let loading = true;
	let error = '';
	let htmlContent = '';
	let messages: string[] = [];
	let contentEl: HTMLDivElement;

	async function parseDocx() {
		loading = true;
		error = '';
		try {
			// Dependency: npm install mammoth
			// mammoth must be installed: npm install mammoth
			const mammoth = await import('mammoth');
			const result = await mammoth.convertToHtml(
				{ arrayBuffer: data },
				{
					// Convert embedded images to base64 inline
					convertImage: mammoth.images.imgElement(async (image: any) => {
						const buf = await image.read('base64');
						const mime = image.contentType || 'image/png';
						return { src: `data:${mime};base64,${buf}` };
					})
				}
			);
			htmlContent = result.value;
			messages = result.messages
				.filter((m: any) => m.type === 'warning')
				.map((m: any) => m.message);
		} catch (e: any) {
			error = e?.message || 'Failed to parse DOCX document';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		parseDocx();
	});
</script>

<!-- Header bar -->
<div
	class="flex items-center justify-between px-3 py-1.5 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 flex-shrink-0"
>
	<div class="flex items-center gap-2 min-w-0">
		<span class="text-blue-600 dark:text-blue-400 text-sm font-medium">DOCX</span>
		<span class="text-sm font-mono truncate text-gray-600 dark:text-gray-300">
			{filePath}
		</span>
		{#if messages.length > 0}
			<span class="text-xs text-amber-500" title={messages.join('\n')}>
				({messages.length}
				{$i18n.t('warnings')})
			</span>
		{/if}
	</div>
	<button
		class="px-2 py-1 text-xs rounded-lg text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
		on:click={() => dispatch('close')}
	>
		{$i18n.t('Close')}
	</button>
</div>

<!-- Content -->
{#if loading}
	<div class="flex items-center justify-center py-12 text-gray-400 flex-1">
		<svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
			/>
		</svg>
		{$i18n.t('Parsing document...')}
	</div>
{:else if error}
	<div class="flex items-center justify-center py-12 text-red-500 text-sm flex-1">
		{error}
	</div>
{:else}
	<div
		class="flex-1 overflow-auto bg-white dark:bg-gray-900 px-6 py-4 docx-viewer"
		bind:this={contentEl}
	>
		{@html htmlContent}
	</div>
{/if}

<style>
	/* Document styling that matches dark/light theme */
	.docx-viewer {
		font-family:
			'Segoe UI',
			-apple-system,
			BlinkMacSystemFont,
			sans-serif;
		font-size: 14px;
		line-height: 1.7;
		color: inherit;
	}

	/* Headings */
	.docx-viewer :global(h1) {
		font-size: 1.75em;
		font-weight: 700;
		margin: 1.2em 0 0.5em;
		border-bottom: 1px solid rgba(128, 128, 128, 0.2);
		padding-bottom: 0.3em;
	}
	.docx-viewer :global(h2) {
		font-size: 1.4em;
		font-weight: 600;
		margin: 1em 0 0.4em;
	}
	.docx-viewer :global(h3) {
		font-size: 1.15em;
		font-weight: 600;
		margin: 0.8em 0 0.3em;
	}
	.docx-viewer :global(h4),
	.docx-viewer :global(h5),
	.docx-viewer :global(h6) {
		font-size: 1em;
		font-weight: 600;
		margin: 0.6em 0 0.2em;
	}

	/* Paragraphs */
	.docx-viewer :global(p) {
		margin: 0.5em 0;
	}

	/* Lists */
	.docx-viewer :global(ul) {
		list-style: disc;
		padding-left: 1.5em;
		margin: 0.5em 0;
	}
	.docx-viewer :global(ol) {
		list-style: decimal;
		padding-left: 1.5em;
		margin: 0.5em 0;
	}
	.docx-viewer :global(li) {
		margin: 0.2em 0;
	}

	/* Tables */
	.docx-viewer :global(table) {
		border-collapse: collapse;
		width: 100%;
		margin: 0.8em 0;
		font-size: 0.9em;
	}
	.docx-viewer :global(th),
	.docx-viewer :global(td) {
		border: 1px solid rgba(128, 128, 128, 0.3);
		padding: 6px 10px;
		text-align: left;
	}
	.docx-viewer :global(th) {
		background: rgba(128, 128, 128, 0.1);
		font-weight: 600;
	}

	/* Images */
	.docx-viewer :global(img) {
		max-width: 100%;
		height: auto;
		margin: 0.5em 0;
		border-radius: 4px;
	}

	/* Strong / emphasis */
	.docx-viewer :global(strong) {
		font-weight: 700;
	}
	.docx-viewer :global(em) {
		font-style: italic;
	}

	/* Links */
	.docx-viewer :global(a) {
		color: #3b82f6;
		text-decoration: underline;
	}
	.docx-viewer :global(a:hover) {
		color: #2563eb;
	}
</style>
