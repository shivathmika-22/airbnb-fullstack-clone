"use client";
import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserCircle, Menu, X, Home, Heart, BriefcaseBusiness } from "lucide-react";
import { useApp } from "./AppProvider";

const users=[{id:1,name:"Aarav",email:"aarav@stayly.com",role:"host"},{id:2,name:"Priya",email:"priya@stayly.com",role:"host"},{id:3,name:"Shiv",email:"shiv@stayly.com",role:"guest"},{id:4,name:"Ananya",email:"ananya@stayly.com",role:"guest"}];
export function Navbar(){
 const {userId,setUserId}=useApp(); const pathname=usePathname(); const [open,setOpen]=React.useState(false); const [profile,setProfile]=React.useState(false);
 const user=users.find(x=>x.id===userId)||users[2]; const host=user.role==="host";
 return <header className="navbar"><div className="nav-inner">
  <Link href="/" className="brand"><span className="brand-mark">S</span><span>stayly</span></Link>
  <nav className="desktop-nav"><Link className={pathname==="/"?"active":""} href="/">Explore</Link>{host?<><Link href="/host"><BriefcaseBusiness size={16}/>Host Dashboard</Link><Link href="/host/listings">My Listings</Link><Link className={pathname.startsWith("/host/bookings")?"active":""} href="/host/bookings">Bookings</Link></>:<><Link href="/wishlist"><Heart size={16}/>Wishlist</Link><Link href="/trips">Trips</Link></>}</nav>
  <div className="nav-right"><select value={user.id} onChange={e=>setUserId(Number(e.target.value))}>{users.map(u=><option key={u.id} value={u.id}>{u.role==="host"?"Host":"Guest"}: {u.name}</option>)}</select><button className="icon-btn" onClick={()=>setProfile(!profile)} aria-label="Profile"><UserCircle size={30}/></button><button className="icon-btn mobile-only" onClick={()=>setOpen(!open)} aria-label="Menu">{open?<X/>:<Menu/>}</button>
  {profile&&<div className="profile-menu"><strong>{user.name}</strong><span>{user.email}</span><small>{user.role.toUpperCase()}</small><hr/>{host?<><Link href="/host">Host dashboard</Link><Link href="/host/listings">My listings</Link><Link href="/host/bookings">Bookings</Link></>:<><Link href="/trips">My trips</Link><Link href="/wishlist">Wishlist</Link></>}<button onClick={()=>setProfile(false)}>Close</button></div>}</div>
  {open&&<div className="mobile-menu"><Link href="/">Explore</Link>{host?<><Link href="/host">Host Dashboard</Link><Link href="/host/listings">My Listings</Link><Link href="/host/bookings">Bookings</Link></>:<><Link href="/wishlist">Wishlist</Link><Link href="/trips">Trips</Link></>}</div>}
 </div></header>
}
