import React from 'react';

export default function InputField({
    id,
    name,
    type,
    label,
    placeholder,
    icon,
    value,
    onChange,
    required = false,
    rightElement = null
}) {
    return (
        <div className="space-y-2">
            <div className="flex items-center justify-between">
                <label className="text-slate-700 dark:text-slate-300 text-sm font-medium" htmlFor={id}>
                    {label}
                </label>
                {rightElement && rightElement}
            </div>
            <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xl">
                    {icon}
                </span>
                <input
                    className="w-full pl-10 pr-10 py-3 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-primary focus:border-transparent transition-all placeholder:text-slate-400"
                    id={id}
                    name={name}
                    placeholder={placeholder}
                    required={required}
                    type={type}
                    value={value}
                    onChange={onChange}
                />
            </div>
        </div>
    );
}
