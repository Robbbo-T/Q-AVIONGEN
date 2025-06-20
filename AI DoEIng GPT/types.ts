
export interface PromptItem {
  promptId: string;
  docId: string;
  path: string;
  description: string;
  division: string; 
}

export interface PromptData {
  [division: string]: PromptItem[];
}

export interface GeneratedDocument {
  id: string; // Added unique ID for each document
  metadata: PromptItem;
  title: string;
  generatedContent: string;
  refinementHistory?: { instruction: string; content: string }[]; // Optional: to track refinements
}

// Gemini API related types (simplified for this example)
export interface GeminiService {
  generateDocumentContent: (promptDescription: string, promptId: string, originalContent?: string, refinementInstruction?: string) => Promise<string>;
}

export const ViewMode = {
  List: 'list',
  Grid: 'grid',
} as const;

export type ViewModeType = typeof ViewMode[keyof typeof ViewMode];

export type ExportFormat = 'md' | 'pdf' | 'xml' | 'html' | 'json';
