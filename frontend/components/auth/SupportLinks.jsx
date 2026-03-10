import React from 'react';

export default function SupportLinks() {
    return (
        <div className="mt-8 flex justify-center gap-6">
            <a className="flex items-center gap-1 text-slate-500 dark:text-slate-400 text-xs hover:text-primary transition-colors" href="#">
                <span className="material-symbols-outlined text-sm">help</span>
                Support Center
            </a>
            <a className="flex items-center gap-1 text-slate-500 dark:text-slate-400 text-xs hover:text-primary transition-colors" href="#">
                <span className="material-symbols-outlined text-sm">g_translate</span>
                Language
            </a>
            <a className="flex items-center gap-1 text-slate-500 dark:text-slate-400 text-xs hover:text-primary transition-colors" href="#">
                <span className="material-symbols-outlined text-sm">verified_user</span>
                Privacy Policy
            </a>
        </div>
    );
}
