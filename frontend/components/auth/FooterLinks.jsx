import React from 'react';
import Link from 'next/link';

export default function FooterLinks() {
    return (
        <div className="mt-8 pt-6 border-t border-slate-100 dark:border-slate-800 text-center">
            <p className="text-slate-500 dark:text-slate-400 text-xs">
                Don't have an account?
                <Link className="text-primary font-bold hover:underline ml-1" href="/auth/register">Register here</Link>
            </p>
        </div>
    );
}
