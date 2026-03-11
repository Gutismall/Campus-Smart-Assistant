"use client";
import React, { useState, useEffect } from 'react';

const tablesConfig = {
    users: {
        id: 'users',
        endpoint: '/api/data/users',
        label: 'Users Table',
        icon: 'group',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'email', label: 'Email', type: 'email', required: true },
            { name: 'id_number', label: 'ID Number', type: 'text', required: true },
            { name: 'password', label: 'Password (Create/Update)', type: 'text' },
            { name: 'is_system_admin', label: 'Is Admin', type: 'select', options: ['true', 'false'], required: true },
        ]
    },
    campuses: {
        id: 'campuses',
        endpoint: '/api/data/campuses',
        label: 'Campuses',
        icon: 'domain',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'name', label: 'Name', type: 'text', required: true },
            { name: 'address_details', label: 'Address Details', type: 'text' }
        ]
    },
    divisions: {
        id: 'divisions',
        endpoint: '/api/data/divisions',
        label: 'Divisions',
        icon: 'account_tree',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'name', label: 'Name', type: 'text', required: true },
            { name: 'campus_id', label: 'Campus ID', type: 'number', required: true }
        ]
    },
    buildings: {
        id: 'buildings',
        endpoint: '/api/data/buildings',
        label: 'Buildings',
        icon: 'apartment',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'name', label: 'Name', type: 'text', required: true },
            { name: 'campus_id', label: 'Campus ID', type: 'number', required: true }
        ]
    },
    rooms: {
        id: 'rooms',
        endpoint: '/api/data/rooms',
        label: 'Rooms',
        icon: 'meeting_room',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'building_id', label: 'Building ID', type: 'number', required: true },
            { name: 'room_number', label: 'Room Number', type: 'text', required: true },
            { name: 'capacity', label: 'Capacity', type: 'number' },
            { name: 'room_type', label: 'Type', type: 'text' }
        ]
    },
    students: {
        id: 'students',
        endpoint: '/api/data/students',
        label: 'Students',
        icon: 'school',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'user_id', label: 'User ID', type: 'number', required: true },
            { name: 'division_id', label: 'Division ID', type: 'number', required: true },
            { name: 'enrollment_year', label: 'Enrollment Year', type: 'number', required: true }
        ]
    },
    lecturers: {
        id: 'lecturers',
        endpoint: '/api/data/lecturers',
        label: 'Lecturers',
        icon: 'person_presentation',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'user_id', label: 'User ID', type: 'number', required: true },
            { name: 'title', label: 'Title', type: 'text' },
            { name: 'office_hours', label: 'Office Hours', type: 'text' }
        ]
    },
    tests: {
        id: 'tests',
        endpoint: '/api/data/tests',
        label: 'Tests',
        icon: 'assignment',
        fields: [
            { name: 'id', label: 'ID', type: 'text', readOnly: true },
            { name: 'course_name', label: 'Course Name', type: 'text', required: true },
            { name: 'date_time', label: 'Date/Time (ISO)', type: 'text', required: true },
            { name: 'room_id', label: 'Room ID', type: 'number' },
            { name: 'lecturer_id', label: 'Lecturer ID', type: 'number' }
        ]
    }
};

export default function TableManager() {
    const [activeTableId, setActiveTableId] = useState('users');
    const [tableData, setTableData] = useState([]);
    const [editingRecord, setEditingRecord] = useState(null);
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState(null);

    const activeTable = tablesConfig[activeTableId];

    const getAuthHeaders = () => {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    };

    const fetchTableData = async () => {
        setLoading(true);
        setErrorMsg(null);
        try {
            const url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${url}${activeTable.endpoint}`, {
                headers: getAuthHeaders()
            });
            if (!res.ok) throw new Error('Failed to fetch data');
            const data = await res.json();
            setTableData(data);
        } catch (err) {
            console.error(err);
            setErrorMsg(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTableData();
    }, [activeTableId]);

    const handleSelectTable = (e) => {
        setActiveTableId(e.target.value);
        setEditingRecord(null); // Reset form when moving tables
    };

    const handleEdit = (record) => {
        setEditingRecord(record);
    };

    const handleCreateNew = () => {
        const newRecord = {};
        activeTable.fields.forEach(field => {
            newRecord[field.name] = field.type === 'number' ? 0 : '';
        });
        setEditingRecord(newRecord);
    };

    const handleDelete = async (id) => {
        if (!confirm('Are you sure you want to delete this record?')) return;
        try {
            const url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${url}${activeTable.endpoint}/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders()
            });
            if (!res.ok) throw new Error('Failed to delete');
            setTableData(prev => prev.filter(r => r.id !== id));
            if (editingRecord?.id === id) setEditingRecord(null);
        } catch(err) {
            alert('Error deleting record: ' + err.message);
        }
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const payload = {};
        
        activeTable.fields.forEach(field => {
            if (!field.readOnly) {
                let val = formData.get(field.name);
                if (val !== null && val !== '') {
                    if (field.type === 'number') val = Number(val);
                    if (val === 'true') val = true;
                    if (val === 'false') val = false;
                    payload[field.name] = val;
                }
            }
        });

        const isCreate = !editingRecord?.id;
        const method = isCreate ? 'POST' : 'PUT';
        const urlSuffix = isCreate ? '' : `/${editingRecord.id}`;
        
        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${baseUrl}${activeTable.endpoint}${urlSuffix}`, {
                method,
                headers: getAuthHeaders(),
                body: JSON.stringify(payload)
            });
            
            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Failed to save');
            }
            
            const savedRecord = await res.json();
            
            if (isCreate) {
                setTableData(prev => [...prev, savedRecord]);
            } else {
                setTableData(prev => prev.map(r => r.id === savedRecord.id ? savedRecord : r));
            }
            setEditingRecord(null);
        } catch (err) {
            alert('Error saving record: ' + err.message);
        }
    };

    return (
        <div className="w-full flex-col flex gap-8 pb-10">
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex flex-col">
                <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-primary">dynamic_form</span>
                        <h3 className="font-bold text-slate-900 dark:text-slate-100">Database Manager</h3>
                    </div>
                    
                    <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                        <select 
                            className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-sm font-medium text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-primary/20 appearance-none"
                            value={activeTableId} 
                            onChange={handleSelectTable}
                        >
                            {Object.values(tablesConfig).map(table => (
                                <option key={table.id} value={table.id}>{table.label}</option>
                            ))}
                        </select>
                        <button onClick={handleCreateNew} className="px-3 py-1.5 bg-primary text-white text-xs font-bold rounded-lg hover:bg-primary/90 flex justify-center items-center gap-1 shadow-sm transition-colors">
                            <span className="material-symbols-outlined text-sm">add</span> New Record
                        </button>
                    </div>
                </div>

                <div className="overflow-x-auto min-h-[150px] relative">
                    {loading && <div className="absolute inset-0 bg-white/50 flex items-center justify-center z-10 font-bold text-slate-500">Loading...</div>}
                    {errorMsg && <div className="absolute inset-x-0 top-0 p-4 bg-red-50 text-red-600 text-center z-10 text-sm font-bold">{errorMsg}</div>}
                    <table className="w-full text-left bg-transparent">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/30 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider font-semibold border-b border-slate-100 dark:border-slate-800">
                                {activeTable.fields.map(field => (
                                    <th key={field.name} className="px-6 py-4">{field.label}</th>
                                ))}
                                <th className="px-6 py-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {tableData.length > 0 ? (
                                tableData.map((record) => (
                                    <tr key={record.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                                        {activeTable.fields.map(field => (
                                            <td key={field.name} className="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-200 truncate max-w-[200px]">
                                                {String(record[field.name] ?? '')}
                                            </td>
                                        ))}
                                        <td className="px-6 py-4 text-right whitespace-nowrap">
                                            <div className="flex justify-end gap-2">
                                                <button onClick={() => handleEdit(record)} title="Edit Record" className="p-1.5 rounded-md hover:bg-primary/10 text-primary transition-colors inline-flex bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                                                    <span className="material-symbols-outlined text-[18px]">edit</span>
                                                </button>
                                                <button onClick={() => handleDelete(record.id)} title="Delete Record" className="p-1.5 rounded-md hover:bg-red-500/10 text-red-500 transition-colors inline-flex bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                                                    <span className="material-symbols-outlined text-[18px]">delete</span>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={activeTable.fields.length + 1} className="px-6 py-8 text-center text-slate-500 dark:text-slate-400">
                                        {loading ? '' : `No records found in ${activeTable.label}.`}
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {editingRecord && (
                <div className="bg-white dark:bg-slate-900 rounded-xl border border-primary/30 shadow-md shadow-primary/5 overflow-hidden ring-1 ring-primary/10 transition-all animate-in fade-in slide-in-from-top-4 duration-300">
                    <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <span className="material-symbols-outlined text-primary">
                                {editingRecord.id ? 'edit_document' : 'note_add'}
                            </span>
                            <h3 className="font-bold text-slate-900 dark:text-slate-100">
                                {editingRecord.id ? `Edit ${activeTable.label} Record` : `Create New ${activeTable.label} Record`}
                            </h3>
                        </div>
                        <button onClick={() => setEditingRecord(null)} className="text-slate-400 hover:text-red-500 transition-colors flex">
                            <span className="material-symbols-outlined">close</span>
                        </button>
                    </div>
                    <div className="p-6">
                        <form onSubmit={handleFormSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {activeTable.fields.map(field => {
                                const isIdFieldNew = field.name === 'id' && !editingRecord.id;
                                const isReadOnly = field.readOnly;
                                if (isIdFieldNew) return null;

                                let defaultVal = editingRecord[field.name];
                                if (field.type === 'select' && typeof defaultVal === 'boolean') {
                                    defaultVal = defaultVal ? 'true' : 'false';
                                }

                                return (
                                    <div key={field.name} className="flex flex-col gap-1.5">
                                        <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1">
                                            {field.label} {field.required && <span className="text-red-500" title="Required">*</span>}
                                        </label>
                                        
                                        {field.type === 'select' ? (
                                            <select 
                                                name={field.name}
                                                required={field.required}
                                                defaultValue={defaultVal || ''}
                                                className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 text-slate-900 dark:text-slate-100"
                                            >
                                                <option value="" disabled>Select {field.label}</option>
                                                {field.options.map(opt => (
                                                    <option key={opt} value={opt} className="capitalize">{opt}</option>
                                                ))}
                                            </select>
                                        ) : (
                                            <input 
                                                type={field.type === 'number' ? 'number' : field.type === 'email' ? 'email' : 'text'}
                                                name={field.name}
                                                readOnly={isReadOnly}
                                                required={field.required}
                                                defaultValue={defaultVal || ''}
                                                className={`w-full border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 text-slate-900 dark:text-slate-100 overflow-hidden ${isReadOnly ? 'border-transparent opacity-60 cursor-not-allowed bg-slate-100 dark:bg-slate-800/50' : 'bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700'}`}
                                                placeholder={`Enter ${field.label.toLowerCase()}`}
                                            />
                                        )}
                                    </div>
                                );
                            })}
                            
                            <div className="md:col-span-2 flex justify-end gap-3 mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
                                <button type="button" onClick={() => setEditingRecord(null)} className="px-4 py-2 rounded-lg text-sm font-bold text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                                    Cancel
                                </button>
                                <button type="submit" className="px-4 py-2 rounded-lg text-sm font-bold text-white bg-primary hover:bg-primary/90 shadow-md shadow-primary/20 transition-all flex items-center gap-2">
                                    <span className="material-symbols-outlined text-[18px]">save</span>
                                    {editingRecord.id ? 'Save Changes' : 'Create Record'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
