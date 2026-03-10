"use client";

import React from 'react';
import BrandIdentity from '../../../components/auth/BrandIdentity';
import UniversityHeader from '../../../components/auth/UniversityHeader';
import LoginForm from '../../../components/auth/LoginForm';
import SupportLinks from '../../../components/auth/SupportLinks';

export default function LoginPage() {
    return (
        <div className="bg-background-light dark:bg-background-dark font-display antialiased min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <BrandIdentity />

                {/* Login Card */}
                <div className="bg-white dark:bg-slate-900 shadow-xl rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800">
                    <UniversityHeader />
                    <LoginForm />
                </div>

                <SupportLinks />
            </div>
        </div>
    );
}
