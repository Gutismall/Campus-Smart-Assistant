import React from 'react';

export default function Header({ navItems = [] }) {
    return (
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 lg:px-10 py-3 sticky top-0 z-50">
            <div className="flex items-center gap-4">
                <div className="text-primary">
                    <span className="material-symbols-outlined text-3xl">school</span>
                </div>
                <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-tight">Campus Assistant</h2>
            </div>
            <div className="flex flex-1 justify-end gap-6 items-center">
                <nav className="hidden md:flex items-center gap-6">
                    {navItems.map((item, index) => (
                        <a
                            key={index}
                            className="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors"
                            href={item.href}
                        >
                            {item.label}
                        </a>
                    ))}
                </nav>

                <div className="bg-primary/10 rounded-full h-10 w-10 flex items-center justify-center overflow-hidden border border-primary/20">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img alt="Student profile avatar" className="w-full h-full object-cover" data-alt="University student profile picture avatar" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDCZrZH8zNCmGQtTz9ByrCPMydlp_fOH2UAGDznOkwK3idEJ9fFrlZSVVw6Z1q6MSoFx2vrmP01yIIUFyW67D_4SGJcLutao87RHAcefUfVt44-aNpE0Ps-VMzfS2rDIQeU0Dz5T88EAemmx6JN7R7WXQPjXuuXhO-ifojo740CzYRFBA_8r-ZAghh3OC6UXmh0-jrPz0-WDyOrC1pk_QS1t-oD_TuOwpTL_OXj8-7uUpAUuu5R-BCjBT401kMzOQLuTf69bZwFx-E" />
                </div>
            </div>
        </header>
    );
}
