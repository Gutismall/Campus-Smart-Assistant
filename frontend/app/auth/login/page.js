"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Logo from '../../../components/auth/Logo';
import InputField from '../../../components/auth/InputField';

export default function LoginPage() {
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
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/auth/login`, {
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
        <div className="bg-background-light dark:bg-background-dark font-display antialiased min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md">

                {/* Brand Identity */}
                <div className="flex flex-col items-center mb-8">
                    <Logo />
                    <h1 className="text-slate-900 dark:text-slate-100 text-2xl font-bold tracking-tight">Campus Assistant</h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-2 text-sm">Welcome back to your university portal</p>
                </div>

                {/* Login Card */}
                <div className="bg-white dark:bg-slate-900 shadow-xl rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800">

                    {/* University Header */}
                    <div className="h-40 w-full relative">
                        <div className="absolute inset-0 bg-gradient-to-br from-primary to-blue-600 opacity-90" data-alt="Abstract university campus silhouette in blue gradient"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <div className="text-white text-center">
                                <span className="material-symbols-outlined text-5xl mb-1">school</span>
                                <p className="font-semibold uppercase tracking-widest text-xs opacity-80">University Login</p>
                            </div>
                        </div>
                    </div>

                    {/* Login Form */}
                    <div className="p-8">
                        {error && (
                            <div className="mb-6 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-3 rounded-lg text-sm font-medium border border-red-100 dark:border-red-800 flex items-center gap-2">
                                <span className="material-symbols-outlined text-sm">error</span>
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleLogin} className="space-y-6">
                            {/* Email Field */}
                            <InputField
                                id="email"
                                name="email"
                                type="email"
                                label="Email Address"
                                placeholder="name@university.edu"
                                icon="alternate_email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required={true}
                            />

                            {/* Password Field */}
                            <InputField
                                id="password"
                                name="password"
                                type="password"
                                label="Password"
                                placeholder="••••••••"
                                icon="lock"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required={true}
                                rightElement={
                                    <a className="text-primary text-xs font-medium hover:underline" href="#">Forgot?</a>
                                }
                            />

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

                        {/* Footer Links (was previously inside LoginForm) */}
                        <div className="mt-8 pt-6 border-t border-slate-100 dark:border-slate-800 text-center">
                            <p className="text-slate-500 dark:text-slate-400 text-xs">
                                Don't have an account?
                                <Link className="text-primary font-bold hover:underline ml-1" href="/auth/register">Register here</Link>
                            </p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}
