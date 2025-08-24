import React from 'react';
import { colors, typography } from './designTokens';

interface PrimaryButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export function PrimaryButton({ children, ...props }: PrimaryButtonProps) {
  return (
    <button
      {...props}
      style={{
        backgroundColor: colors.primary,
        color: 'white',
        fontFamily: typography.body,
      }}
      className="px-4 py-2 rounded"
    >
      {children}
    </button>
  );
}
