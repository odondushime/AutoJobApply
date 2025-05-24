import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  DocumentArrowUpIcon,
  CheckCircleIcon,
  XCircleIcon,
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

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600";
    if (score >= 70) return "text-yellow-600";
    return "text-red-600";
  };

  const handleOptimizedResume = (resume: string) => {
    setOptimizedResume(resume);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Get Your Dream Job
          </h1>
          <p className="mt-4 text-xl text-gray-600">
            Start by checking if your resume is ATS-friendly
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-12"
        >
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold text-gray-900">
                Upload Your Resume
              </h2>
              <p className="mt-2 text-gray-600">
                We'll analyze your resume for ATS compatibility
              </p>
            </div>

            <div className="space-y-6">
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

              {error && (
                <div className="text-center text-red-600">
                  <p>{error}</p>
                </div>
              )}

              {isAnalyzing && (
                <div className="text-center">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
                  <p className="mt-2 text-sm text-gray-600">
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
                  <div className="inline-flex items-center justify-center p-4 rounded-full bg-gray-50">
                    <span
                      className={`text-4xl font-bold ${getScoreColor(atsScore)}`}
                    >
                      {atsScore}%
                    </span>
                  </div>
                  <p className="mt-2 text-sm text-gray-600">
                    ATS Compatibility Score
                  </p>
                  <div className="mt-4 space-y-2">
                    {atsScore >= 90 ? (
                      <div className="flex items-center text-green-600">
                        <CheckCircleIcon className="h-5 w-5 mr-2" />
                        <span>Your resume is highly ATS-friendly!</span>
                      </div>
                    ) : (
                      <div className="flex items-center text-yellow-600">
                        <XCircleIcon className="h-5 w-5 mr-2" />
                        <span>Your resume could use some improvements</span>
                      </div>
                    )}
                  </div>

                  {recommendations.length > 0 && (
                    <div className="mt-6 text-left">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        Recommendations:
                      </h3>
                      <ul className="space-y-2">
                        {recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-indigo-600 mr-2">•</span>
                            <span className="text-gray-600">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </div>
        </motion.div>

        {atsScore !== null && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-12"
          >
            <ResumeTailor onOptimizedResume={handleOptimizedResume} />
          </motion.div>
        )}

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="mt-12 text-center"
        >
          <div className="mt-6">
            <label className="flex items-center justify-center space-x-2 text-sm text-gray-600">
              <input
                type="checkbox"
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span>
                I agree to the Privacy Policy and confirm that the information
                provided is either my own or I have the right to submit it.
              </span>
            </label>
          </div>

          <div className="mt-8">
            <Link
              to="/dashboard"
              className="inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Continue to Job Search
            </Link>
          </div>

          <p className="mt-6 text-sm text-gray-500">
            Already Have An Account?{" "}
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              Sign In
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default Landing;
