import { motion } from "framer-motion";
import {
  ChartBarIcon,
  BriefcaseIcon,
  CheckCircleIcon,
  ClockIcon,
} from "@heroicons/react/24/outline";

const Dashboard = () => {
  const stats = [
    {
      name: "Total Applications",
      value: "156",
      icon: BriefcaseIcon,
      change: "+12%",
      changeType: "increase",
    },
    {
      name: "Success Rate",
      value: "23%",
      icon: ChartBarIcon,
      change: "+5%",
      changeType: "increase",
    },
    {
      name: "Interviews",
      value: "12",
      icon: CheckCircleIcon,
      change: "+3",
      changeType: "increase",
    },
    {
      name: "Pending",
      value: "45",
      icon: ClockIcon,
      change: "-2",
      changeType: "decrease",
    },
  ];

  const recentApplications = [
    {
      id: 1,
      company: "Tech Corp",
      position: "Senior Software Engineer",
      status: "Applied",
      date: "2024-03-20",
    },
    {
      id: 2,
      company: "StartupX",
      position: "Full Stack Developer",
      status: "Interview",
      date: "2024-03-19",
    },
    {
      id: 3,
      company: "Big Tech",
      position: "Frontend Developer",
      status: "Rejected",
      date: "2024-03-18",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Track your job search progress and manage your applications
        </p>
      </motion.div>

      {/* Stats */}
      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon
                    className="h-6 w-6 text-gray-400"
                    aria-hidden="true"
                  />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd>
                      <div className="text-lg font-medium text-gray-900">
                        {stat.value}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm">
                <span
                  className={`font-medium ${
                    stat.changeType === "increase"
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  {stat.change}
                </span>
                <span className="text-gray-500"> from last month</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Recent Applications */}
      <div className="mt-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-white shadow rounded-lg"
        >
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Recent Applications
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              A list of your most recent job applications
            </p>
          </div>
          <div className="border-t border-gray-200">
            <ul className="divide-y divide-gray-200">
              {recentApplications.map((application) => (
                <motion.li
                  key={application.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  className="px-4 py-4 sm:px-6"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <BriefcaseIcon
                          className="h-6 w-6 text-gray-400"
                          aria-hidden="true"
                        />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {application.position}
                        </div>
                        <div className="text-sm text-gray-500">
                          {application.company}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          application.status === "Applied"
                            ? "bg-blue-100 text-blue-800"
                            : application.status === "Interview"
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                        }`}
                      >
                        {application.status}
                      </span>
                      <span className="ml-4 text-sm text-gray-500">
                        {application.date}
                      </span>
                    </div>
                  </div>
                </motion.li>
              ))}
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
