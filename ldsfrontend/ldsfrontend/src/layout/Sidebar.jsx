import React from "react";
import {
  LayoutDashboard,
  FileUp,
  BarChart3,
  FileText,
  Settings,
  LogOut,
} from "lucide-react";

const Sidebar = () => {
  const navItems = [
    { name: "Dashboard", icon: LayoutDashboard, active: true },
    { name: "Upload Contracts", icon: FileUp, active: false },
    { name: "Analytics", icon: BarChart3, active: false },
    { name: "Reports", icon: FileText, active: false },
  ];

  return (
    <aside className="
      fixed left-0 top-0 h-screen w-72
      bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950
      border-r border-slate-800/60
      backdrop-blur-xl
      flex flex-col justify-between
      shadow-[0_0_40px_rgba(99,102,241,0.05)]
      z-50
    ">

      {/* Brand */}
      <div>
        <div className="flex items-center gap-3 px-6 py-8">
          <div className="
            h-9 w-9
            bg-indigo-600/20
            border border-indigo-500/30
            rounded-xl
            flex items-center justify-center
            shadow-lg shadow-indigo-500/20
          ">
            <div className="h-4 w-4 bg-indigo-500 rounded-sm" />
          </div>

          <h2 className="text-xl font-bold text-white tracking-tight">
            Zero<span className="text-indigo-500">Paper</span>
          </h2>
        </div>

        {/* Navigation */}
        <nav className="space-y-2 px-4">
          {navItems.map((item) => (
            <SidebarItem key={item.name} {...item} />
          ))}
        </nav>
      </div>

      {/* Bottom Section */}
      <div className="border-t border-slate-800/60 p-4 space-y-2">
        <BottomItem icon={Settings} label="Settings" />
        <BottomItem icon={LogOut} label="Logout" danger />
      </div>
    </aside>
  );
};

const SidebarItem = ({ name, icon: Icon, active }) => {
  return (
    <button
      className={`
        relative w-full flex items-center gap-3 px-4 py-3 rounded-xl
        text-sm font-medium transition-all duration-300 group
        ${
          active
            ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shadow-inner"
            : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
        }
      `}
    >
      {/* Left active indicator */}
      {active && (
        <span className="absolute left-0 top-0 h-full w-1 bg-indigo-500 rounded-r-full" />
      )}

      <Icon
        className={`
          w-5 h-5 transition-colors
          ${
            active
              ? "text-indigo-400"
              : "text-slate-500 group-hover:text-white"
          }
        `}
      />

      {name}
    </button>
  );
};

const BottomItem = ({ icon: Icon, label, danger }) => {
  return (
    <button
      className={`
        w-full flex items-center gap-3 px-4 py-3 rounded-xl
        text-sm font-medium transition-all duration-300
        ${
          danger
            ? "text-rose-400 hover:bg-rose-500/10"
            : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
        }
      `}
    >
      <Icon className="w-5 h-5" />
      {label}
    </button>
  );
};

export default Sidebar;