<script>
	import KnowledgeBase from '$lib/components/workspace/Knowledge/KnowledgeBase.svelte';
	import WorkspaceSubpageHeader from '$lib/components/workspace/shell/WorkspaceSubpageHeader.svelte';
</script>

<div class="space-y-4">
	<WorkspaceSubpageHeader
		backHref="/workspace/knowledge"
		titleKey="Knowledge Base"
		descKey="Review files, add content, and manage retrieval data for the selected workspace knowledge base."
	/>
	<KnowledgeBase />
</div>
