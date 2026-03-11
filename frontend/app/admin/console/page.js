"use client";
import React, { useState, useEffect } from 'react';
import Header from '../../../components/Header';
import RegistrationRequestRow from '../../../components/admin/RegistrationRequestRow';
import TableManager from '../../../components/admin/TableManager';

export default function AdminConsole() {
    const [requests, setRequests] = useState([]);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    };

    useEffect(() => {
        const fetchRequests = async () => {
            try {
                const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                const res = await fetch(`${API_URL}/api/user/requests`, { headers: getAuthHeaders() });
                if (res.ok) {
                    const users = await res.json();
                    // Just filter non-admin users to show as pending requests for demonstration
                    const studentUsers = users.filter(u => !u.is_system_admin).map(u => ({
                        id: u.id,
                        name: u.email.split('@')[0], // derived name
                        email: u.email,
                        studentId: u.id_number
                    }));
                    setRequests(studentUsers);
                }
            } catch (err) {
                console.error("Failed fetching pending registrations:", err);
            }
        };
        fetchRequests();
    }, []);

    const handleApprove = async (id) => {
        console.log(`Approved student request ${id}`);
        setRequests(prev => prev.filter(req => req.id !== id));
    };

    const handleReject = async (id) => {
        console.log(`Rejected student request ${id}`);
        setRequests(prev => prev.filter(req => req.id !== id));
    };

    return (
        <div className="bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 antialiased min-h-screen font-display">
            <div className="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden">
                <Header navItems={[
                    { label: 'Chat', href: '/' }
                ]} />

                <div className="flex flex-1 flex-col lg:flex-row">

                    {/* Main Content Area */}
                    <main className="flex-1 p-6 md:p-10 bg-background-light dark:bg-background-dark max-w-7xl mx-auto w-full">
                        <div className="mb-8">
                            <h1 className="text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">Admin Console</h1>
                            <p className="text-slate-500 dark:text-slate-400 mt-1">Review pending applications and manage institutional data points.</p>
                        </div>
                        <div className="flex flex-col gap-8 w-full max-w-5xl mx-auto">
                            {/* Section 1: Student Registration Requests */}
                            <div className="w-full flex flex-col gap-6">
                                <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
                                    <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-800/50">
                                        <div className="flex items-center gap-2">
                                            <span className="material-symbols-outlined text-primary">how_to_reg</span>
                                            <h3 className="font-bold text-slate-900 dark:text-slate-100">Pending Student Registrations</h3>
                                        </div>
                                        {requests.length > 0 && (
                                            <span className="bg-primary/10 text-primary text-xs font-bold px-2.5 py-1 rounded-full">
                                                {requests.length} New
                                            </span>
                                        )}
                                    </div>
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-left bg-transparent">
                                            <thead>
                                                <tr className="bg-slate-50 dark:bg-slate-800/30 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider font-semibold">
                                                    <th className="px-6 py-4">Student Info</th>
                                                    <th className="px-6 py-4">Student ID</th>
                                                    <th className="px-6 py-4 text-right">Actions</th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                                                {requests.length > 0 ? (
                                                    requests.map((req) => (
                                                        <RegistrationRequestRow
                                                            key={req.id}
                                                            request={req}
                                                            onApprove={handleApprove}
                                                            onReject={handleReject}
                                                        />
                                                    ))
                                                ) : (
                                                    <tr>
                                                        <td colSpan="3" className="px-6 py-8 text-center text-slate-500 dark:text-slate-400">
                                                            No pending requests.
                                                        </td>
                                                    </tr>
                                                )}
                                            </tbody>
                                        </table>
                                    </div>
                                    <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/30 border-t border-slate-100 dark:border-slate-800">
                                        <button className="text-primary text-sm font-bold hover:underline">View all pending requests</button>
                                    </div>
                                </div>
                            </div>

                            {/* Section 2: Database Data Tables (Dynamic CRUD) */}
                            <div className="mt-4 border-t border-slate-200 dark:border-slate-800 pt-8" />
                            <TableManager />
                        </div>
                    </main>
                </div>
            </div>
        </div>
    );
}
