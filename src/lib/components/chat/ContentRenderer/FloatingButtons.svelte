<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { getContext, onDestroy, tick } from 'svelte';

	import { chatCompletion } from '$lib/apis/openai';
	import ChatBubble from '$lib/components/icons/ChatBubble.svelte';
	import LightBlub from '$lib/components/icons/LightBlub.svelte';
	import Markdown from '../Messages/Markdown.svelte';
	import Skeleton from '../Messages/Skeleton.svelte';

	const i18n = getContext('i18n');

	type FloatingAction = {
		id: string;
		label: string;
		icon?: any;
		input?: boolean;
		prompt: string;
	};

	export let id = '';
	export let model = null;
	export let messages = [];
	export let actions: FloatingAction[] = [];
	export let onAdd = () => {};

	const defaultActions: FloatingAction[] = [
		{
			id: 'ask',
			label: $i18n.t('Ask'),
			icon: ChatBubble,
			input: true,
			prompt: '{{SELECTED_CONTENT}}\n\n\n{{INPUT_CONTENT}}'
		},
		{
			id: 'explain',
			label: $i18n.t('Explain'),
			icon: LightBlub,
			input: false,
			prompt: `{{SELECTED_CONTENT}}\n\n\n${$i18n.t('Explain')}`
		}
	];
	$: resolvedActions = (actions ?? []).length > 0 ? actions : defaultActions;

	let floatingInput = false;
	let selectedAction: FloatingAction | null = null;

	let selectedText = '';
	let floatingInputValue = '';

	let prompt = '';
	let responseContent: string | null = null;
	let responseDone = false;
	let requestController: AbortController | null = null;

	const autoScroll = async () => {
		const responseContainer = document.getElementById('response-container');
		if (!responseContainer) {
			return;
		}

		if (
			responseContainer.scrollHeight - responseContainer.clientHeight <=
			responseContainer.scrollTop + 50
		) {
			responseContainer.scrollTop = responseContainer.scrollHeight;
		}
	};

	const buildPrompt = (action: FloatingAction, inputContent = '') => {
		const selectedQuotedText = selectedText
			.split('\n')
			.map((line) => `> ${line}`)
			.join('\n');

		return (action.prompt ?? '')
			.replaceAll('{{INPUT_CONTENT}}', inputContent)
			.replaceAll('{{CONTENT}}', selectedText)
			.replaceAll('{{SELECTED_CONTENT}}', selectedQuotedText);
	};

	const runAction = async (action: FloatingAction, inputContent = '') => {
		if (!model) {
			toast.error($i18n.t('Model not selected'));
			return;
		}

		prompt = buildPrompt(action, inputContent);
		floatingInputValue = '';

		responseContent = '';
		responseDone = false;

		const [res, controller] = await chatCompletion(localStorage.token, {
			model,
			messages: [
				...messages,
				{
					role: 'user',
					content: prompt
				}
			].map((message) => ({
				role: message.role,
				content: message.content
			})),
			stream: true
		});
		requestController = controller;

		if (!(res && res.ok)) {
			toast.error($i18n.t('An error occurred while fetching the explanation'));
			return;
		}

		const reader = res.body.getReader();
		const decoder = new TextDecoder();

		try {
			while (true) {
				const { done, value } = await reader.read();
				if (done) {
					break;
				}

				const chunk = decoder.decode(value, { stream: true });
				const lines = chunk.split('\n').filter((line) => line.trim() !== '');

				for (const line of lines) {
					if (!line.startsWith('data: ')) {
						continue;
					}

					if (line.startsWith('data: [DONE]')) {
						responseDone = true;
						await tick();
						autoScroll();
						continue;
					}

					try {
						const data = JSON.parse(line.slice(6));
						const delta = data?.choices?.[0]?.delta?.content;
						if (delta) {
							responseContent += delta;
							autoScroll();
						}
					} catch (error) {
						console.error(error);
					}
				}
			}
		} catch (error) {
			if ((error as Error)?.name !== 'AbortError') {
				console.error(error);
			}
		}
	};

	const addHandler = async () => {
		onAdd({
			modelId: model,
			parentId: id,
			messages: [
				{
					role: 'user',
					content: prompt
				},
				{
					role: 'assistant',
					content: responseContent
				}
			]
		});
	};

	export const closeHandler = () => {
		requestController?.abort();
		requestController = null;
		selectedAction = null;
		responseContent = null;
		responseDone = false;
		floatingInput = false;
		floatingInputValue = '';
	};

	onDestroy(() => {
		requestController?.abort();
	});
</script>

<div
	id={`floating-buttons-${id}`}
	class="absolute rounded-lg mt-1 text-xs z-9999"
	style="display: none"
>
	{#if responseContent === null}
		{#if !floatingInput}
			<div
				class="flex flex-row gap-0.5 shrink-0 p-1 bg-white dark:bg-gray-850 dark:text-gray-100 text-medium rounded-lg shadow-xl"
			>
				{#each resolvedActions as action}
					<button
						class="px-1 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-sm flex items-center gap-1 min-w-fit"
						on:click={async () => {
							selectedText = window.getSelection().toString();
							selectedAction = action;
							if (action.input) {
								floatingInput = true;
								await tick();
								setTimeout(() => {
									const input = document.getElementById('floating-message-input');
									input?.focus();
								}, 0);
							} else {
								runAction(action);
							}
						}}
					>
						{#if action.icon}
							<svelte:component this={action.icon} className="size-3 shrink-0" />
						{/if}
						<div class="shrink-0">{action.label}</div>
					</button>
				{/each}
			</div>
		{:else}
			<div
				class="py-1 flex dark:text-gray-100 bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-850 w-72 rounded-full shadow-xl"
			>
				<input
					type="text"
					id="floating-message-input"
					class="ml-5 bg-transparent outline-hidden w-full flex-1 text-sm"
					placeholder={$i18n.t('Ask a question')}
					bind:value={floatingInputValue}
					on:keydown={(e) => {
						if (e.key === 'Enter' && selectedAction) {
							floatingInput = false;
							runAction(selectedAction, floatingInputValue);
						}
					}}
				/>

				<div class="ml-1 mr-2">
					<button
						class="{floatingInputValue !== ''
							? 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
							: 'text-white bg-gray-200 dark:text-gray-900 dark:bg-gray-700 disabled'} transition rounded-full p-1.5 m-0.5 self-center"
						on:click={() => {
							if (selectedAction) {
								floatingInput = false;
								runAction(selectedAction, floatingInputValue);
							}
						}}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 16 16"
							fill="currentColor"
							class="size-4"
						>
							<path
								fill-rule="evenodd"
								d="M8 14a.75.75 0 0 1-.75-.75V4.56L4.03 7.78a.75.75 0 0 1-1.06-1.06l4.5-4.5a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06L8.75 4.56v8.69A.75.75 0 0 1 8 14Z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
				</div>
			</div>
		{/if}
	{:else}
		<div class="bg-white dark:bg-gray-850 dark:text-gray-100 rounded-xl shadow-xl w-80 max-w-full">
			<div
				class="bg-gray-50/50 dark:bg-gray-800 dark:text-gray-100 text-medium rounded-xl px-3.5 py-3 w-full"
			>
				<div class="font-medium">
					<Markdown id={`${id}-float-prompt`} content={prompt} />
				</div>
			</div>

			<div
				class="bg-white dark:bg-gray-850 dark:text-gray-100 text-medium rounded-xl px-3.5 py-3 w-full"
			>
				<div class=" max-h-80 overflow-y-auto w-full markdown-prose-xs" id="response-container">
					{#if (responseContent ?? '').trim() === ''}
						<Skeleton size="sm" />
					{:else}
						<Markdown id={`${id}-float-response`} content={responseContent ?? ''} />
					{/if}

					{#if responseDone}
						<div class="flex justify-end pt-3 text-sm font-medium">
							<button
								class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
								on:click={addHandler}
							>
								{$i18n.t('Add')}
							</button>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
