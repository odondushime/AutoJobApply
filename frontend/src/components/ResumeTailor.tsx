import { useState } from "react";
import { motion } from "framer-motion";
import {
  DocumentArrowUpIcon,
  CheckCircleIcon,
  XCircleIcon,
} from "@heroicons/react/24/outline";

interface ResumeTailorProps {
  onOptimizedResume: (resume: string) => void;
}

interface AnalysisResult {
  overall_match_score: number;
  ats_score: number;
  suggestions: string[];
  matches: Record<
    string,
    {
      matched_keywords: string[];
      missing_keywords: string[];
      match_percentage: number;
      importance: number;
    }
  >;
}

const ResumeTailor = ({ onOptimizedResume }: ResumeTailorProps) => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!resumeFile || !jobDescription) {
      setError("Please provide both a resume and job description");
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch("http://localhost:5000/api/resume/tailor", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to tailor resume");
      }

      const data = await response.json();
      setAnalysis(data.analysis);
      onOptimizedResume(data.optimized_resume);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600";
    if (score >= 70) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-semibold text-gray-900">
          Tailor Your Resume
        </h2>
        <p className="mt-2 text-gray-600">
          Upload your resume and job description to get a tailored version
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="flex justify-center">
          <label className="relative cursor-pointer">
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileUpload}
              className="hidden"
            />
            <div className="flex flex-col items-center p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-indigo-500 transition-colors">
              <DocumentArrowUpIcon className="h-12 w-12 text-gray-400" />
              <span className="mt-2 text-sm font-medium text-gray-600">
                {resumeFile ? resumeFile.name : "Click to upload resume"}
              </span>
              <span className="mt-1 text-xs text-gray-500">
                PDF, DOC, or DOCX (max 5MB)
              </span>
            </div>
          </label>
        </div>

        <div>
          <label
            htmlFor="jobDescription"
            className="block text-sm font-medium text-gray-700"
          >
            Job Description
          </label>
          <textarea
            id="jobDescription"
            rows={6}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
          />
        </div>

        {error && (
          <div className="text-center text-red-600">
            <p>{error}</p>
          </div>
        )}

        <div className="flex justify-center">
          <button
            type="submit"
            disabled={isAnalyzing}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                Analyzing...
              </>
            ) : (
              "Tailor Resume"
            )}
          </button>
        </div>
      </form>

      {analysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8"
        >
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900">
                Match Score
              </h3>
              <span
                className={`text-4xl font-bold ${getScoreColor(analysis.overall_match_score)}`}
              >
                {analysis.overall_match_score}%
              </span>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900">ATS Score</h3>
              <span
                className={`text-4xl font-bold ${getScoreColor(analysis.ats_score)}`}
              >
                {analysis.ats_score}%
              </span>
            </div>
          </div>

          {analysis.suggestions.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Recommendations:
              </h3>
              <ul className="space-y-2">
                {analysis.suggestions.map(
                  (suggestion: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <span className="text-indigo-600 mr-2">•</span>
                      <span className="text-gray-600">{suggestion}</span>
                    </li>
                  )
                )}
              </ul>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default ResumeTailor;
