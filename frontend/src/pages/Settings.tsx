import { useState } from "react";
import { UserIcon, DocumentIcon, KeyIcon } from "@heroicons/react/24/outline";

export default function Settings() {
  const [settings, setSettings] = useState({
    name: "",
    email: "",
    phone: "",
    location: "",
    resume: null as File | null,
    coverLetter: null as File | null,
    linkedinEmail: "",
    linkedinPassword: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement settings save
    console.log("Settings:", settings);
  };

  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    type: "resume" | "coverLetter"
  ) => {
    const file = e.target.files?.[0] || null;
    setSettings({ ...settings, [type]: file });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-500">
          Configure your job application settings
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 flex items-center">
            <UserIcon className="h-5 w-5 mr-2" />
            Personal Information
          </h2>
          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700"
              >
                Full Name
              </label>
              <input
                type="text"
                id="name"
                className="input-field mt-1"
                value={settings.name}
                onChange={(e) =>
                  setSettings({ ...settings, name: e.target.value })
                }
              />
            </div>
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                className="input-field mt-1"
                value={settings.email}
                onChange={(e) =>
                  setSettings({ ...settings, email: e.target.value })
                }
              />
            </div>
            <div>
              <label
                htmlFor="phone"
                className="block text-sm font-medium text-gray-700"
              >
                Phone
              </label>
              <input
                type="tel"
                id="phone"
                className="input-field mt-1"
                value={settings.phone}
                onChange={(e) =>
                  setSettings({ ...settings, phone: e.target.value })
                }
              />
            </div>
            <div>
              <label
                htmlFor="location"
                className="block text-sm font-medium text-gray-700"
              >
                Location
              </label>
              <input
                type="text"
                id="location"
                className="input-field mt-1"
                value={settings.location}
                onChange={(e) =>
                  setSettings({ ...settings, location: e.target.value })
                }
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 flex items-center">
            <DocumentIcon className="h-5 w-5 mr-2" />
            Documents
          </h2>
          <div className="mt-4 space-y-4">
            <div>
              <label
                htmlFor="resume"
                className="block text-sm font-medium text-gray-700"
              >
                Resume
              </label>
              <input
                type="file"
                id="resume"
                accept=".pdf,.doc,.docx"
                className="input-field mt-1"
                onChange={(e) => handleFileChange(e, "resume")}
              />
            </div>
            <div>
              <label
                htmlFor="coverLetter"
                className="block text-sm font-medium text-gray-700"
              >
                Cover Letter
              </label>
              <input
                type="file"
                id="coverLetter"
                accept=".pdf,.doc,.docx"
                className="input-field mt-1"
                onChange={(e) => handleFileChange(e, "coverLetter")}
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 flex items-center">
            <KeyIcon className="h-5 w-5 mr-2" />
            Job Board Credentials
          </h2>
          <div className="mt-4 space-y-4">
            <div>
              <label
                htmlFor="linkedinEmail"
                className="block text-sm font-medium text-gray-700"
              >
                LinkedIn Email
              </label>
              <input
                type="email"
                id="linkedinEmail"
                className="input-field mt-1"
                value={settings.linkedinEmail}
                onChange={(e) =>
                  setSettings({ ...settings, linkedinEmail: e.target.value })
                }
              />
            </div>
            <div>
              <label
                htmlFor="linkedinPassword"
                className="block text-sm font-medium text-gray-700"
              >
                LinkedIn Password
              </label>
              <input
                type="password"
                id="linkedinPassword"
                className="input-field mt-1"
                value={settings.linkedinPassword}
                onChange={(e) =>
                  setSettings({ ...settings, linkedinPassword: e.target.value })
                }
              />
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button type="submit" className="btn-primary">
            Save Settings
          </button>
        </div>
      </form>
    </div>
  );
}
