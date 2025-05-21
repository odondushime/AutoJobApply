import { Link, useLocation } from "react-router-dom";
import {
  HomeIcon,
  MagnifyingGlassIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/outline";

const navigation = [
  { name: "Dashboard", href: "/", icon: HomeIcon },
  { name: "Job Search", href: "/search", icon: MagnifyingGlassIcon },
  { name: "Settings", href: "/settings", icon: Cog6ToothIcon },
];

export default function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-primary-600">
              AutoJobApply
            </Link>
          </div>

          <div className="flex space-x-4">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium ${
                    isActive
                      ? "bg-primary-50 text-primary-600"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  }`}
                >
                  <item.icon className="h-5 w-5 mr-2" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
