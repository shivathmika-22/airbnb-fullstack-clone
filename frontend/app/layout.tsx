import type { Metadata } from "next";
import "./globals.css";
import { AppProvider } from "../components/AppProvider";
import { Navbar } from "../components/Navbar";
export const metadata:Metadata={title:"Stayly — Airbnb Clone",description:"Stayly marketplace"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><AppProvider><Navbar/><main>{children}</main></AppProvider></body></html>}
