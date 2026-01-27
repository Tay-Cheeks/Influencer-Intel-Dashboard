"use client";

import { createContext, useContext, useMemo, useState } from "react";

export type AnalysisSummary = {
  id: string; // simple uuid later, for now can be Date.now().toString()
  channelId: string;
  channelName: string;
  channelUrl?: string;
  region?: string;
  subscribers?: number;
  medianViews?: number;
  averageViews?: number;
  createdAt: string; // ISO string
};

type AnalysisState = {
  activeId: string | null;
  byId: Record<string, AnalysisSummary>;
  recentIds: string[]; // most recent first
};

const AnalysisContext = createContext<{
  state: AnalysisState;
  upsertAnalysis: (a: AnalysisSummary) => void;
  setActive: (id: string) => void;
  getActive: () => AnalysisSummary | null;
}>({
  state: { activeId: null, byId: {}, recentIds: [] },
  upsertAnalysis: () => {},
  setActive: () => {},
  getActive: () => null,
});

export function AnalysisProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AnalysisState>({
    activeId: null,
    byId: {},
    recentIds: [],
  });

  const upsertAnalysis = (a: AnalysisSummary) => {
    setState((prev) => {
      const byId = { ...prev.byId, [a.id]: a };

      const nextRecent = [
        a.id,
        ...prev.recentIds.filter((x) => x !== a.id),
      ].slice(0, 5); // keep last 5 for MVP

      return {
        activeId: a.id,
        byId,
        recentIds: nextRecent,
      };
    });
  };

  const setActive = (id: string) => {
    setState((prev) => {
      if (!prev.byId[id]) return prev;
      const nextRecent = [id, ...prev.recentIds.filter((x) => x !== id)];
      return { ...prev, activeId: id, recentIds: nextRecent };
    });
  };

  const getActive = () => {
    const id = state.activeId;
    if (!id) return null;
    return state.byId[id] ?? null;
  };

  const value = useMemo(
    () => ({ state, upsertAnalysis, setActive, getActive }),
    [state],
  );

  return (
    <AnalysisContext.Provider value={value}>
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  return useContext(AnalysisContext);
}
