import React from 'react';
import { typography, colors } from './designTokens';

interface PageHeadingProps {
  children: React.ReactNode;
}

export function PageHeading({ children }: PageHeadingProps) {
  return (
    <h1
      style={{ fontFamily: typography.heading, color: colors.primary }}
      className="text-2xl font-bold mb-4"
    >
      {children}
    </h1>
  );
}
