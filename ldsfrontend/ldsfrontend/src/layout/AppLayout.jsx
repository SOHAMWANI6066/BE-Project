import Sidebar from "./Sidebar";

const AppLayout = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-200">

      {/* Sidebar (fixed width) */}
      <Sidebar />

      {/* Content Wrapper */}
      <div className="flex-1 ml-72 flex flex-col">

        {/* Main Content */}
        <main className="
          flex-1
          p-8
          overflow-y-auto
          bg-gradient-to-b
          from-slate-950
          via-slate-950
          to-slate-900
        ">
          {children}
        </main>

      </div>
    </div>
  );
};

export default AppLayout;