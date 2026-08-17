import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-[calc(100vh-64px)]">
      {/* Hero Section */}
      <main className="flex-1">
        <div className="relative bg-white overflow-hidden">
          <div className="max-w-7xl mx-auto">
            <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32 pt-20">
              <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
                <div className="sm:text-center lg:text-left">
                  <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                    <span className="block xl:inline">AI-Powered Civic</span>{" "}
                    <span className="block text-blue-600 xl:inline">Issue Resolution</span>
                  </h1>
                  <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                    RiskLens automatically categorizes, prioritizes, and routes public complaints to the right authorities in seconds using cutting-edge AI and spatial mapping.
                  </p>
                  <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start gap-4">
                    <div className="rounded-md shadow">
                      <Link
                        href="/citizen/report"
                        className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-colors"
                      >
                        Report an Issue
                      </Link>
                    </div>
                    <div className="mt-3 sm:mt-0 sm:ml-3">
                      <Link
                        href="/officer/login"
                        className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 md:py-4 md:text-lg md:px-10 transition-colors"
                      >
                        Officer Portal
                      </Link>
                    </div>
                  </div>
                </div>
              </main>
            </div>
          </div>
          <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2 bg-gray-50 flex items-center justify-center border-l border-gray-200">
            {/* Nagpur Smart City Command Center Mockup */}
            <div className="relative w-full h-full flex flex-col items-center justify-center p-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-20">
              
              {/* Central Map Radar */}
              <div className="relative w-80 h-80 rounded-full border-4 border-risklens-primary/20 flex items-center justify-center">
                <div className="absolute w-64 h-64 rounded-full border border-risklens-primary/40 animate-ping opacity-20"></div>
                <div className="absolute w-48 h-48 rounded-full border border-risklens-primary/60"></div>
                <div className="w-32 h-32 bg-risklens-primary rounded-full shadow-[0_0_40px_rgba(255,107,0,0.4)] flex items-center justify-center text-white font-bold">
                  Nagpur Zero Mile
                </div>
                
                {/* Markers */}
                <div className="absolute top-10 left-20 w-4 h-4 bg-red-500 rounded-full shadow-[0_0_10px_red]"></div>
                <div className="absolute bottom-20 right-10 w-4 h-4 bg-amber-500 rounded-full shadow-[0_0_10px_orange]"></div>
                <div className="absolute top-40 right-20 w-4 h-4 bg-risklens-primary rounded-full shadow-[0_0_10px_#FF6B00]"></div>
              </div>

              {/* Floating Cards */}
              <div className="absolute top-20 right-10 bg-white p-4 rounded-xl shadow-xl border-l-4 border-risklens-primary">
                <p className="text-xs text-gray-500 font-bold uppercase">Critical Incident</p>
                <p className="text-sm font-bold text-gray-800">Traffic Jam - Wardha Rd</p>
                <p className="text-xs text-risklens-primary mt-1">AI Confidence: 94%</p>
              </div>

              <div className="absolute bottom-20 left-10 bg-risklens-dark p-4 rounded-xl shadow-xl">
                <p className="text-xs text-gray-400 font-bold uppercase">Live City Status</p>
                <ul className="text-sm text-white mt-2 space-y-1">
                  <li className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-green-500"></span> Traffic Normal</li>
                  <li className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-risklens-primary"></span> 3 Active Complaints</li>
                  <li className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-red-500"></span> 1 High Risk Zone</li>
                </ul>
              </div>

            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Features</h2>
              <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                A smarter way to manage cities
              </p>
            </div>

            <div className="mt-10">
              <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
                {/* Feature 1 */}
                <div className="relative p-6 bg-white rounded-xl shadow-sm border border-gray-100">
                  <div className="w-12 h-12 flex items-center justify-center rounded-md bg-blue-500 text-white mb-4">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                  </div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">AI Classification</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Our AI automatically analyzes descriptions and identifies the exact category and department needed.
                  </p>
                </div>

                {/* Feature 2 */}
                <div className="relative p-6 bg-white rounded-xl shadow-sm border border-gray-100">
                  <div className="w-12 h-12 flex items-center justify-center rounded-md bg-indigo-500 text-white mb-4">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                  </div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Spatial Routing</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Complaints are pinpointed on the map and automatically assigned to the correct ward officers.
                  </p>
                </div>

                {/* Feature 3 */}
                <div className="relative p-6 bg-white rounded-xl shadow-sm border border-gray-100">
                  <div className="w-12 h-12 flex items-center justify-center rounded-md bg-orange-500 text-white mb-4">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">SLA Tracking</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Every issue is bound by strict Service Level Agreements to ensure timely resolution.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 md:flex md:items-center md:justify-between lg:px-8">
          <div className="mt-8 md:mt-0 md:order-1">
            <p className="text-center text-base text-gray-400">
              &copy; 2026 RiskLens Civic Platform. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
