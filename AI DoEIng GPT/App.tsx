
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { GoogleGenAI } from "@google/genai";
import { jsPDF } from "jspdf";
import { Q_DIVISIONS, PROMPT_DATA, S1000D_CHECKLIST_TABLES } from './constants';
import type { PromptItem, GeneratedDocument, GeminiService, ExportFormat, S1000DTable } from './types';
import { ViewMode, ViewModeType } from './types';

// Mock Gemini Service (updated for refinement)
const mockGeminiService: GeminiService = {
  generateDocumentContent: async (promptDescription: string, promptId: string, originalContent?: string, refinementInstruction?: string): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    if (!process.env.API_KEY) {
      console.warn("API Key not found. Using mock response. Please set the API_KEY environment variable for actual Gemini calls.");
      if (originalContent && refinementInstruction) {
        return `Refined content for ${promptId} based on "${refinementInstruction}". Original: "${originalContent.substring(0,50)}..."`;
      }
      return `Mock content for ${promptId}: ${promptDescription.substring(0,100)}... (API Key Missing)`;
    }

    let prompt;
    if (originalContent && refinementInstruction) {
      prompt = `
        Original Document Content (for Prompt ID ${promptId}):
        ---
        ${originalContent}
        ---
        Refinement Instruction: ${refinementInstruction}
        ---
        Please provide the refined document content based on the instruction. Output only the refined content.
      `;
    } else {
      prompt = `Generate a document section based on the following description for Prompt ID ${promptId}: ${promptDescription}. Focus on providing a concise summary or an introductory paragraph that would be suitable for a technical document. The document should be well-structured with a clear title and logical blocks of content. Ensure the output is formatted clearly.`;
    }

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash-preview-04-17',
        contents: prompt,
      });
      return response.text;
    } catch (error) {
      console.error("Error generating/refining document content:", error);
      return Promise.reject(`Error processing content for ${promptId}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
};

const APP_STYLES = `
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    background-color: #111827; /* Tailwind bg-gray-900 */
    color: #f3f4f6; /* Tailwind text-gray-100 */
    line-height: 1.6;
  }
  .app-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  header {
    background-color: #1f2937; /* Tailwind bg-gray-800 */
    color: white;
    padding: 1.5rem 2rem; /* Increased padding */
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  header h1 {
    margin: 0 0 0.25rem 0;
    font-size: 2.5rem; /* Main title size */
    font-weight: 700; /* Bold */
  }
  header .full-name-subtitle { /* New class for the full name */
    font-size: 1.25rem; /* Size for full name */
    font-style: italic;
    color: #cbd5e1; /* Tailwind slate-300 */
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
  }
  header .tagline { /* New class for tagline */
    font-size: 1rem;
    color: #9ca3af; /* Tailwind text-gray-400 */
    margin-top: 0.25rem;
    margin-bottom: 0;
  }
  main {
    display: flex;
    flex-grow: 1;
    padding: 1rem;
    gap: 1rem;
  }
  .sidebar {
    width: 350px; /* Increased width */
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: calc(100vh - 180px); /* Adjust based on new header height */
    overflow-y: auto;
    background-color: #1f2937; /* Tailwind bg-gray-800 */
    padding: 1rem;
    border-radius: 8px;
  }
  .content-area {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: calc(100vh - 180px); /* Adjust based on new header height */
    overflow-y: auto;
  }
  .card {
    background-color: #374151; /* Tailwind bg-gray-700 */
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.05);
    color: #d1d5db; /* Tailwind text-gray-300 */
  }
  .card h2 {
    margin-top: 0;
    font-size: 1.5rem; /* Increased font size */
    color: #e5e7eb; /* Tailwind text-gray-200 */
    border-bottom: 1px solid #4b5563; /* Tailwind border-gray-600 */
    padding-bottom: 0.75rem; /* Increased padding */
    margin-bottom: 1.25rem; /* Increased margin */
  }
  .card h3 {
    margin-top: 0;
    font-size: 1.25rem; /* Increased font size */
    color: #d1d5db; /* Tailwind text-gray-300 */
  }
  select, input[type="text"], textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #4b5563; /* Tailwind border-gray-600 */
    background-color: #1f2937; /* Tailwind bg-gray-800 */
    color: #e5e7eb; /* Tailwind text-gray-200 */
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 0.95rem;
    margin-bottom: 0.75rem; /* Increased margin */
  }
  select:focus, input[type="text"]:focus, textarea:focus {
    outline: none;
    border-color: #3b82f6; /* Tailwind border-blue-500 */
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4);
  }
  button {
    background-color: #2563eb; /* Tailwind bg-blue-600 */
    color: white;
    border: none;
    padding: 0.75rem 1.25rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    transition: background-color 0.2s ease;
  }
  button:hover:not(:disabled) {
    background-color: #1d4ed8; /* Tailwind bg-blue-700 */
  }
  button:disabled {
    background-color: #4b5563; /* Tailwind bg-gray-600 */
    cursor: not-allowed;
    opacity: 0.7;
  }
  .button-secondary {
    background-color: #4b5563; /* Tailwind bg-gray-600 */
  }
  .button-secondary:hover:not(:disabled) {
    background-color: #374151; /* Tailwind bg-gray-700 */
  }
  .prompt-list, .recently-used ul {
    list-style: none;
    padding: 0;
    max-height: 280px; /* Increased height */
    overflow-y: auto;
    border: 1px solid #4b5563; /* Tailwind border-gray-600 */
    border-radius: 4px;
    background-color: #1f2937; /* Tailwind bg-gray-800 */
  }
  .prompt-list li, .recently-used li {
    padding: 0.75rem 1rem;
    cursor: pointer;
    border-bottom: 1px solid #374151; /* Tailwind border-gray-700 */
    transition: background-color 0.2s ease;
    font-size: 0.9rem;
    color: #d1d5db; /* Tailwind text-gray-300 */
  }
  .prompt-list li:last-child, .recently-used li:last-child {
    border-bottom: none;
  }
  .prompt-list li:hover, .recently-used li:hover {
    background-color: #374151; /* Tailwind bg-gray-700 */
  }
  .prompt-list li.selected, .recently-used li.selected {
    background-color: #2563eb; /* Tailwind bg-blue-600 */
    color: white;
    font-weight: bold;
  }
  .error-message {
    color: #f87171; /* Tailwind text-red-400 */
    background-color: #450a0a; /* Tailwind bg-red-900 */
    border: 1px solid #ef4444; /* Tailwind border-red-500 */
    padding: 1rem;
    border-radius: 4px;
  }
  .generated-documents-section .documents-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  .view-mode-toggle button {
    background-color: #4b5563; /* Tailwind bg-gray-600 */
    color: #e5e7eb; /* Tailwind text-gray-200 */
    margin-left: 0.5rem;
  }
  .view-mode-toggle button.active {
    background-color: #2563eb; /* Tailwind bg-blue-600 */
    color: white;
  }
  .document-list {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column; /* List view default */
    gap: 1rem;
  }
  .document-list.grid {
    flex-direction: row; /* Grid view */
    flex-wrap: wrap;
  }
  .document-item {
    /* Styles for list items common to both views */
    border: 1px solid #4b5563; /* Tailwind border-gray-600 */
  }
  .document-list.grid .document-item {
    width: calc(50% - 0.5rem); /* Adjusted for gap */
  }
  .document-list.grid .document-item:nth-child(odd) {
     /* No margin needed if using gap property */
  }
  .document-content-preview pre {
    background-color: #1f2937; /* Tailwind bg-gray-800 */
    padding: 0.75rem;
    border-radius: 4px;
    max-height: 150px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
    font-size: 0.85rem;
    color: #9ca3af; /* Tailwind text-gray-400 */
    border: 1px solid #4b5563; /* Tailwind border-gray-600 */
  }
  .document-actions {
    margin-top: 1rem;
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex-wrap: wrap;
  }
  .export-action {
    position: relative;
  }
  .export-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    background-color: #374151; /* Tailwind bg-gray-700 */
    border: 1px solid #4b5563; /* Tailwind border-gray-600 */
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    z-index: 10;
    display: flex;
    flex-direction: column;
    min-width: 100px;
  }
  .export-dropdown button {
    background-color: #374151; /* Tailwind bg-gray-700 */
    color: #e5e7eb; /* Tailwind text-gray-200 */
    text-align: left;
    padding: 0.5rem 1rem;
    border-radius: 0;
    width: 100%;
  }
  .export-dropdown button:hover {
    background-color: #4b5563; /* Tailwind bg-gray-600 */
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(17, 24, 39, 0.8); /* Tailwind bg-gray-900 with opacity */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 1rem;
  }
  .modal-content {
    width: 90%;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
  }
  .modal-content textarea {
    min-height: 100px;
    margin-bottom: 1rem;
  }
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1rem;
  }
  .s1000d-utils-section .s1000d-table-item {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #4b5563; /* Tailwind border-gray-600 */
  }
  .s1000d-utils-section .s1000d-table-item:last-child {
    border-bottom: none;
  }
  .s1000d-utils-section h4 {
    font-size: 1.1rem;
    color: #e5e7eb; /* Tailwind text-gray-200 */
    margin-bottom: 0.5rem;
  }

  /* Responsive adjustments */
  @media (max-width: 900px) {
    .document-list.grid .document-item {
      width: 100%; /* Full width for grid items on smaller screens */
    }
  }
  @media (max-width: 768px) {
    main {
      flex-direction: column;
      max-height: none;
    }
    .sidebar, .content-area {
      width: 100%;
      max-height: none; /* Allow full scroll on mobile */
      overflow-y: visible;
    }
     .sidebar {
        max-height: 50vh; /* Or some appropriate height */
        overflow-y: auto;
    }
    .content-area {
        overflow-y: auto; /* Allow content area to scroll independently if needed */
    }
     header h1 {
      font-size: 1.8rem;
    }
    header .full-name-subtitle {
        font-size: 1.1rem;
    }
    header .tagline {
      font-size: 0.9rem;
    }
  }
`;

export const App = (): JSX.Element => {
  const [selectedDivision, setSelectedDivision] = useState<string | null>(null);
  const [selectedPrompt, setSelectedPrompt] = useState<PromptItem | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [generatedDocuments, setGeneratedDocuments] = useState<GeneratedDocument[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isRefiningLoading, setIsRefiningLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [recentlyUsed, setRecentlyUsed] = useState<PromptItem[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [geminiService, setGeminiService] = useState<GeminiService>(mockGeminiService);
  const [viewMode, setViewMode] = useState<ViewModeType>(ViewMode.List);

  const [showRefineModal, setShowRefineModal] = useState<boolean>(false);
  const [refiningDoc, setRefiningDoc] = useState<GeneratedDocument | null>(null);
  const [refinementInstruction, setRefinementInstruction] = useState<string>('');
  const [showExportDropdown, setShowExportDropdown] = useState<string | null>(null); // Store doc.id for which dropdown is open

  useEffect(() => {
    const styleTag = document.createElement('style');
    styleTag.id = 'app-styles';
    styleTag.innerHTML = APP_STYLES;
    document.head.appendChild(styleTag);

    return () => {
      const existingStyleTag = document.getElementById('app-styles');
      if (existingStyleTag) {
        document.head.removeChild(existingStyleTag);
      }
    };
  }, []);

  useEffect(() => {
    const storedRecentlyUsed = localStorage.getItem('recentlyUsedPrompts');
    if (storedRecentlyUsed) {
      try {
        setRecentlyUsed(JSON.parse(storedRecentlyUsed));
      } catch (e) {
        console.error("Failed to parse recently used prompts from localStorage", e);
        localStorage.removeItem('recentlyUsedPrompts');
      }
    }
  }, []);

  const updateRecentlyUsed = useCallback((prompt: PromptItem) => {
    setRecentlyUsed(prev => {
      const newRecentlyUsed = [prompt, ...prev.filter(p => p.promptId !== prompt.promptId)].slice(0, 5);
      localStorage.setItem('recentlyUsedPrompts', JSON.stringify(newRecentlyUsed));
      return newRecentlyUsed;
    });
  }, []);

  const handleDivisionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedDivision(event.target.value);
    setSelectedPrompt(null);
    setSearchTerm('');
  };

  const handlePromptSelect = (prompt: PromptItem) => {
    setSelectedPrompt(prompt);
  };

  const handleGenerateDocument = async () => {
    if (!selectedPrompt) {
      setError("Please select a prompt first.");
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const generatedContent = await geminiService.generateDocumentContent(selectedPrompt.description, selectedPrompt.promptId);
      const newDocument: GeneratedDocument = {
        id: `doc-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
        metadata: selectedPrompt,
        title: `Doc: ${selectedPrompt.promptId}`,
        generatedContent: generatedContent,
        refinementHistory: []
      };
      setGeneratedDocuments(prev => [newDocument, ...prev]);
      updateRecentlyUsed(selectedPrompt);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartRefine = (doc: GeneratedDocument) => {
    setRefiningDoc(doc);
    setRefinementInstruction('');
    setShowRefineModal(true);
  };

  const handleRefineSubmit = async () => {
    if (!refiningDoc || !refinementInstruction.trim()) {
      setError("Refinement instruction cannot be empty.");
      return;
    }
    setIsRefiningLoading(true);
    setError(null);
    try {
      const refinedContent = await geminiService.generateDocumentContent(
        refiningDoc.metadata.description,
        refiningDoc.metadata.promptId,
        refiningDoc.generatedContent,
        refinementInstruction
      );
      setGeneratedDocuments(prevDocs =>
        prevDocs.map(doc =>
          doc.id === refiningDoc.id
            ? { 
                ...doc, 
                generatedContent: refinedContent, 
                refinementHistory: [...(doc.refinementHistory || []), { instruction: refinementInstruction, content: doc.generatedContent }] 
              }
            : doc
        )
      );
      setShowRefineModal(false);
      setRefiningDoc(null);
    } catch (err) {
      setError(`Refinement failed: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsRefiningLoading(false);
    }
  };
  
  const downloadFile = (filename: string, content: string, mimeType: string) => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: mimeType });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element); 
    element.click();
    document.body.removeChild(element);
    URL.revokeObjectURL(element.href); 
  };

  const handleExport = (doc: GeneratedDocument, format: ExportFormat) => {
    const filenameBase = `${doc.metadata.promptId}_${doc.metadata.docId}`.replace(/[^a-z0-9_.-]/gi, '_');
    switch (format) {
      case 'md':
        downloadFile(`${filenameBase}.md`, doc.generatedContent, 'text/markdown;charset=utf-8');
        break;
      case 'json':
        downloadFile(`${filenameBase}.json`, JSON.stringify(doc, null, 2), 'application/json;charset=utf-8');
        break;
      case 'html':
        const htmlContent = `
          <!DOCTYPE html>
          <html lang="en">
          <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${doc.title}</title>
            <style>body { font-family: sans-serif; line-height: 1.6; padding: 20px; color: #333; background-color: #f8f9fa; } h1 { color: #2c3e50; } pre { white-space: pre-wrap; word-wrap: break-word; background: #fff; padding: 15px; border-radius: 5px; border: 1px solid #ddd; font-size: 0.9em; } hr { border: 0; border-top: 1px solid #ccc; margin: 20px 0; }</style>
          </head>
          <body>
            <h1>${doc.title}</h1>
            <p><strong>Prompt ID:</strong> ${doc.metadata.promptId}</p>
            <p><strong>Document ID:</strong> ${doc.metadata.docId}</p>
            <p><strong>Path:</strong> ${doc.metadata.path}</p>
            <p><strong>Description:</strong> ${doc.metadata.description}</p>
            <hr>
            <h2>Generated Content</h2>
            <pre>${doc.generatedContent.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</pre>
          </body>
          </html>`;
        downloadFile(`${filenameBase}.html`, htmlContent, 'text/html;charset=utf-8');
        break;
      case 'xml':
        const xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<document>
  <metadata>
    <promptId><![CDATA[${doc.metadata.promptId}