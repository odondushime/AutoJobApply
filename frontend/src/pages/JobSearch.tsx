import { useState } from "react";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

export default function JobSearch() {
  const [searchParams, setSearchParams] = useState({
    keywords: "",
    location: "",
    jobBoard: "linkedin",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement job search
    console.log("Search params:", searchParams);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Job Search</h1>
        <p className="mt-1 text-sm text-gray-500">
          Search and apply to jobs automatically
        </p>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-4">
        <div>
          <label
            htmlFor="keywords"
            className="block text-sm font-medium text-gray-700"
          >
            Keywords
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="keywords"
              id="keywords"
              className="input-field"
              placeholder="e.g., Software Engineer, Python Developer"
              value={searchParams.keywords}
              onChange={(e) =>
                setSearchParams({ ...searchParams, keywords: e.target.value })
              }
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="location"
            className="block text-sm font-medium text-gray-700"
          >
            Location
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="location"
              id="location"
              className="input-field"
              placeholder="e.g., Remote, San Francisco"
              value={searchParams.location}
              onChange={(e) =>
                setSearchParams({ ...searchParams, location: e.target.value })
              }
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="jobBoard"
            className="block text-sm font-medium text-gray-700"
          >
            Job Board
          </label>
          <div className="mt-1">
            <select
              id="jobBoard"
              name="jobBoard"
              className="input-field"
              value={searchParams.jobBoard}
              onChange={(e) =>
                setSearchParams({ ...searchParams, jobBoard: e.target.value })
              }
            >
              <option value="linkedin">LinkedIn</option>
              <option value="indeed">Indeed</option>
              <option value="glassdoor">Glassdoor</option>
            </select>
          </div>
        </div>

        <div>
          <button type="submit" className="btn-primary w-full">
            <MagnifyingGlassIcon className="h-5 w-5 inline-block mr-2" />
            Search Jobs
          </button>
        </div>
      </form>

      <div className="card">
        <h2 className="text-lg font-medium text-gray-900">Search Results</h2>
        <div className="mt-4">
          <p className="text-sm text-gray-500">
            No results yet. Start a search to find jobs.
          </p>
        </div>
      </div>
    </div>
  );
}
