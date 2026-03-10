"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import FooterLinks from './FooterLinks';

export default function LoginForm() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.access_token);
                // Redirect to the dashboard/landing page after successful login
                router.push('/');
            } else {
                setError(data.detail || 'Invalid login credentials.');
            }
        } catch (err) {
            setError('Could not connect to the server. Please check your network.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8">
            {error && (
                <div className="mb-6 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-3 rounded-lg text-sm font-medium border border-red-100 dark:border-red-800 flex items-center gap-2">
                    <span className="material-symbols-outlined text-sm">error</span>
                    {error}
                </div>
            )}

            <form onSubmit={handleLogin} className="space-y-6">
                {/* Email Field */}
                <div className="space-y-2">
                    <label className="text-slate-700 dark:text-slate-300 text-sm font-medium" htmlFor="email">Email Address</label>
                    <div className="relative">
                        <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xl">alternate_email</span>
                        <input
                            className="w-full pl-10 pr-4 py-3 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-primary focus:border-transparent transition-all placeholder:text-slate-400"
                            id="email"
                            name="email"
                            placeholder="name@university.edu"
                            required
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                </div>

                {/* Password Field */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <label className="text-slate-700 dark:text-slate-300 text-sm font-medium" htmlFor="password">Password</label>
                        <a className="text-primary text-xs font-medium hover:underline" href="#">Forgot?</a>
                    </div>
                    <div className="relative">
                        <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xl">lock</span>
                        <input
                            className="w-full pl-10 pr-10 py-3 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-primary focus:border-transparent transition-all placeholder:text-slate-400"
                            id="password"
                            name="password"
                            placeholder="••••••••"
                            required
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                </div>

                {/* Log In Button */}
                <button
                    disabled={loading}
                    className={`w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 px-4 rounded-lg shadow-md transition-colors flex items-center justify-center gap-2 group ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                    type="submit"
                >
                    <span>{loading ? 'Logging In...' : 'Log In'}</span>
                    {!loading && <span className="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform">arrow_forward</span>}
                </button>
            </form>

            <FooterLinks />
        </div>
    );
}
