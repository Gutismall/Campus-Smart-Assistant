import React from 'react';

export default function SystemMessage({ messages = [], sources = [] }) {
    return (
        <div className="flex flex-col gap-3 max-w-[85%]">
            <div className="flex items-end gap-2">
                <div className="bg-white dark:bg-slate-800 p-4 rounded-2xl rounded-bl-none shadow-sm border border-slate-200 dark:border-slate-700 w-full">
                    {messages.map((msg, idx) => {
                        let parsedData = null;
                        try {
                            let cleanMsg = msg.trim();
                            // Attempt to clean markdown if present (e.g. ```json ... ```)
                            if (cleanMsg.startsWith('```json')) {
                                cleanMsg = cleanMsg.replace(/^```json/, '').replace(/```$/, '').trim();
                            }
                            const obj = JSON.parse(cleanMsg);
                            if (obj && typeof obj === 'object' && obj.message && Array.isArray(obj.info)) {
                                parsedData = obj;
                            }
                        } catch (e) {
                            // Fallback to normal rendering if parsing fails
                        }

                        if (parsedData) {
                            return (
                                <div key={idx} className="text-sm leading-relaxed mb-4 last:mb-0">
                                    <p className="mb-3 font-medium text-slate-800 dark:text-slate-200">{parsedData.message}</p>
                                    <div className="space-y-4">
                                        {parsedData.info.map((infoItem, i) => (
                                            <div key={i} className="flex flex-col space-y-1">
                                                {typeof infoItem === 'object' && infoItem !== null ? (
                                                    Object.entries(infoItem).map(([key, value], kIdx) => (
                                                        <p key={kIdx} className="m-0 text-slate-700 dark:text-slate-300">
                                                            <span className="font-semibold text-slate-900 dark:text-slate-100 mr-1">{key}:</span> {String(value)}
                                                        </p>
                                                    ))
                                                ) : (
                                                    <p className="m-0 text-slate-700 dark:text-slate-300">{String(infoItem)}</p>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            );
                        }

                        // Original fallback for unstructured string / HTML formats
                        let fallbackMsg = msg;
                        if (typeof msg === 'string') {
                            // Replace markdown bold with HTML bold and newlines with <br/>
                            fallbackMsg = msg
                                .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                                .replace(/\n/g, '<br/>');
                            
                            // If the AI collapses everything into a single line, force breaks before bold labels
                            if (!msg.includes('\n')) {
                                fallbackMsg = fallbackMsg.replace(/ <b>/g, '<br/><br/><b>');
                            }
                        }

                        return <p key={idx} className="text-sm leading-relaxed mb-4 last:mb-0" dangerouslySetInnerHTML={{ __html: fallbackMsg }} />;
                    })}

                    {/* Source Badges */}
                    {sources && sources.length > 0 && (
                        <div className="pt-3 border-t border-slate-100 dark:border-slate-700 mt-4 rounded-b-2xl">
                            <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Sources</p>
                            <div className="flex flex-wrap gap-2">
                                {sources.map((source, idx) => (
                                    <div key={idx} className="flex items-center gap-1.5 px-2 py-1 bg-primary/5 border border-primary/20 rounded-md text-[11px] font-medium text-primary">
                                        <span className="material-symbols-outlined text-xs">{source.icon || 'description'}</span>
                                        {source.label}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
