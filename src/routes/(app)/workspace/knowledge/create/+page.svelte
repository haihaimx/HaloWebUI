<script>
	import CreateKnowledgeBase from '$lib/components/workspace/Knowledge/CreateKnowledgeBase.svelte';
	import WorkspaceSubpageHeader from '$lib/components/workspace/shell/WorkspaceSubpageHeader.svelte';
</script>

<div class="space-y-4">
	<WorkspaceSubpageHeader
		backHref="/workspace/knowledge"
		titleKey="Create Knowledge Base"
		descKey="Start a new collection for documents, notes, and retrieval-ready workspace context."
	/>
	<CreateKnowledgeBase showBackButton={false} showIntro={false} />
</div>
