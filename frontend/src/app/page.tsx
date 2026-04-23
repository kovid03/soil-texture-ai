"use client";

import React, { useState, useRef, useCallback } from "react";
import {
  UploadCloud,
  CheckCircle,
  RefreshCw,
  Sprout,
  AlertCircle,
  Image as ImageIcon,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [lang, setLang] = useState<"en" | "hi">("en");
  const [dragActive, setDragActive] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const texts = {
    en: {
      title: "Soil Texture AI",
      subtitle:
        "Upload a soil image to discover its classification and recommendations.",
      uploadText: "Drag & drop your soil image here",
      orClick: "or click to browse",
      predictBtn: "Analyze Soil",
      analyzing: "Analyzing...",
      results: "Analysis Results",
      confidence: "Confidence",
      crops: "Recommended Crops",
      fertilizers: "Recommended Fertilizers",
      gradcam: "AI Focus Area (Grad-CAM)",
      reset: "Analyze Another",
      unknown: "Unknown",
      soilType: "Soil Type",
    },
    hi: {
      title: "मिट्टी की बनावट एआई",
      subtitle:
        "मिट्टी का वर्गीकरण और सिफारिशें जानने के लिए एक तस्वीर अपलोड करें।",
      uploadText: "अपनी मिट्टी की तस्वीर यहाँ खींचें और छोड़ें",
      orClick: "या ब्राउज़ करने के लिए क्लिक करें",
      predictBtn: "मिट्टी का विश्लेषण करें",
      analyzing: "विश्लेषण हो रहा है...",
      results: "विश्लेषण के परिणाम",
      confidence: "आत्मविश्वास",
      crops: "अनुशंसित फसलें",
      fertilizers: "अनुशंसित उर्वरक",
      gradcam: "एआई फोकस क्षेत्र (Grad-CAM)",
      reset: "एक और विश्लेषण करें",
      unknown: "अज्ञात",
      soilType: "मिट्टी का प्रकार",
    },
  };

  const t = texts[lang];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
      setError(null);
    }
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      setFile(droppedFile);
      setPreview(URL.createObjectURL(droppedFile));
      setResult(null);
      setError(null);
    }
  }, []);

  const handlePredict = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to get prediction from server (HTTP " + res.status + ")");
      }

      const data = await res.json();
      if (data.error) {
        throw new Error(data.error);
      }
      setResult(data);
    } catch (err: any) {
      if (err.message?.includes("fetch") || err.name === "TypeError") {
        setError("Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000");
      } else {
        setError(err.message || "An unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="min-h-screen flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-slate-900 text-white">
      {/* Background blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-600/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-amber-600/20 blur-[120px] pointer-events-none" />
      <div className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-[30%] h-[30%] rounded-full bg-teal-500/10 blur-[100px] pointer-events-none" />

      <div className="w-full max-w-5xl z-10">
        {/* Header */}
        <header className="flex justify-between items-center mb-10">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-emerald-400 to-green-600 rounded-xl shadow-lg shadow-emerald-900/40">
              <Sprout className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-200">
              {t.title}
            </h1>
          </div>
          <button
            onClick={() => setLang(lang === "en" ? "hi" : "en")}
            className="px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/10 transition-all font-medium text-sm"
          >
            {lang === "en" ? "हिंदी" : "English"}
          </button>
        </header>

        {/* Subtitle */}
        <div className="text-center mb-10">
          <p className="text-lg text-slate-300 max-w-2xl mx-auto">
            {t.subtitle}
          </p>
        </div>

        <main>
          {/* ───── No result yet: full-width upload ───── */}
          {!result && (
            <div className="max-w-2xl mx-auto">
              {/* Dropzone */}
              <div
                className={`rounded-2xl p-10 text-center border-2 border-dashed transition-all cursor-pointer flex flex-col items-center justify-center min-h-[340px] relative group
                  bg-white/5 backdrop-blur-md shadow-xl
                  ${dragActive ? "border-emerald-400 bg-emerald-900/20" : ""}
                  ${file ? "border-emerald-500/50" : "border-slate-600"}
                  hover:border-emerald-400/80`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept="image/*"
                  className="hidden"
                />

                <AnimatePresence mode="wait">
                  {preview ? (
                    <motion.div
                      key="preview"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0 }}
                      className="w-full flex flex-col items-center gap-4"
                    >
                      <div className="w-56 h-56 rounded-xl overflow-hidden shadow-lg border border-slate-700">
                        <img
                          src={preview}
                          alt="Uploaded soil preview"
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <p className="text-sm text-slate-400 flex items-center gap-1">
                        <RefreshCw className="w-3.5 h-3.5" /> Click to change
                        image
                      </p>
                    </motion.div>
                  ) : (
                    <motion.div
                      key="upload"
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="flex flex-col items-center gap-5"
                    >
                      <div className="p-5 bg-slate-800/60 rounded-full ring-1 ring-slate-700">
                        <UploadCloud className="w-14 h-14 text-emerald-400" />
                      </div>
                      <div>
                        <p className="text-xl font-semibold text-slate-100">
                          {t.uploadText}
                        </p>
                        <p className="text-sm text-slate-400 mt-1">
                          {t.orClick}
                        </p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Analyze Button */}
              {file && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-6 flex justify-center"
                >
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePredict();
                    }}
                    disabled={loading}
                    className="flex items-center gap-2 px-10 py-4 bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-white rounded-full font-bold text-lg shadow-lg shadow-emerald-900/50 transition-all hover:scale-105 disabled:opacity-70 disabled:hover:scale-100 disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <>
                        <RefreshCw className="w-5 h-5 animate-spin" />{" "}
                        {t.analyzing}
                      </>
                    ) : (
                      <>
                        <CheckCircle className="w-5 h-5" /> {t.predictBtn}
                      </>
                    )}
                  </button>
                </motion.div>
              )}

              {/* Error */}
              {error && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-4 p-4 bg-red-900/40 border border-red-500/50 rounded-xl flex items-start gap-3 text-red-200"
                >
                  <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                  <p className="text-sm">{error}</p>
                </motion.div>
              )}
            </div>
          )}

          {/* ───── Results layout: side-by-side ───── */}
          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="grid grid-cols-1 md:grid-cols-12 gap-8"
              >
                {/* Left: uploaded image */}
                <div className="md:col-span-5">
                  <div className="rounded-2xl bg-white/5 backdrop-blur-md border border-white/10 shadow-xl p-6 flex flex-col items-center gap-4">
                    {preview && (
                      <div className="w-full max-w-xs rounded-xl overflow-hidden shadow-lg border border-slate-700">
                        <img
                          src={preview}
                          alt="Uploaded soil"
                          className="w-full h-auto object-cover"
                        />
                      </div>
                    )}

                    {result.gradcam_image && (
                      <div className="w-full max-w-xs">
                        <h3 className="font-semibold text-base mb-2 flex items-center gap-2 text-purple-300">
                          <ImageIcon className="w-4 h-4" /> {t.gradcam}
                        </h3>
                        <div className="rounded-xl overflow-hidden border border-slate-700">
                          <img
                            src={`data:image/jpeg;base64,${result.gradcam_image}`}
                            alt="Grad-CAM heatmap"
                            className="w-full h-auto"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Right: results */}
                <div className="md:col-span-7 space-y-6">
                  <div className="rounded-2xl bg-white/5 backdrop-blur-md border border-white/10 shadow-xl p-6">
                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                      <SparklesIcon className="w-6 h-6 text-emerald-400" />
                      {t.results}
                    </h2>

                    {/* Soil type & confidence cards */}
                    <div className="flex flex-col sm:flex-row gap-4 mb-8">
                      <div className="flex-1 bg-slate-800/50 border border-slate-700/50 rounded-2xl p-5 text-center">
                        <p className="text-xs text-slate-400 uppercase tracking-widest mb-2">
                          {t.soilType}
                        </p>
                        <p className="text-3xl font-extrabold text-white">
                          {result.soil_type || t.unknown}
                        </p>
                      </div>
                      <div className="flex-1 bg-slate-800/50 border border-slate-700/50 rounded-2xl p-5 text-center">
                        <p className="text-xs text-slate-400 uppercase tracking-widest mb-2">
                          {t.confidence}
                        </p>
                        <p className="text-3xl font-extrabold text-emerald-400">
                          {(result.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>

                    {/* Recommendations */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                      <div className="space-y-3">
                        <h3 className="font-semibold text-lg flex items-center gap-2 text-amber-300">
                          <Sprout className="w-5 h-5" /> {t.crops}
                        </h3>
                        <ul className="space-y-2">
                          {result.recommendations?.crops?.map(
                            (crop: string, idx: number) => (
                              <li
                                key={idx}
                                className="flex items-center gap-2 text-slate-300 bg-slate-800/30 px-3 py-2 rounded-lg"
                              >
                                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0" />
                                {crop}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                      <div className="space-y-3">
                        <h3 className="font-semibold text-lg flex items-center gap-2 text-cyan-300">
                          <span className="w-5 h-5 flex items-center justify-center border-2 border-cyan-300 rounded-full text-[10px] font-bold leading-none">
                            N
                          </span>
                          {t.fertilizers}
                        </h3>
                        <ul className="space-y-2">
                          {result.recommendations?.fertilizers?.map(
                            (fert: string, idx: number) => (
                              <li
                                key={idx}
                                className="flex items-center gap-2 text-slate-300 bg-slate-800/30 px-3 py-2 rounded-lg"
                              >
                                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0" />
                                {fert}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    </div>
                  </div>

                  {/* Reset button */}
                  <div className="flex justify-end">
                    <button
                      onClick={handleReset}
                      className="px-6 py-3 text-slate-300 hover:text-white bg-slate-800/50 hover:bg-slate-700/50 rounded-full transition-colors font-medium flex items-center gap-2"
                    >
                      <RefreshCw className="w-4 h-4" /> {t.reset}
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

function SparklesIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
      <path d="M5 3v4" />
      <path d="M19 17v4" />
      <path d="M3 5h4" />
      <path d="M17 19h4" />
    </svg>
  );
}
