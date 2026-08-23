"use client";
import React, { useState, useEffect } from "react";
import { Search, MapPin, Phone, Mail, DollarSign, Home, Activity, LogOut, ChevronRight } from "lucide-react";

export default function SaaSApp() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  if (!isLoggedIn) {
    return <LoginScreen onLogin={() => setIsLoggedIn(true)} />;
  }
  return <Dashboard onLogout={() => setIsLoggedIn(false)} />;
}

function LoginScreen({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    onLogin();
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="relative w-full max-w-md bg-white/5 border border-white/10 backdrop-blur-xl p-8 rounded-2xl shadow-2xl">
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-blue-500/50">
            <Home className="text-white w-6 h-6" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight">LeadProphet</h1>
          <p className="text-slate-400 mt-2 text-sm">Sign in to your investor workspace</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Email address</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-black/30 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-slate-600"
              placeholder="investor@example.com"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-black/30 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-slate-600"
              placeholder="••••••••"
              required
            />
          </div>
          <button 
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 rounded-lg mt-6 shadow-lg shadow-blue-600/30 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
          >
            Access Workspace
          </button>
        </form>
      </div>
    </div>
  );
}

function Dashboard({ onLogout }: { onLogout: () => void }) {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("https://bright-seals-move.loca.lt/api/leads", {
      headers: {
        "Bypass-Tunnel-Reminder": "true"
      }
    })
      .then(res => res.json())
      .then(data => {
        setLeads(data.leads || []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load leads", err);
        setLoading(false);
      });
  }, []);

  const validPhones = leads.filter(l => l.phone_1 && l.phone_1 !== 'Not found' && l.phone_1 !== 'API Error' && l.phone_1 !== 'None found').length;
  const matchRate = leads.length > 0 ? Math.round((validPhones / leads.length) * 100) : 0;

  const filteredLeads = leads.filter(l => 
    (l.owner_name && l.owner_name.toLowerCase().includes(search.toLowerCase())) ||
    (l.property_address && l.property_address.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="min-h-screen bg-[#0A0F1C] text-slate-200 flex">
      {/* Sidebar */}
      <div className="w-64 border-r border-white/5 bg-white/[0.02] p-6 flex flex-col hidden md:flex">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Home className="text-white w-5 h-5" />
          </div>
          <span className="text-xl font-bold text-white tracking-tight">LeadProphet</span>
        </div>
        
        <nav className="flex-1 space-y-2">
          <a href="#" className="flex items-center gap-3 bg-blue-600/10 text-blue-400 px-4 py-3 rounded-xl font-medium border border-blue-500/20">
            <Activity className="w-5 h-5" />
            Live Leads
          </a>
          <a href="#" className="flex items-center gap-3 text-slate-400 hover:text-white px-4 py-3 rounded-xl font-medium transition-colors hover:bg-white/5">
            <ChevronRight className="w-5 h-5" />
            Campaigns
          </a>
          <a href="#" className="flex items-center gap-3 text-slate-400 hover:text-white px-4 py-3 rounded-xl font-medium transition-colors hover:bg-white/5">
            <ChevronRight className="w-5 h-5" />
            Settings
          </a>
        </nav>
        
        <button onClick={onLogout} className="flex items-center gap-3 text-slate-500 hover:text-red-400 mt-auto px-4 py-3 font-medium transition-colors">
          <LogOut className="w-5 h-5" />
          Sign out
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 overflow-y-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-white">Pre-Foreclosure Leads</h2>
            <p className="text-slate-400 text-sm mt-1">Real-time distressed property data</p>
          </div>
          <div className="relative">
            <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input 
              type="text" 
              placeholder="Search owners or addresses..." 
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:border-blue-500 w-64 transition-all"
            />
          </div>
        </header>

        {/* Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 group-hover:bg-blue-500/20 transition-all"></div>
            <p className="text-slate-400 text-sm font-medium">Total Properties Found</p>
            <p className="text-3xl font-bold text-white mt-2">{leads.length}</p>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 group-hover:bg-emerald-500/20 transition-all"></div>
            <p className="text-slate-400 text-sm font-medium">Verified Phone Numbers</p>
            <p className="text-3xl font-bold text-white mt-2">{validPhones}</p>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 group-hover:bg-purple-500/20 transition-all"></div>
            <p className="text-slate-400 text-sm font-medium">Skip-Trace Match Rate</p>
            <p className="text-3xl font-bold text-white mt-2">{matchRate}%</p>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white/[0.02] border border-white/5 rounded-2xl overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/5 bg-white/[0.02]">
                  <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Owner</th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Property</th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Value</th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Contact</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {loading ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-slate-500">Loading live data...</td>
                  </tr>
                ) : filteredLeads.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-slate-500">No properties found.</td>
                  </tr>
                ) : (
                  filteredLeads.map((lead, idx) => (
                    <tr key={idx} className="hover:bg-white/[0.02] transition-colors group">
                      <td className="px-6 py-4">
                        <div className="font-medium text-white">{lead.owner_name}</div>
                        <div className="text-xs text-slate-500 mt-1">ID: {lead.id}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-start gap-2">
                          <MapPin className="w-4 h-4 text-blue-400 mt-0.5 shrink-0" />
                          <div>
                            <div className="text-slate-200">{lead.property_address}</div>
                            <a href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(lead.property_address)}`} target="_blank" className="text-xs text-blue-400 hover:text-blue-300 transition-colors">
                              View on Map
                            </a>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
                          <DollarSign className="w-4 h-4" />
                          {lead.property_value}
                        </div>
                        <div className="text-xs text-slate-500 mt-1">Delinquent: {lead.delinquent_amount}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="space-y-2">
                          <div className="flex items-center gap-2 text-sm">
                            <Phone className="w-3.5 h-3.5 text-slate-500" />
                            <span className={lead.phone_1 && lead.phone_1 !== 'Not found' ? 'text-slate-300' : 'text-slate-600'}>
                              {lead.phone_1 || 'Not found'}
                            </span>
                          </div>
                          <div className="flex items-center gap-2 text-sm">
                            <Mail className="w-3.5 h-3.5 text-slate-500" />
                            <span className={lead.email && lead.email !== 'Not found' ? 'text-slate-300' : 'text-slate-600'}>
                              {lead.email || 'Not found'}
                            </span>
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
