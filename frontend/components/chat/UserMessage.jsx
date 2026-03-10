import React from 'react';

export default function UserMessage({ message, time }) {
    return (
        <div className="flex flex-col gap-2 max-w-[80%] ml-auto">
            <div className="flex items-end gap-2 justify-end">
                <div className="bg-primary p-4 rounded-2xl rounded-br-none shadow-md">
                    <p className="text-sm text-white leading-relaxed">{message}</p>
                </div>
            </div>
            {time && (
                <span className="text-[10px] text-slate-500 text-right mr-1">{time}</span>
            )}
        </div>
    );
}
