import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  DocumentArrowUpIcon,
  RocketLaunchIcon,
  SparklesIcon,
  ChartBarIcon,
  ArrowRightIcon,
} from "@heroicons/react/24/outline";
import ResumeTailor from "../components/ResumeTailor";

const Landing = () => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [atsScore, setAtsScore] = useState<number | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [optimizedResume, setOptimizedResume] = useState<string | null>(null);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setResumeFile(file);
    setIsAnalyzing(true);
    setError(null);
    setRecommendations([]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/api/resume/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze resume");
      }

      const data = await response.json();
      setAtsScore(data.score);
      setRecommendations(data.recommendations);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleOptimizedResume = (resume: string) => {
    setOptimizedResume(resume);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-indigo-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
        <div className="relative max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <motion.h1
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl"
                >
                  <span className="block">Land Your Dream Job</span>
                  <span className="block text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                    With AI-Powered Precision
                  </span>
                </motion.h1>
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="mt-3 text-base text-gray-300 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0"
                >
                  Transform your job search with our AI-powered platform. Get
                  personalized resume analysis, automated job applications, and
                  expert career guidance.
                </motion.p>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                  className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start"
                >
                  <div className="rounded-md shadow">
                    <Link
                      to="/dashboard"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 md:py-4 md:text-lg md:px-10 transition-all duration-200"
                    >
                      Get Started
                      <ArrowRightIcon className="ml-2 h-5 w-5" />
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0 sm:ml-3">
                    <Link
                      to="/login"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 md:py-4 md:text-lg md:px-10 transition-all duration-200"
                    >
                      Sign In
                    </Link>
                  </div>
                </motion.div>
              </div>
            </main>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-white/10 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-indigo-400 font-semibold tracking-wide uppercase">
              Features
            </h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl">
              Everything you need to succeed
            </p>
          </div>

          <div className="mt-10">
            <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="relative bg-white/5 backdrop-blur-lg rounded-lg p-6 hover:bg-white/10 transition-all duration-200"
              >
                <div className="absolute -top-4 -left-4 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg">
                  <RocketLaunchIcon className="h-6 w-6" />
                </div>
                <p className="ml-8 text-lg leading-6 font-medium text-white">
                  Automated Job Applications
                </p>
                <p className="mt-2 ml-8 text-base text-gray-300">
                  Apply to hundreds of jobs with a single click. Our AI handles
                  the heavy lifting.
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="relative bg-white/5 backdrop-blur-lg rounded-lg p-6 hover:bg-white/10 transition-all duration-200"
              >
                <div className="absolute -top-4 -left-4 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg">
                  <SparklesIcon className="h-6 w-6" />
                </div>
                <p className="ml-8 text-lg leading-6 font-medium text-white">
                  ATS Optimization
                </p>
                <p className="mt-2 ml-8 text-base text-gray-300">
                  Get your resume past ATS systems with our advanced
                  optimization tools.
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="relative bg-white/5 backdrop-blur-lg rounded-lg p-6 hover:bg-white/10 transition-all duration-200"
              >
                <div className="absolute -top-4 -left-4 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg">
                  <ChartBarIcon className="h-6 w-6" />
                </div>
                <p className="ml-8 text-lg leading-6 font-medium text-white">
                  Smart Analytics
                </p>
                <p className="mt-2 ml-8 text-base text-gray-300">
                  Track your application success rate and get insights to
                  improve your chances.
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="relative bg-white/5 backdrop-blur-lg rounded-lg p-6 hover:bg-white/10 transition-all duration-200"
              >
                <div className="absolute -top-4 -left-4 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg">
                  <DocumentArrowUpIcon className="h-6 w-6" />
                </div>
                <p className="ml-8 text-lg leading-6 font-medium text-white">
                  Resume Tailoring
                </p>
                <p className="mt-2 ml-8 text-base text-gray-300">
                  Automatically customize your resume for each job application.
                </p>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Resume Analysis Section */}
      <div className="py-12 bg-gradient-to-b from-indigo-900/50 to-purple-900/50 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
              Get Your Resume Analyzed
            </h2>
            <p className="mt-4 text-lg text-gray-300">
              Upload your resume and get instant feedback on its ATS
              compatibility
            </p>
          </div>

          <div className="mt-12">
            <div className="bg-white/10 backdrop-blur-lg rounded-lg shadow-xl p-8 border border-white/20">
              <div className="space-y-6">
                <div className="flex justify-center">
                  <label className="relative cursor-pointer">
                    <input
                      type="file"
                      accept=".pdf,.doc,.docx"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                    <div className="flex flex-col items-center p-6 border-2 border-dashed border-white/30 rounded-lg hover:border-indigo-400 transition-colors bg-white/5">
                      <DocumentArrowUpIcon className="h-12 w-12 text-white/60" />
                      <span className="mt-2 text-sm font-medium text-white">
                        {resumeFile
                          ? resumeFile.name
                          : "Click to upload resume"}
                      </span>
                      <span className="mt-1 text-xs text-white/60">
                        PDF, DOC, or DOCX (max 5MB)
                      </span>
                    </div>
                  </label>
                </div>

                {error && (
                  <div className="text-center text-red-400">
                    <p>{error}</p>
                  </div>
                )}

                {isAnalyzing && (
                  <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-400 border-t-transparent"></div>
                    <p className="mt-2 text-sm text-white/60">
                      Analyzing your resume...
                    </p>
                  </div>
                )}

                {atsScore !== null && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center"
                  >
                    <div className="inline-flex items-center justify-center p-4 rounded-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 backdrop-blur-lg border border-white/20">
                      <span className="text-4xl font-bold text-white">
                        {atsScore}%
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-white/60">
                      ATS Compatibility Score
                    </p>

                    {recommendations.length > 0 && (
                      <div className="mt-6 text-left">
                        <h3 className="text-lg font-semibold text-white mb-2">
                          Recommendations:
                        </h3>
                        <ul className="space-y-2">
                          {recommendations.map((rec, index) => (
                            <li key={index} className="flex items-start">
                              <span className="text-indigo-400 mr-2">•</span>
                              <span className="text-white/80">{rec}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Resume Tailor Section */}
      {atsScore !== null && (
        <div className="py-12 bg-white/10 backdrop-blur-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <ResumeTailor onOptimizedResume={handleOptimizedResume} />
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-black/50 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-base text-white/60">
              &copy; 2024 AutoJobApply. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
