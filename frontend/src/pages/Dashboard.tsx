import { useQuery } from "@tanstack/react-query";
import {
  DocumentCheckIcon,
  ClockIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";

const stats = [
  { name: "Total Applications", value: "0", icon: DocumentCheckIcon },
  { name: "In Progress", value: "0", icon: ClockIcon },
  { name: "Successful", value: "0", icon: CheckCircleIcon },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Track your job application progress
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {stats.map((item) => (
          <div
            key={item.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6"
          >
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {item.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline">
              <p className="text-2xl font-semibold text-gray-900">
                {item.value}
              </p>
            </dd>
          </div>
        ))}
      </div>

      <div className="card">
        <h2 className="text-lg font-medium text-gray-900">
          Recent Applications
        </h2>
        <div className="mt-4">
          <p className="text-sm text-gray-500">No recent applications</p>
        </div>
      </div>
    </div>
  );
}
