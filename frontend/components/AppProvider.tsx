"use client";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

type AppContext = { userId:number; setUserId:(id:number)=>void };
const Ctx=createContext<AppContext | null>(null);
export function AppProvider({children}:{children:React.ReactNode}){
 const [userId,setUserIdState]=useState(3);
 useEffect(()=>{const saved=window.localStorage.getItem("userId"); if(saved) setUserIdState(Number(saved));},[]);
 const setUserId=(id:number)=>{setUserIdState(id); window.localStorage.setItem("userId",String(id));};
 const value=useMemo(()=>({userId,setUserId}),[userId]);
 return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
export function useApp(){const v=useContext(Ctx); if(!v) throw new Error("useApp must be used inside AppProvider"); return v;}
