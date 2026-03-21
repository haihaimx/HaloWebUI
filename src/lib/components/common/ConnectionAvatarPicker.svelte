<script lang="ts">
	/**
	 * 连接头像选择器
	 * 支持：首字母默认 / 内置图标库 / 用户上传
	 */
	import { createEventDispatcher, getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';

	import {
		CONNECTION_AVATAR_FILES,
		DARK_MODE_INVERT_CONN_AVATARS
	} from '$lib/utils/connection-avatars.manifest';
	import LetterAvatar from '$lib/components/common/LetterAvatar.svelte';

	const i18n = getContext('i18n') as Writable<i18nType>;
	const dispatch = createEventDispatcher<{ change: string }>();

	export let icon: string = '';
	export let name: string = '';
	export let size: string = 'size-9';

	const AVATAR_BASE = '/static/connection-avatars';

	/** Check if an icon path is a monochrome connection avatar that needs dark-mode inversion. */
	const shouldInvert = (src: string): boolean => {
		if (!src || src.startsWith('data:')) return false;
		const filename = src.split('/').at(-1) ?? '';
		return DARK_MODE_INVERT_CONN_AVATARS.has(filename);
	};

	let showMenu = false;
	let showGallery = false;
	let fileInput: HTMLInputElement;

	const handleUpload = (event: Event) => {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;

		const reader = new FileReader();
		reader.onload = (e) => {
			const img = new Image();
			img.onload = () => {
				const canvas = document.createElement('canvas');
				const ctx = canvas.getContext('2d')!;
				const s = 250;
				canvas.width = s;
				canvas.height = s;

				// Center-crop resize
				const ratio = img.width / img.height;
				let w: number, h: number;
				if (ratio > 1) {
					w = s * ratio;
					h = s;
				} else {
					w = s;
					h = s / ratio;
				}
				ctx.drawImage(img, (s - w) / 2, (s - h) / 2, w, h);
				const dataUrl = canvas.toDataURL('image/webp', 0.85) || canvas.toDataURL('image/jpeg');
				dispatch('change', dataUrl);
				showMenu = false;
			};
			img.src = e.target?.result as string;
		};
		reader.readAsDataURL(file);
		input.value = '';
	};

	const selectBuiltIn = (filename: string) => {
		dispatch('change', `${AVATAR_BASE}/${filename}`);
		showGallery = false;
		showMenu = false;
	};

	const resetAvatar = () => {
		dispatch('change', '');
		showMenu = false;
	};

	const handleClickOutside = (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		if (!target.closest('.avatar-picker-root')) {
			showMenu = false;
			showGallery = false;
		}
	};
</script>

<svelte:window on:mousedown={handleClickOutside} />

<div class="relative avatar-picker-root">
	<!-- Avatar display (clickable) -->
	<button
		type="button"
		class="relative group cursor-pointer rounded-xl {size} overflow-hidden"
		on:click|stopPropagation={() => {
			showMenu = !showMenu;
			showGallery = false;
		}}
		title={$i18n.t('Change avatar')}
	>
		{#if icon}
			<img
				src={icon}
				alt="avatar"
				class="w-full h-full object-cover rounded-xl"
				class:avatar-invert={shouldInvert(icon)}
			/>
		{:else}
			<LetterAvatar {name} {size} />
		{/if}
		<!-- Hover overlay -->
		<div
			class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity rounded-xl flex items-center justify-center"
		>
			<svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
				/>
			</svg>
		</div>
	</button>

	<!-- Dropdown menu -->
	{#if showMenu && !showGallery}
		<div
			class="absolute top-full left-0 mt-1 z-50 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg py-1 min-w-[140px]"
		>
			<button
				type="button"
				class="w-full px-3 py-1.5 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-800 transition text-gray-700 dark:text-gray-300"
				on:click|stopPropagation={() => fileInput.click()}
			>
				{$i18n.t('Upload Image')}
			</button>
			{#if CONNECTION_AVATAR_FILES.length > 0}
				<button
					type="button"
					class="w-full px-3 py-1.5 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-800 transition text-gray-700 dark:text-gray-300"
					on:click|stopPropagation={() => {
						showGallery = true;
					}}
				>
					{$i18n.t('Built-in Avatars')}
				</button>
			{/if}
			{#if icon}
				<button
					type="button"
					class="w-full px-3 py-1.5 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-800 transition text-orange-600 dark:text-orange-400"
					on:click|stopPropagation={resetAvatar}
				>
					{$i18n.t('Reset Avatar')}
				</button>
			{/if}
		</div>
	{/if}

	<!-- Built-in gallery -->
	{#if showGallery}
		<div
			class="absolute top-full left-0 mt-1 z-50 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-3 w-[320px]"
		>
			<div class="flex items-center justify-between mb-2">
				<span class="text-xs text-gray-500">{$i18n.t('Built-in Avatars')}</span>
				<button
					type="button"
					class="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 px-1.5 py-0.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
					on:click|stopPropagation={() => {
						showGallery = false;
					}}
				>
					{$i18n.t('Back')}
				</button>
			</div>
			<div class="grid grid-cols-6 gap-2 max-h-[240px] overflow-y-auto">
				{#each CONNECTION_AVATAR_FILES as filename}
					{@const isSelected = icon === `${AVATAR_BASE}/${filename}`}
					{@const needsInvert = DARK_MODE_INVERT_CONN_AVATARS.has(filename)}
					<button
						type="button"
						class="size-10 rounded-lg overflow-hidden border-2 transition hover:scale-105 flex items-center justify-center bg-gray-50 dark:bg-gray-800
							{isSelected
							? 'border-blue-500 ring-1 ring-blue-300'
							: 'border-gray-200 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click|stopPropagation={() => selectBuiltIn(filename)}
						title={filename.replace(/\.[^.]+$/, '')}
					>
						<img
							src="{AVATAR_BASE}/{filename}"
							alt={filename}
							class="w-full h-full object-contain p-0.5"
							class:avatar-invert={needsInvert}
							on:error={(e) => {
								e.currentTarget.style.display = 'none';
							}}
						/>
					</button>
				{/each}
			</div>
		</div>
	{/if}

	<input
		type="file"
		accept="image/*"
		class="hidden"
		bind:this={fileInput}
		on:change={handleUpload}
	/>
</div>

<style>
	:global(html.dark) .avatar-invert {
		filter: invert(1) brightness(1.12) contrast(1.06);
	}
</style>
