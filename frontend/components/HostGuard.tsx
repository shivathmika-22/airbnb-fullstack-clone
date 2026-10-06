"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "./AppProvider";
export default function HostGuard({children}:{children:React.ReactNode}){
 const {userId}=useApp(); const router=useRouter(); const isHost=userId===1||userId===2;
 useEffect(()=>{if(!isHost) router.replace("/");},[isHost,router]);
 if(!isHost) return <div className="center-page"><p>Redirecting…</p></div>;
 return <>{children}</>;
}
