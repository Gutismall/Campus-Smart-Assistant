import React from 'react';

export default function SystemMessage({ messages = [], sources = [] }) {
    return (
        <div className="flex flex-col gap-3 max-w-[85%]">
            <div className="flex items-end gap-2">
                <div className="bg-white dark:bg-slate-800 p-4 rounded-2xl rounded-bl-none shadow-sm border border-slate-200 dark:border-slate-700 w-full">
                    {messages.map((msg, idx) => (
                        <p key={idx} className="text-sm leading-relaxed mb-4 last:mb-0" dangerouslySetInnerHTML={{ __html: msg }} />
                    ))}

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
