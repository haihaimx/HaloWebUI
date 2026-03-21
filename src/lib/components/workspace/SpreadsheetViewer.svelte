<script lang="ts">
	import { onMount, getContext, createEventDispatcher } from 'svelte';
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
	let sheetNames: string[] = [];
	let activeSheet = 0;
	let headers: string[] = [];
	let rows: string[][] = [];
	let totalRows = 0;

	// Tooltip for truncated cells
	let tooltipText = '';
	let tooltipX = 0;
	let tooltipY = 0;
	let showTooltip = false;

	const MAX_CELL_LENGTH = 64;
	const MAX_DISPLAY_ROWS = 2000;

	// Column letter helper: 0 -> A, 1 -> B, ..., 25 -> Z, 26 -> AA
	function colLabel(idx: number): string {
		let label = '';
		let n = idx;
		while (n >= 0) {
			label = String.fromCharCode(65 + (n % 26)) + label;
			n = Math.floor(n / 26) - 1;
		}
		return label;
	}

	function truncate(val: string): string {
		if (val.length <= MAX_CELL_LENGTH) return val;
		return val.slice(0, MAX_CELL_LENGTH) + '\u2026';
	}

	function handleCellHover(e: MouseEvent, val: string) {
		if (val.length > MAX_CELL_LENGTH) {
			tooltipText = val;
			tooltipX = e.clientX + 8;
			tooltipY = e.clientY + 8;
			showTooltip = true;
		}
	}

	function hideTooltip() {
		showTooltip = false;
	}

	async function parseSpreadsheet() {
		loading = true;
		error = '';
		try {
			// Dependency: npm install xlsx
			// SheetJS (xlsx) must be installed: npm install xlsx
			const XLSX = await import('xlsx');
			const workbook = XLSX.read(data, { type: 'array' });
			sheetNames = workbook.SheetNames;
			loadSheet(workbook, 0);
		} catch (e: any) {
			error = e?.message || 'Failed to parse spreadsheet';
		} finally {
			loading = false;
		}
	}

	function loadSheet(workbook: any, idx: number) {
		activeSheet = idx;
		const sheet = workbook.Sheets[workbook.SheetNames[idx]];

		// Dependency: xlsx library
		const XLSX = (window as any).__xlsx_cache;
		if (!XLSX) {
			// Fallback: re-import (shouldn't happen in practice)
			importAndLoad(idx);
			return;
		}

		const jsonRows: any[][] = XLSX.utils.sheet_to_json(sheet, {
			header: 1,
			defval: '',
			blankrows: false
		});

		totalRows = jsonRows.length;
		const displayRows = jsonRows.slice(0, MAX_DISPLAY_ROWS);

		// Determine max column count
		let maxCols = 0;
		for (const row of displayRows) {
			if (row.length > maxCols) maxCols = row.length;
		}

		headers = Array.from({ length: maxCols }, (_, i) => colLabel(i));
		rows = displayRows.map((row) => {
			const cells: string[] = [];
			for (let c = 0; c < maxCols; c++) {
				const val = row[c];
				cells.push(val == null ? '' : String(val));
			}
			return cells;
		});
	}

	async function importAndLoad(idx: number) {
		const XLSX = await import('xlsx');
		(window as any).__xlsx_cache = XLSX;
		const workbook = XLSX.read(data, { type: 'array' });
		loadSheet(workbook, idx);
	}

	async function switchSheet(idx: number) {
		if (idx === activeSheet) return;
		loading = true;
		try {
			const XLSX = await import('xlsx');
			(window as any).__xlsx_cache = XLSX;
			const workbook = XLSX.read(data, { type: 'array' });
			loadSheet(workbook, idx);
		} catch (e: any) {
			error = e?.message || 'Failed to switch sheet';
		} finally {
			loading = false;
		}
	}

	onMount(async () => {
		const XLSX = await import('xlsx');
		(window as any).__xlsx_cache = XLSX;
		await parseSpreadsheet();
	});
</script>

<!-- Header bar -->
<div
	class="flex items-center justify-between px-3 py-1.5 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 flex-shrink-0"
>
	<div class="flex items-center gap-2 min-w-0">
		<span class="text-green-600 dark:text-green-400 text-sm font-medium">XLSX</span>
		<span class="text-sm font-mono truncate text-gray-600 dark:text-gray-300">
			{filePath}
		</span>
		{#if totalRows > MAX_DISPLAY_ROWS}
			<span class="text-xs text-amber-500 ml-1">
				({$i18n.t('Showing {{count}} of {{total}} rows', {
					count: MAX_DISPLAY_ROWS,
					total: totalRows
				})})
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

<!-- Sheet tabs -->
{#if sheetNames.length > 1}
	<div
		class="flex items-center gap-0.5 px-3 py-1 bg-gray-50 dark:bg-gray-800/30 border-b border-gray-200 dark:border-gray-700 overflow-x-auto flex-shrink-0"
	>
		{#each sheetNames as name, idx}
			<button
				class="px-3 py-1 text-xs rounded-t-md transition whitespace-nowrap
					{idx === activeSheet
					? 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 border border-b-0 border-gray-200 dark:border-gray-600 font-medium'
					: 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700/50'}"
				on:click={() => switchSheet(idx)}
			>
				{name}
			</button>
		{/each}
	</div>
{/if}

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
		{$i18n.t('Parsing spreadsheet...')}
	</div>
{:else if error}
	<div class="flex items-center justify-center py-12 text-red-500 text-sm flex-1">
		{error}
	</div>
{:else}
	<div class="flex-1 overflow-auto relative">
		<table class="border-collapse text-xs font-mono">
			<!-- Fixed header -->
			<thead class="sticky top-0 z-10">
				<tr>
					<!-- Row number header -->
					<th
						class="px-2 py-1.5 text-center bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-gray-600 font-normal min-w-[3rem] sticky left-0 z-20"
					>
						#
					</th>
					{#each headers as h}
						<th
							class="px-3 py-1.5 text-center bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-600 font-semibold min-w-[4rem] whitespace-nowrap"
						>
							{h}
						</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each rows as row, rIdx}
					<tr
						class={rIdx % 2 === 0 ? 'bg-white dark:bg-gray-900' : 'bg-gray-50 dark:bg-gray-800/30'}
					>
						<!-- Row number -->
						<td
							class="px-2 py-1 text-center text-gray-400 dark:text-gray-500 border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50 sticky left-0 tabular-nums"
						>
							{rIdx + 1}
						</td>
						{#each row as cell}
							<td
								class="px-3 py-1 border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 max-w-[20rem] truncate whitespace-nowrap"
								title={cell.length > MAX_CELL_LENGTH ? cell : ''}
								on:mouseenter={(e) => handleCellHover(e, cell)}
								on:mouseleave={hideTooltip}
							>
								{truncate(cell)}
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

<!-- Tooltip for truncated cells -->
{#if showTooltip}
	<div
		class="fixed z-50 max-w-md p-2 text-xs bg-gray-900 text-white rounded-lg shadow-lg pointer-events-none break-words"
		style="left: {tooltipX}px; top: {tooltipY}px;"
	>
		{tooltipText}
	</div>
{/if}
