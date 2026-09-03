import { useState, useRef } from "react";
import { uploadPDFs } from "../../services/api";
import { FiUploadCloud, FiFileText, FiX, FiCheckCircle } from "react-icons/fi";

const UploadCard = ({ onAnalysisComplete }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFiles = (newFiles) => {
    const pdfs = Array.from(newFiles).filter((f) => f.type === "application/pdf");
    setFiles((prev) => [...prev, ...pdfs]);
  };

  const handleChange = (e) => handleFiles(e.target.files);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === "dragenter" || e.type === "dragover");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files) handleFiles(e.dataTransfer.files);
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (!files.length) return;

    try {
      setLoading(true);
      setProgress(10);

      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) return prev;
          return prev + 5;
        });
      }, 300);

      const result = await uploadPDFs(files);

      clearInterval(interval);
      setProgress(100);

      setTimeout(() => {
        onAnalysisComplete(result);
        setLoading(false);
        setProgress(0);
      }, 500);

    } catch (err) {
      alert("Analysis failed.");
      setLoading(false);
      setProgress(0);
    }
  };

  return (
    <div className="w-full h-full group">
      <div
        className={`relative h-full bg-[#0B0F1A]/80 backdrop-blur-2xl border rounded-[2.5rem] p-10 overflow-hidden transition-all duration-500 ease-out shadow-[0_20px_50px_rgba(0,0,0,0.5)]
        ${dragActive ? "border-indigo-500 ring-4 ring-indigo-500/10 scale-[1.02]" : "border-white/10 hover:border-white/20"}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {/* Decorative Neural Glow */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-600/10 blur-[100px] rounded-full group-hover:bg-indigo-600/20 transition-all duration-700" />

        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
        />

        {/* Action Header */}
        <div className="relative z-10 flex flex-col items-center text-center">
          <div className="relative mb-6">
            <div className={`p-6 rounded-3xl bg-gradient-to-br from-indigo-500/20 to-transparent border border-indigo-500/20 text-indigo-400 shadow-[0_0_20px_rgba(99,102,241,0.2)] transition-transform duration-500 ${loading ? 'animate-pulse scale-110' : 'group-hover:scale-110'}`}>
              <FiUploadCloud size={36} />
            </div>
            {/* Pulsing Outer Ring */}
            <div className={`absolute -inset-2 border border-indigo-500/30 rounded-[2rem] animate-ping opacity-20 ${!loading && 'hidden'}`} />
          </div>

          <h2 className="text-3xl font-black text-white tracking-tight mb-3">
            Contract <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-indigo-600">Intelligence.</span>
          </h2>

          <p className="text-slate-500 text-sm font-medium max-w-xs leading-relaxed">
            Upload PDF agreements to extract high-risk variables using our <span className="text-slate-300">CUAD Hybrid Engine.</span>
          </p>

          <button
            onClick={() => fileInputRef.current.click()}
            className="mt-6 px-6 py-2 rounded-full bg-white/5 border border-white/10 text-xs font-black uppercase tracking-widest text-indigo-400 hover:bg-white/10 hover:text-white transition-all duration-300"
          >
            Browse Workspace
          </button>
        </div>

        {/* File Preview Area */}
        <div className={`mt-10 space-y-3 transition-all duration-500 ${files.length > 0 ? 'opacity-100' : 'opacity-0 h-0'}`}>
          <div className="flex items-center justify-between mb-2">
             <span className="text-[10px] font-black text-slate-600 uppercase tracking-widest">Queue ({files.length})</span>
             {files.length > 0 && <button onClick={() => setFiles([])} className="text-[10px] text-red-500 font-bold hover:underline">Clear All</button>}
          </div>

          <div className="max-h-48 overflow-y-auto pr-2 space-y-2 custom-scrollbar">
            {files.map((file, idx) => (
              <div
                key={idx}
                className="group/file flex items-center justify-between bg-white/[0.02] border border-white/5 p-4 rounded-2xl hover:bg-white/[0.05] transition-all animate-in slide-in-from-left-4"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <div className="flex items-center gap-3 overflow-hidden">
                  <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                    <FiFileText size={18} />
                  </div>
                  <span className="text-sm font-semibold text-slate-300 truncate">
                    {file.name}
                  </span>
                </div>
                <button
                  onClick={() => removeFile(idx)}
                  className="p-1.5 text-slate-600 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all"
                >
                  <FiX size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Dynamic Launch Button */}
        <div className="mt-8 relative">
          <button
            onClick={handleUpload}
            disabled={loading || files.length === 0}
            className={`group/btn relative w-full py-5 rounded-2xl font-black uppercase tracking-widest text-sm transition-all duration-500 overflow-hidden
              ${loading
                ? "bg-slate-800 text-slate-500 cursor-not-allowed"
                : files.length > 0
                  ? "bg-indigo-600 text-white shadow-[0_10px_30px_rgba(79,70,229,0.4)] hover:shadow-[0_15px_40px_rgba(79,70,229,0.5)] hover:-translate-y-1"
                  : "bg-white/5 text-slate-600 border border-white/10 cursor-not-allowed"}
            `}
          >
            <div className="relative z-10 flex items-center justify-center gap-3">
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-slate-500 border-t-white rounded-full animate-spin" />
                  Processing Matrix...
                </>
              ) : (
                <>
                  {files.length > 0 && <FiCheckCircle className="animate-bounce" />}
                  Launch Analysis {files.length > 0 && `(${files.length})`}
                </>
              )}
            </div>

            {/* Shimmer Effect */}
            {!loading && files.length > 0 && (
                <div className="absolute inset-0 w-1/2 h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -skew-x-12 -translate-x-full group-hover/btn:animate-shimmer" />
            )}
          </button>
        </div>

        {/* Advanced Progress Display */}
        {loading && (
          <div className="mt-6 animate-in fade-in duration-700">
             <div className="flex justify-between items-end mb-2">
                <span className="text-[10px] font-black text-indigo-400 uppercase tracking-[0.2em]">Neural Engine Processing</span>
                <span className="text-lg font-black text-white leading-none">{progress}%</span>
             </div>
             <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400 transition-all duration-300 ease-out shadow-[0_0_10px_rgba(99,102,241,0.5)]"
                  style={{ width: `${progress}%` }}
                />
             </div>
          </div>
        )}

        {/* Global System Status */}
        <div className="mt-8 pt-6 border-t border-white/5 flex items-center justify-center gap-3">
          <div className="relative flex items-center justify-center">
            <div className={`w-2 h-2 rounded-full ${loading ? "bg-amber-500 animate-pulse" : "bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"}`} />
          </div>
          <span className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">
            {loading ? "Decrypting Risk Vectors" : "Ready for Deployment"}
          </span>
        </div>
      </div>
    </div>
  );
};

export default UploadCard;