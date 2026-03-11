"use client";
import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Header from '../components/Header';
import UserMessage from '../components/chat/UserMessage';
import SystemMessage from '../components/chat/SystemMessage';
import TypingIndicator from '../components/chat/TypingIndicator';

export default function LandingPage() {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userRole, setUserRole] = useState(null);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    // Initial state
    const [messages, setMessages] = useState([
        {
            role: 'system',
            content: ["Hello! I'm your Campus Assistant. I can help you with your schedule, find locations on campus, or look up information from your syllabi. How can I help you today?"]
        }
    ]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    const handleSendMessage = async (e) => {
        e?.preventDefault();
        if (!inputValue.trim() || isTyping) return;

        const currentInput = inputValue;
        const newUserMsg = {
            role: 'user',
            content: currentInput,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        setMessages(prev => [...prev, newUserMsg]);
        setInputValue('');
        setIsTyping(true);

        try {
            const token = localStorage.getItem('token');
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

            const response = await fetch(`${API_URL}/api/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message: currentInput })
            });

            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            const data = await response.json();

            const newSystemMsg = {
                role: 'system',
                content: [data.reply]
            };
            setMessages(prev => [...prev, newSystemMsg]);
        } catch (error) {
            console.error("Chat error:", error);
            setMessages(prev => [...prev, {
                role: 'system',
                content: ["Sorry, I encountered an error communicating with the server. Please try again later."]
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    useEffect(() => {
        const verifyAuth = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                router.push('/auth/login');
                return;
            }

            try {
                const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                const response = await fetch(`${API_URL}/api/auth/verify`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    setIsAuthenticated(true);
                    setUserRole(data.role || 'student'); // Default to student if no role is found
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
        <div className="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-slate-100 h-screen flex flex-col overflow-hidden">


            {/* Top Navigation Bar */}
            <Header
                navItems={
                    userRole === 'admin'
                        ? [
                            { label: 'System Settings', href: '/admin/console' }
                        ]
                        : []
                }
            />

            <main className="flex-1 flex p-4 md:p-8 max-w-5xl mx-auto w-full min-h-0">

                {/* Main Chat Area */}
                <section className="flex-1 flex flex-col bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl rounded-2xl md:rounded-[2rem] overflow-hidden min-h-0">
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
                    </div>

                    {/* Messages Area */}
                    <div className="flex-1 overflow-y-auto p-6 space-y-6">
                        {messages.map((msg, index) => (
                            msg.role === 'system' ? (
                                <SystemMessage
                                    key={index}
                                    messages={msg.content}
                                    sources={msg.sources}
                                />
                            ) : (
                                <UserMessage
                                    key={index}
                                    message={msg.content}
                                    time={msg.time}
                                />
                            )
                        ))}

                        {isTyping && <TypingIndicator />}
                        <div ref={messagesEndRef} />

                    </div> {/* End Messages Area */}

                    {/* Input Area (Pinned to bottom of the card) */}
                    <div className="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 p-4 w-full">
                        <div className="max-w-4xl mx-auto flex flex-col">
                            <form onSubmit={handleSendMessage} className="flex items-center gap-2">
                                <div className="relative flex-1">
                                    <input
                                        className="w-full bg-slate-100 dark:bg-slate-800 border-none rounded-xl py-3 px-4 text-sm focus:ring-2 focus:ring-primary transition-all text-slate-900 dark:text-slate-100 placeholder:text-slate-500"
                                        placeholder="Ask about your schedule, campus, or professors..."
                                        type="text"
                                        value={inputValue}
                                        onChange={(e) => setInputValue(e.target.value)}
                                        disabled={isTyping}
                                    />
                                </div>
                                <button type="submit" disabled={isTyping || !inputValue.trim()} className="disabled:opacity-50 bg-primary text-white p-3 rounded-xl hover:bg-primary/90 transition-all flex items-center justify-center shadow-lg shadow-primary/20">
                                    <span className="material-symbols-outlined">send</span>
                                </button>
                            </form>
                            <p className="text-center text-[10px] text-slate-400 mt-3">CampusBot may provide incorrect info. Always verify important dates with your official university portal.</p>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
