<script lang="ts">
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Plus from '$lib/components/icons/Plus.svelte';

	let selected = '';
</script>

<div
	class="min-w-[5.5rem] bg-gray-50/80 dark:bg-gray-950/80 backdrop-blur-xl flex gap-3 flex-col pt-8 h-screen border-r border-gray-100 dark:border-gray-900 z-50 transition-all duration-300"
>
	<div class="flex justify-center relative">
		{#if selected === 'home'}
			<div class="absolute top-0 left-0 flex h-full">
				<div class="my-auto rounded-r-lg w-1.5 h-8 bg-black dark:bg-white transition-all"></div>
			</div>
		{/if}

		<Tooltip content="Home" placement="right">
			<button
				class=" cursor-pointer transition-all duration-200 {selected === 'home'
					? 'rounded-2xl scale-105 shadow-md'
					: 'rounded-3xl hover:bg-gray-100 dark:hover:bg-gray-900'} p-2"
				on:click={() => {
					selected = 'home';

					if (window.electronAPI) {
						window.electronAPI.load('home');
					}
				}}
			>
				<img src="/static/splash.png" class="size-10 dark:invert" alt="logo" draggable="false" />
			</button>
		</Tooltip>
	</div>

	<div class="my-2 border-b-2 border-gray-100 dark:border-gray-800 mx-6 rounded-full"></div>

	<div class="flex justify-center relative group">
		{#if selected === ''}
			<div class="absolute top-0 left-0 flex h-full">
				<div class="my-auto rounded-r-lg w-1.5 h-8 bg-black dark:bg-white transition-all"></div>
			</div>
		{/if}
		<Tooltip content="Chat" placement="right">
			<button
				class=" cursor-pointer transition-all duration-200 {selected === ''
					? 'rounded-2xl scale-105 shadow-md'
					: 'rounded-3xl hover:bg-gray-100 dark:hover:bg-gray-900'} p-2"
				on:click={() => {
					selected = '';
				}}
			>
				<img src="/static/favicon.png" class="size-9 dark:invert" alt="logo" draggable="false" />
			</button>
		</Tooltip>
	</div>

	<!-- <div class="flex justify-center relative group text-gray-400">
		<button class=" cursor-pointer p-2" on:click={() => {}}>
			<Plus className="size-4" strokeWidth="2" />
		</button>
	</div> -->
</div>
