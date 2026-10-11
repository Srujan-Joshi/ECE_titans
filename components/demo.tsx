// components/demo.tsx
import React from "react";
import { Component } from "@/components/ui/globe";

export default function DemoOne() {
  return (
    <main className="min-h-screen w-full flex items-center justify-center p-4 bg-neutral-100 dark:bg-neutral-950 transition-colors duration-300">
      <Component />
    </main>
  );
}
