"use client";
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const verifyAuth = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                router.push('/auth/login');
                return;
            }

            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/verify`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    setIsAuthenticated(true);
                } else {
                    localStorage.removeItem('token');
                    router.push('/auth/login');
                }
            } catch (error) {
                console.error("Authentication check failed:", error);
                localStorage.removeItem('token');
                router.push('/auth/login');
            }
        };

        verifyAuth();
    }, [router]);

    if (!isAuthenticated) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    return (
        <div className="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-slate-100 min-h-screen flex flex-col">


            {/* Top Navigation Bar */}
            <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 lg:px-10 py-3 sticky top-0 z-50">
                <div className="flex items-center gap-4">
                    <div className="text-primary">
                        <span className="material-symbols-outlined text-3xl">school</span>
                    </div>
                    <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-tight">Campus Assistant</h2>
                </div>
                <div className="flex flex-1 justify-end gap-6 items-center">
                    <nav className="hidden md:flex items-center gap-6">
                        <a className="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors" href="#">Dashboard</a>
                        <a className="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors" href="#">Schedule</a>
                        <a className="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors" href="#">Grades</a>
                    </nav>
                    <div className="flex gap-2">
                        <button className="flex items-center justify-center rounded-lg h-10 w-10 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                            <span className="material-symbols-outlined text-xl">notifications</span>
                        </button>
                        <button className="flex items-center justify-center rounded-lg h-10 w-10 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                            <span className="material-symbols-outlined text-xl">settings</span>
                        </button>
                    </div>
                    <div className="bg-primary/10 rounded-full h-10 w-10 flex items-center justify-center overflow-hidden border border-primary/20">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img alt="Student profile avatar" className="w-full h-full object-cover" data-alt="University student profile picture avatar" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDCZrZH8zNCmGQtTz9ByrCPMydlp_fOH2UAGDznOkwK3idEJ9fFrlZSVVw6Z1q6MSoFx2vrmP01yIIUFyW67D_4SGJcLutao87RHAcefUfVt44-aNpE0Ps-VMzfS2rDIQeU0Dz5T88EAemmx6JN7R7WXQPjXuuXhO-ifojo740CzYRFBA_8r-ZAghh3OC6UXmh0-jrPz0-WDyOrC1pk_QS1t-oD_TuOwpTL_OXj8-7uUpAUuu5R-BCjBT401kMzOQLuTf69bZwFx-E" />
                    </div>
                </div>
            </header>

            <main className="flex-1 flex overflow-hidden max-w-[1600px] mx-auto w-full">
                {/* Left Sidebar: Today at a Glance */}
                <aside className="hidden lg:flex flex-col w-80 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 overflow-y-auto">
                    {/* Next Upcoming Test Widget */}
                    <div className="mb-8">
                        <h3 className="text-slate-900 dark:text-slate-100 text-sm font-bold uppercase tracking-wider mb-4">Upcoming Test</h3>
                        <div className="bg-primary/5 border border-primary/10 rounded-xl p-4">
                            <div className="text-primary text-xs font-bold mb-2 uppercase">Advanced Calculus</div>
                            <div className="flex gap-2 text-center">
                                <div className="flex-1 bg-white dark:bg-slate-800 rounded-lg p-2 shadow-sm">
                                    <div className="text-xl font-bold text-primary">00</div>
                                    <div className="text-[10px] uppercase text-slate-500">Days</div>
                                </div>
                                <div className="flex-1 bg-white dark:bg-slate-800 rounded-lg p-2 shadow-sm">
                                    <div className="text-xl font-bold text-primary">04</div>
                                    <div className="text-[10px] uppercase text-slate-500">Hrs</div>
                                </div>
                                <div className="flex-1 bg-white dark:bg-slate-800 rounded-lg p-2 shadow-sm">
                                    <div className="text-xl font-bold text-primary">22</div>
                                    <div className="text-[10px] uppercase text-slate-500">Min</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Open Now Status */}
                    <div className="mb-8">
                        <h3 className="text-slate-900 dark:text-slate-100 text-sm font-bold uppercase tracking-wider mb-4">Campus Status</h3>
                        <div className="space-y-3">
                            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                                <div className="flex items-center gap-3">
                                    <span className="material-symbols-outlined text-primary">menu_book</span>
                                    <span className="text-sm font-medium">Main Library</span>
                                </div>
                                <span className="flex h-2 w-2 rounded-full bg-green-500"></span>
                            </div>
                            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                                <div className="flex items-center gap-3">
                                    <span className="material-symbols-outlined text-primary">biotech</span>
                                    <span className="text-sm font-medium">Science Lab 4</span>
                                </div>
                                <span className="flex h-2 w-2 rounded-full bg-green-500"></span>
                            </div>
                            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                                <div className="flex items-center gap-3">
                                    <span className="material-symbols-outlined text-slate-400">fitness_center</span>
                                    <span className="text-sm font-medium">Student Gym</span>
                                </div>
                                <span className="flex h-2 w-2 rounded-full bg-orange-400"></span>
                            </div>
                        </div>
                    </div>

                    {/* Suggested Questions */}
                    <div>
                        <h3 className="text-slate-900 dark:text-slate-100 text-sm font-bold uppercase tracking-wider mb-4">Quick Questions</h3>
                        <div className="space-y-2">
                            <button className="w-full text-left p-3 text-xs font-medium bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg hover:border-primary hover:text-primary transition-all shadow-sm">
                                &quot;Where is Professor Cohen?&quot;
                            </button>
                            <button className="w-full text-left p-3 text-xs font-medium bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg hover:border-primary hover:text-primary transition-all shadow-sm">
                                &quot;When is the math final?&quot;
                            </button>
                            <button className="w-full text-left p-3 text-xs font-medium bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg hover:border-primary hover:text-primary transition-all shadow-sm">
                                &quot;Dining hall menu for today&quot;
                            </button>
                        </div>
                    </div>
                </aside>

                {/* Main Chat Area */}
                <section className="flex-1 flex flex-col bg-slate-50 dark:bg-background-dark overflow-hidden">
                    {/* Chat Header */}
                    <div className="px-6 py-4 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="relative">
                                <div className="size-10 rounded-full bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
                                    <span className="material-symbols-outlined">smart_toy</span>
                                </div>
                                <div className="absolute bottom-0 right-0 size-3 bg-green-500 border-2 border-white dark:border-slate-900 rounded-full"></div>
                            </div>
                            <div>
                                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">CampusBot</h3>
                                <p className="text-xs text-green-600 dark:text-green-500 font-medium leading-none">Online • University Assistant</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button className="p-2 text-slate-500 hover:text-primary transition-colors">
                                <span className="material-symbols-outlined">search</span>
                            </button>
                            <button className="p-2 text-slate-500 hover:text-primary transition-colors">
                                <span className="material-symbols-outlined">more_vert</span>
                            </button>
                        </div>
                    </div>

                    {/* Messages Area */}
                    <div className="flex-1 overflow-y-auto p-6 space-y-6">
                        {/* AI Message */}
                        <div className="flex flex-col gap-2 max-w-[80%]">
                            <div className="flex items-end gap-2">
                                <div className="bg-white dark:bg-slate-800 p-4 rounded-2xl rounded-bl-none shadow-sm border border-slate-200 dark:border-slate-700">
                                    <p className="text-sm leading-relaxed">Hello! I&apos;m your Campus Assistant. I can help you with your schedule, find locations on campus, or look up information from your syllabi. How can I help you today?</p>
                                </div>
                            </div>
                        </div>

                        {/* User Message */}
                        <div className="flex flex-col gap-2 max-w-[80%] ml-auto">
                            <div className="flex items-end gap-2 justify-end">
                                <div className="bg-primary p-4 rounded-2xl rounded-br-none shadow-md">
                                    <p className="text-sm text-white leading-relaxed">Where is my next class and what do I need to prepare?</p>
                                </div>
                            </div>
                            <span className="text-[10px] text-slate-500 text-right mr-1">10:42 AM</span>
                        </div>

                        {/* AI Message with RAG Citations */}
                        <div className="flex flex-col gap-3 max-w-[85%]">
                            <div className="flex items-end gap-2">
                                <div className="bg-white dark:bg-slate-800 p-4 rounded-2xl rounded-bl-none shadow-sm border border-slate-200 dark:border-slate-700">
                                    <p className="text-sm leading-relaxed mb-4">Your next class is <strong>CS101: Introduction to Programming</strong> at 2:00 PM in the <strong>Lovelace Building, Room 302</strong>.</p>
                                    <p className="text-sm leading-relaxed mb-4">According to the syllabus, you should have completed the &apos;Loops and Conditionals&apos; exercise and bring your laptop for the live coding session.</p>

                                    {/* Source Badges */}
                                    <div className="pt-3 border-t border-slate-100 dark:border-slate-700">
                                        <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Sources</p>
                                        <div className="flex flex-wrap gap-2">
                                            <div className="flex items-center gap-1.5 px-2 py-1 bg-primary/5 border border-primary/20 rounded-md text-[11px] font-medium text-primary">
                                                <span className="material-symbols-outlined text-xs">description</span>
                                                CS101 Syllabus
                                            </div>
                                            <div className="flex items-center gap-1.5 px-2 py-1 bg-primary/5 border border-primary/20 rounded-md text-[11px] font-medium text-primary">
                                                <span className="material-symbols-outlined text-xs">calendar_month</span>
                                                Personal Schedule
                                            </div>
                                            <div className="flex items-center gap-1.5 px-2 py-1 bg-primary/5 border border-primary/20 rounded-md text-[11px] font-medium text-primary">
                                                <span className="material-symbols-outlined text-xs">map</span>
                                                Campus Map
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Input Area (Moved down for structure) */}
                        <div className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 mt-auto absolute bottom-0 w-full lg:w-[calc(100%-20rem-16rem)] max-w-4xl mx-auto flex items-center gap-2" style={{ position: 'relative', width: '100%', maxWidth: 'none', borderTop: 'none', background: 'transparent', padding: '0' }}>
                            <div className="w-full relative mt-4">
                                <div className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 w-full">
                                    <div className="max-w-4xl mx-auto flex items-center gap-2">
                                        <button className="p-2 text-slate-400 hover:text-primary transition-colors flex items-center justify-center">
                                            <span className="material-symbols-outlined">attach_file</span>
                                        </button>
                                        <div className="relative flex-1">
                                            <input className="w-full bg-slate-100 dark:bg-slate-800 border-none rounded-xl py-3 px-4 text-sm focus:ring-2 focus:ring-primary transition-all text-slate-900 dark:text-slate-100 placeholder:text-slate-500" placeholder="Ask about your schedule, campus, or professors..." type="text" />
                                        </div>
                                        <button className="bg-primary text-white p-3 rounded-xl hover:bg-primary/90 transition-all flex items-center justify-center shadow-lg shadow-primary/20">
                                            <span className="material-symbols-outlined">send</span>
                                        </button>
                                    </div>
                                    <p className="text-center text-[10px] text-slate-400 mt-3">CampusBot may provide incorrect info. Always verify important dates with your official university portal.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Right Sidebar (Mobile / Tablet Hidden) - Recent Activity/Links */}
                <aside className="hidden xl:flex flex-col w-64 border-l border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6">
                    <h3 className="text-slate-900 dark:text-slate-100 text-sm font-bold uppercase tracking-wider mb-4">Resources</h3>
                    <div className="space-y-4">
                        <a className="flex items-center gap-3 group" href="#">
                            <div className="size-8 rounded bg-primary/5 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                                <span className="material-symbols-outlined text-sm">link</span>
                            </div>
                            <span className="text-xs font-medium text-slate-600 dark:text-slate-400">Student Portal</span>
                        </a>
                        <a className="flex items-center gap-3 group" href="#">
                            <div className="size-8 rounded bg-primary/5 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                                <span className="material-symbols-outlined text-sm">mail</span>
                            </div>
                            <span className="text-xs font-medium text-slate-600 dark:text-slate-400">University Email</span>
                        </a>
                        <a className="flex items-center gap-3 group" href="#">
                            <div className="size-8 rounded bg-primary/5 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                                <span className="material-symbols-outlined text-sm">folder</span>
                            </div>
                            <span className="text-xs font-medium text-slate-600 dark:text-slate-400">Shared Drive</span>
                        </a>
                    </div>
                    <div className="mt-10">
                        <h3 className="text-slate-900 dark:text-slate-100 text-sm font-bold uppercase tracking-wider mb-4">Quick Map</h3>
                        <div className="aspect-square bg-slate-100 dark:bg-slate-800 rounded-lg overflow-hidden border border-slate-200 dark:border-slate-700 flex items-center justify-center group relative">
                            {/* eslint-disable-next-line @next/next/no-img-element */}
                            <img alt="Campus Map Preview" className="w-full h-full object-cover" data-alt="Stylized minimalist map of university campus buildings" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCQ2j1WvQq9PyT1jeliijYEbtWf7JHBMudxy3-ccPYJAovDIve-YF_Vwmr0nYOepkfjI-TH-niZbgxacqS2usuVbaPsuyBHbkgGbWWLOAWAXmCiUtrQA95WyXVJLGf4ZWf-GjYcgeal4-FLcoLLNMQ1ws1BHv2yvlgJfcqieaC38XCz1q9XCz6BXg9DVDdfW1Ib4wvMhnMm9-M_mtWpdpLGs6UGFKIUriw8g1hii2uCojDpVMbrECXcQcYatPfKPGbsnu9e6NJ-5hE" />
                            <div className="absolute inset-0 bg-primary/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                <button className="bg-white text-primary px-3 py-1.5 rounded-full text-[10px] font-bold shadow-xl">Open Full Map</button>
                            </div>
                        </div>
                    </div>
                </aside>
            </main>
        </div>
    );
}
