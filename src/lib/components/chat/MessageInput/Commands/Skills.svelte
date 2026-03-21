<script lang="ts">
	import { skills } from '$lib/stores';
	import { tick, getContext } from 'svelte';

	const i18n = getContext('i18n');

	export let prompt = '';
	export let command = '';

	let selectedIdx = 0;
	let filteredSkills = [];

	$: filteredSkills = ($skills ?? [])
		.filter((s) => s.is_active !== false)
		.filter(
			(s) =>
				s.name.toLowerCase().includes(command.slice(1).toLowerCase()) ||
				s.description.toLowerCase().includes(command.slice(1).toLowerCase())
		)
		.sort((a, b) => a.name.localeCompare(b.name));

	$: if (command) {
		selectedIdx = 0;
	}

	export const selectUp = () => {
		selectedIdx = Math.max(0, selectedIdx - 1);
	};

	export const selectDown = () => {
		selectedIdx = Math.min(selectedIdx + 1, filteredSkills.length - 1);
	};

	const confirmSkill = async (skill) => {
		const text = skill.content || '';

		const lines = prompt.split('\n');
		const lastLine = lines.pop();

		const lastLineWords = lastLine.split(' ');
		lastLineWords.pop();

		lastLineWords.push(text);
		lines.push(lastLineWords.join(' '));
		prompt = lines.join('\n');

		const chatInputElement = document.getElementById('chat-input');
		await tick();
		if (chatInputElement) {
			chatInputElement.focus();
			chatInputElement.dispatchEvent(new Event('input'));
		}
	};
</script>

{#if filteredSkills.length > 0}
	<div
		id="commands-container"
		class="px-2 mb-2 text-left w-full absolute bottom-0 left-0 right-0 z-10"
	>
		<div class="flex w-full rounded-xl border border-gray-100 dark:border-gray-850">
			<div
				class="max-h-60 flex flex-col w-full rounded-xl bg-white dark:bg-gray-900 dark:text-gray-100"
			>
				<div class="m-1 overflow-y-auto p-1 space-y-0.5 scrollbar-hidden">
					{#each filteredSkills as skill, idx}
						<button
							class=" px-3 py-1.5 rounded-xl w-full text-left {idx === selectedIdx
								? '  bg-gray-50 dark:bg-gray-850 selected-command-option-button'
								: ''}"
							type="button"
							on:click={() => {
								confirmSkill(skill);
							}}
							on:mousemove={() => {
								selectedIdx = idx;
							}}
							on:focus={() => {}}
						>
							<div class=" font-medium text-black dark:text-gray-100">
								{skill.name}
							</div>

							{#if skill.description}
								<div class=" text-xs text-gray-600 dark:text-gray-100 line-clamp-1">
									{skill.description}
								</div>
							{/if}
						</button>
					{/each}
				</div>

				<div
					class=" px-2 pt-0.5 pb-1 text-xs text-gray-600 dark:text-gray-100 bg-white dark:bg-gray-900 rounded-b-xl flex items-center space-x-1"
				>
					<div>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="w-3 h-3"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"
							/>
						</svg>
					</div>

					<div class="line-clamp-1">
						{$i18n.t('Select a skill to insert its content into the prompt.')}
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
