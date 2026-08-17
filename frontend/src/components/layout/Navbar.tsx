"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();
  
  // Don't show public navbar on officer/admin dashboards
  if (pathname.startsWith('/officer') || pathname.startsWith('/admin')) {
    return null;
  }

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Report Issue", href: "/citizen/report" },
    { name: "Track Complaint", href: "/citizen/complaints" },
    { name: "Live Map", href: "/live-map" },
    { name: "Analytics", href: "/analytics" },
    { name: "About", href: "/about" },
  ];

  return (
    <nav className="sticky top-0 z-50 glass-nav transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20">
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-black tracking-tight text-risklens-dark">
                Risk<span className="text-risklens-primary">Lens</span>
              </span>
            </Link>
            
            <div className="hidden md:ml-10 md:flex md:space-x-8">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className={`${
                    pathname === link.href || (pathname.startsWith(link.href) && link.href !== '/')
                      ? "text-risklens-primary border-b-2 border-risklens-primary font-semibold"
                      : "text-gray-600 hover:text-risklens-primary"
                  } inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors`}
                >
                  {link.name}
                </Link>
              ))}
            </div>
          </div>
          
          <div className="hidden md:flex items-center gap-4">
            <Link
              href="/citizen/login"
              className="text-sm font-semibold text-gray-600 hover:text-risklens-primary transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/citizen/report"
              className="bg-risklens-primary text-white px-5 py-2.5 rounded-full font-bold hover:bg-risklens-deep transition-all shadow-sm text-sm"
            >
              Report an Issue
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
