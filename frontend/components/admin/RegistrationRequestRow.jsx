import React from 'react';

export default function RegistrationRequestRow({ request, onApprove, onReject }) {
    // Generate initials based on the student's name
    const initials = request.name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .substring(0, 2);

    return (
        <tr className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4">
                <div className="flex items-center gap-3">
                    {/* Generates a simple avatar with initials */}
                    <div className="size-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-400 font-bold">
                        {initials}
                    </div>
                    <div>
                        <div className="text-sm font-semibold text-slate-900 dark:text-slate-100">{request.name}</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">{request.email}</div>
                    </div>
                </div>
            </td>
            <td className="px-6 py-4 text-sm font-medium text-slate-600 dark:text-slate-300">{request.studentId}</td>
            <td className="px-6 py-4 text-right">
                <div className="flex justify-end gap-2">
                    <button 
                        onClick={() => onApprove(request.id)}
                        className="px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-bold hover:bg-primary/90 transition-all flex items-center gap-1"
                    >
                        <span className="material-symbols-outlined text-sm">check</span> Approve
                    </button>
                    <button 
                        onClick={() => onReject(request.id)}
                        className="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-xs font-bold hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-all"
                    >
                        Reject
                    </button>
                </div>
            </td>
        </tr>
    );
}
