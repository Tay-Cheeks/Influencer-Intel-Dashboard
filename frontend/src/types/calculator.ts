export type CalculatorMode = "contextual" | "standalone";

export interface CalculatorInput {
  mode: CalculatorMode;

  // Currency
  clientCurrency: string;
  creatorCurrency: string;

  // Pricing
  quotedFee: number;
  agencyMarginPercent: number;

  // Views basis
  expectedViewsBasis: "median" | "average";

  // Optional creator-linked data (Mode 1)
  creatorId?: string;
  medianViews?: number;
  averageViews?: number;
}

export interface CalculatorResult {
  expectedViews: number;
  netCreatorFee: number;
  effectiveCPM: number;
  engagementAdjustedCPM?: number;
}
