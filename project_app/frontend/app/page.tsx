"use client";

import { useState } from "react";

type SimulationInput = {
  y0: number;
  mu: number;
  sigma: number;
  T: number;
  N: number;
};

type SimulationResult = {
  received?: SimulationInput;
  [key: string]: any;
};

export default function Home() {
  const [form, setForm] = useState<SimulationInput>({
    y0: 1.0,
    mu: 0.05,
    sigma: 0.2,
    T: 1.0,
    N: 100,
  });

  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (key: keyof SimulationInput, value: string) => {
    setForm({ ...form, [key]: Number(value) });
  };

  const runSimulation = async () => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const res = await fetch("http://127.0.0.1:8000/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error(await res.text());

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-gray-200 text-gray-900 font-sans p-6">
      <h1 className="text-4xl font-bold mb-8 text-gray-900">PyGBM Simulation</h1>

      <div className="grid grid-cols-2 gap-6 w-full max-w-lg bg-white p-8 rounded-2xl shadow-md border border-gray-200">
        {Object.entries(form).map(([key, value]) => (
          <label key={key} className="flex flex-col text-gray-700 font-medium">
            <span className="mb-2 capitalize">{key}</span>
            <input
              type="number"
              step="any"
              value={value}
              onChange={(e) => handleChange(key as keyof SimulationInput, e.target.value)}
              className="border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-lg p-3 text-gray-900 text-base bg-gray-50 transition"
            />
          </label>
        ))}
      </div>

      <button
        onClick={runSimulation}
        disabled={loading}
        className="mt-8 rounded-full bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg font-semibold shadow-md transition disabled:opacity-60"
      >
        {loading ? "Running..." : "Run Simulation"}
      </button>

      {error && <p className="mt-4 text-red-600 font-semibold">{error}</p>}

      {result && (
        <pre className="mt-8 p-6 bg-gray-100 border border-gray-300 rounded-xl text-sm text-left overflow-x-auto w-full max-w-3xl shadow-inner">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  );
}
