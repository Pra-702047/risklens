import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-risklens-black text-gray-400 py-12 border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <span className="text-2xl font-black tracking-tight text-white mb-4 block">
              Risk<span className="text-risklens-primary">Lens</span>
            </span>
            <p className="text-gray-400 mb-6 max-w-sm">
              Built for a smarter, safer and more responsive Nagpur.
            </p>
          </div>
          
          <div>
            <h3 className="text-white font-semibold mb-4">Citizen Services</h3>
            <ul className="space-y-2">
              <li><Link href="/citizen/report" className="hover:text-risklens-primary transition-colors">Report an Issue</Link></li>
              <li><Link href="/citizen/complaints" className="hover:text-risklens-primary transition-colors">Track Complaint</Link></li>
              <li><Link href="/live-map" className="hover:text-risklens-primary transition-colors">Live Map</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-white font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
              <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
          <p>&copy; {new Date().getFullYear()} RiskLens Civic Platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
