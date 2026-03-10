import React from 'react';

export default function UniversityHeader() {
    return (
        <div className="h-40 w-full relative">
            <div className="absolute inset-0 bg-gradient-to-br from-primary to-blue-600 opacity-90" data-alt="Abstract university campus silhouette in blue gradient"></div>
            <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-white text-center">
                    <span className="material-symbols-outlined text-5xl mb-1">school</span>
                    <p className="font-semibold uppercase tracking-widest text-xs opacity-80">University Login</p>
                </div>
            </div>
        </div>
    );
}
