'use client'
import { use } from 'react';
import { create } from 'zustand';

type ThemeState = {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
};

export const useThemeStore = create<ThemeState>((set) => ({
  theme: 'light',
  toggleTheme: () =>
    set((state) => {
      const newTheme = state.theme === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', newTheme);
      return { theme: newTheme };
    }),
}));
