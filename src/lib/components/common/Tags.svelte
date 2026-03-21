<script lang="ts">
	import { tick, getContext, createEventDispatcher } from 'svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import Plus from '$lib/components/icons/Plus.svelte';
	const dispatch = createEventDispatcher();

	const i18n = getContext('i18n');

	export let tags = [];
	export let suggestionTags = [];
	export let placeholder = '';

	let editing = false;
	let inputValue = '';
	let inputElement: HTMLInputElement;

	const enterEdit = async () => {
		editing = true;
		await tick();
		inputElement?.focus();
	};

	const exitEdit = () => {
		if (inputValue.trim()) addTag();
		editing = false;
	};

	const addTag = () => {
		const value = inputValue.trim();
		if (value && !tags.some((t) => t.name === value)) {
			dispatch('add', value);
			inputValue = '';
		}
	};

	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Enter') {
			e.preventDefault();
			addTag();
		} else if (e.key === 'Escape') {
			exitEdit();
		} else if (e.key === 'Backspace' && !inputValue && tags.length > 0) {
			dispatch('delete', tags[tags.length - 1].name);
		}
	};
</script>

<div class="flex flex-wrap items-center gap-1.5 min-h-[30px] px-2 py-1.5 rounded-lg transition">
	{#if tags.length > 0}
		{#each tags as tag}
			<span
				class="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-200 rounded-md max-w-full"
			>
				<span class="truncate">{tag.name}</span>
				<button
					type="button"
					class="shrink-0 hover:text-red-500 transition"
					on:click|stopPropagation={() => dispatch('delete', tag.name)}
					aria-label={$i18n.t('Remove tag')}
				>
					<XMark className="size-3" strokeWidth="2.5" />
				</button>
			</span>
		{/each}
	{/if}

	{#if editing}
		<input
			bind:this={inputElement}
			bind:value={inputValue}
			class="flex-1 min-w-[60px] text-xs bg-transparent outline-none placeholder:text-gray-400"
			placeholder={placeholder || $i18n.t('Add Tags')}
			list="tagSuggestions"
			on:keydown={handleKeydown}
			on:blur={exitEdit}
		/>
		{#if suggestionTags.length > 0}
			<datalist id="tagSuggestions">
				{#each suggestionTags as tag}
					<option value={tag.name} />
				{/each}
			</datalist>
		{/if}
	{:else}
		<button
			type="button"
			class="inline-flex items-center gap-0.5 px-1.5 py-0.5 text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition"
			on:click|stopPropagation={enterEdit}
		>
			<Plus className="size-3" strokeWidth="2.5" />
		</button>
	{/if}
</div>
