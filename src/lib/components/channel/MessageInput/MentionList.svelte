<script lang="ts">
	import { createEventDispatcher, getContext, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';
	import type { Writable } from 'svelte/store';

	const i18n: Writable<any> = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let query = '';
	export let users: { id: string; name: string; email: string; profile_image_url: string }[] = [];

	let selectedIdx = 0;
	let filteredUsers: typeof users = [];

	$: {
		const q = query.toLowerCase();
		filteredUsers = q
			? users.filter((u) => u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q))
			: users;
		filteredUsers = filteredUsers.slice(0, 8);
		selectedIdx = 0;
	}

	export const selectUp = () => {
		selectedIdx = Math.max(0, selectedIdx - 1);
	};

	export const selectDown = () => {
		selectedIdx = Math.min(selectedIdx + 1, filteredUsers.length - 1);
	};

	export const confirmSelect = () => {
		if (filteredUsers[selectedIdx]) {
			dispatch('select', filteredUsers[selectedIdx]);
		}
	};
</script>

{#if filteredUsers.length > 0}
	<div
		class="absolute bottom-full left-0 right-0 mb-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50 max-h-48 overflow-y-auto"
		in:fade={{ duration: 50 }}
	>
		{#each filteredUsers as user, idx}
			<button
				class="w-full flex items-center gap-2 px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 {idx ===
				selectedIdx
					? 'bg-gray-100 dark:bg-gray-800'
					: ''}"
				on:click|preventDefault|stopPropagation={() => {
					dispatch('select', user);
				}}
			>
				<img
					src={user.profile_image_url}
					alt={user.name}
					class="w-6 h-6 rounded-full object-cover"
				/>
				<span class="font-medium truncate">{user.name}</span>
				<span class="text-gray-400 text-xs truncate">{user.email}</span>
			</button>
		{/each}
	</div>
{/if}
