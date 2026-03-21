<script lang="ts">
	import DOMPurify from 'dompurify';

	import { onDestroy } from 'svelte';

	import tippy from 'tippy.js';

	export let placement = 'top';
	export let content = `I'm a tooltip!`;
	export let touch = true;
	export let className = 'flex';
	export let theme = '';
	export let offset = [0, 4];
	export let allowHTML = true;
	export let tippyOptions = {};

	let tooltipElement;
	let tooltipInstance;

	// Lazy: only create tippy on first hover, not on mount
	function initTooltip() {
		if (tooltipInstance || !tooltipElement || !content) return;
		tooltipInstance = tippy(tooltipElement, {
			content: DOMPurify.sanitize(content),
			placement,
			allowHTML,
			touch,
			...(theme !== '' ? { theme } : { theme: 'dark' }),
			arrow: false,
			offset,
			appendTo: () => document.body,
			zIndex: 11001,
			showOnCreate: true,
			...tippyOptions
		});
	}

	// Only update content if instance already exists (created by hover)
	$: if (tooltipInstance) {
		if (content) {
			tooltipInstance.setContent(DOMPurify.sanitize(content));
		} else {
			tooltipInstance.destroy();
			tooltipInstance = null;
		}
	}

	onDestroy(() => {
		if (tooltipInstance) {
			tooltipInstance.destroy();
		}
	});
</script>

<div
	bind:this={tooltipElement}
	on:pointerenter={initTooltip}
	on:focusin={initTooltip}
	aria-label={content}
	class={className}
>
	<slot />
</div>
