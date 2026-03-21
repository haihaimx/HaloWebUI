export type CuratedLobeHubSkillCategory =
	| 'Documents'
	| 'Browser Automation'
	| 'Notes'
	| 'Social Media'
	| 'Research'
	| 'Web & Frontend';

export type CuratedLobeHubSkillIcon =
	| 'document'
	| 'document-duplicate'
	| 'globe'
	| 'book-open'
	| 'chat-bubble'
	| 'command-line';

export interface CuratedLobeHubSkill {
	id: string;
	identifier: string;
	title: string;
	description: string;
	category: CuratedLobeHubSkillCategory;
	icon: CuratedLobeHubSkillIcon;
	accent: string;
	skillUrl: string;
	downloadUrl: string;
}

export const VERIFIED_LOBEHUB_SKILLS: CuratedLobeHubSkill[] = [
	{
		id: 'anthropics-skills-pdf',
		identifier: 'anthropics-skills-pdf',
		title: 'PDF Toolkit',
		description: 'Read, extract, merge, split, watermark, and OCR PDF files.',
		category: 'Documents',
		icon: 'document',
		accent: 'from-rose-400 via-orange-300 to-amber-200',
		skillUrl: 'https://lobehub.com/skills/anthropics-skills-pdf',
		downloadUrl: 'https://market.lobehub.com/api/v1/skills/anthropics-skills-pdf/download'
	},
	{
		id: 'anthropics-skills-pptx',
		identifier: 'anthropics-skills-pptx',
		title: 'PPTX Toolkit',
		description: 'Create, inspect, edit, and automate PowerPoint presentations.',
		category: 'Documents',
		icon: 'document-duplicate',
		accent: 'from-fuchsia-400 via-pink-300 to-rose-200',
		skillUrl: 'https://lobehub.com/skills/anthropics-skills-pptx',
		downloadUrl: 'https://market.lobehub.com/api/v1/skills/anthropics-skills-pptx/download'
	},
	{
		id: 'anthropics-skills-webapp-testing',
		identifier: 'anthropics-skills-webapp-testing',
		title: 'Webapp Testing',
		description: 'Use Playwright to test, debug, and inspect local web applications.',
		category: 'Browser Automation',
		icon: 'globe',
		accent: 'from-sky-400 via-cyan-300 to-teal-300',
		skillUrl: 'https://lobehub.com/skills/anthropics-skills-webapp-testing',
		downloadUrl:
			'https://market.lobehub.com/api/v1/skills/anthropics-skills-webapp-testing/download'
	},
	{
		id: 'openclaw-openclaw-apple-notes',
		identifier: 'openclaw-openclaw-apple-notes',
		title: 'Apple Notes',
		description: 'Manage Apple Notes from the terminal on macOS with memo CLI.',
		category: 'Notes',
		icon: 'book-open',
		accent: 'from-violet-400 via-purple-300 to-fuchsia-200',
		skillUrl: 'https://lobehub.com/skills/openclaw-openclaw-apple-notes',
		downloadUrl: 'https://market.lobehub.com/api/v1/skills/openclaw-openclaw-apple-notes/download'
	},
	{
		id: 'openclaw-skills-x-twitter',
		identifier: 'openclaw-skills-x-twitter',
		title: 'X / Twitter CLI',
		description: 'Read, search, post, and manage Twitter/X workflows from the terminal.',
		category: 'Social Media',
		icon: 'chat-bubble',
		accent: 'from-slate-500 via-slate-400 to-gray-300',
		skillUrl: 'https://lobehub.com/skills/openclaw-skills-x-twitter',
		downloadUrl: 'https://market.lobehub.com/api/v1/skills/openclaw-skills-x-twitter/download'
	},
	{
		id: 'openclaw-skills-reddit-scraper',
		identifier: 'openclaw-skills-reddit-scraper',
		title: 'Reddit Scraper',
		description: 'Read and search Reddit content with a lightweight, read-only CLI workflow.',
		category: 'Research',
		icon: 'chat-bubble',
		accent: 'from-orange-400 via-amber-300 to-yellow-200',
		skillUrl: 'https://lobehub.com/skills/openclaw-skills-reddit-scraper',
		downloadUrl: 'https://market.lobehub.com/api/v1/skills/openclaw-skills-reddit-scraper/download'
	},
	{
		id: 'code-yeongyu-oh-my-opencode-frontend-ui-ux',
		identifier: 'code-yeongyu-oh-my-opencode-frontend-ui-ux',
		title: 'Frontend UI / UX',
		description: 'Design-aware frontend implementation guidance for polished, non-generic UI.',
		category: 'Web & Frontend',
		icon: 'command-line',
		accent: 'from-emerald-400 via-lime-300 to-teal-200',
		skillUrl: 'https://lobehub.com/skills/code-yeongyu-oh-my-opencode-frontend-ui-ux',
		downloadUrl:
			'https://market.lobehub.com/api/v1/skills/code-yeongyu-oh-my-opencode-frontend-ui-ux/download'
	},
	{
		id: 'bobmatnyc-claude-mpm-artifacts-builder',
		identifier: 'bobmatnyc-claude-mpm-artifacts-builder',
		title: 'artifacts-builder',
		description:
			'Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui).',
		category: 'Web & Frontend',
		icon: 'globe',
		accent: 'from-cyan-400 via-sky-300 to-indigo-200',
		skillUrl: 'https://lobehub.com/skills/bobmatnyc-claude-mpm-artifacts-builder',
		downloadUrl:
			'https://market.lobehub.com/api/v1/skills/bobmatnyc-claude-mpm-artifacts-builder/download'
	}
];

export const getVerifiedLobeHubSkillByIdentifier = (identifier?: string | null) =>
	VERIFIED_LOBEHUB_SKILLS.find((skill) => skill.identifier === identifier) ?? null;

export const isVerifiedLobeHubSkillIdentifier = (identifier?: string | null) =>
	Boolean(getVerifiedLobeHubSkillByIdentifier(identifier));
