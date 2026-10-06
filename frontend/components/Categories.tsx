"use client";
const cats=["All","Apartment","Villa","House","Cottage","Hotel","Cabin"];
export default function Categories({value,onChange}:{value:string;onChange:(v:string)=>void}){return <div className="categories">{cats.map(c=><button key={c} className={value===c?"selected":""} onClick={()=>onChange(c)}>{c}</button>)}</div>}
