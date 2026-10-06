export type ListingCard={id:number;title:string;location:string;price_per_night:number;property_type:string;max_guests:number;primary_image:string|null;rating:number;review_count:number;is_favorite?:boolean};
export type User={id:number;name:string;email:string;role:string};
export type Image={id:number;image_url:string;is_primary:boolean};
export type ListingDetail=ListingCard & {description:string;host:User;images:Image[];amenities:string[]};
export type Booking={id:number;listing_id:number;guest_id:number;check_in:string;check_out:string;guests:number;total_price:number;status:string;created_at:string};
export type Quote={nights:number;nightly_total:number;cleaning_fee:number;service_fee:number;total:number};
export type Review={id:number;listing_id:number;user_id:number;rating:number;comment:string|null;created_at:string};
export type HostStats={listing_count:number;booking_count:number;confirmed_booking_count:number;revenue:number};
export type ListingInput={title:string;description:string;location:string;price_per_night:number;property_type:string;max_guests:number;images:{image_url:string;is_primary:boolean}[];amenities:string[]};
const BASE=process.env.NEXT_PUBLIC_API_URL||"http://127.0.0.1:8000";
function userId(){return typeof window!=="undefined"?localStorage.getItem("userId")||"3":process.env.NEXT_PUBLIC_USER_ID||"3";}
async function request<T>(path:string,options:RequestInit={}):Promise<T>{
 const res=await fetch(`${BASE}${path}`,{...options,headers:{"Content-Type":"application/json","X-User-Id":userId(),...(options.headers||{})},cache:"no-store"});
 if(!res.ok){let msg="Request failed";try{const j=await res.json();msg=j.detail||msg}catch{}throw new Error(msg)}
 if(res.status===204)return undefined as T; return res.json();
}
export const api={
 listings:(p:Record<string,string|number>={})=>{const qs=new URLSearchParams(Object.entries(p).filter(([,v])=>v!==""&&v!=null).map(([k,v])=>[k,String(v)])); return request<{items:ListingCard[];page:number;page_size:number;total:number;pages:number}>(`/listings?${qs}`)},
 listing:(id:number)=>request<ListingDetail>(`/listings/${id}`),
 quote:(id:number,a:string,b:string)=>request<Quote>(`/listings/${id}/quote?check_in=${a}&check_out=${b}`),
 book:(body:{listing_id:number;check_in:string;check_out:string;guests:number})=>request<Booking>("/bookings",{method:"POST",body:JSON.stringify(body)}),
 bookings:()=>request<Booking[]>("/bookings"), booking:(id:number)=>request<Booking>(`/bookings/${id}`), cancelBooking:(id:number)=>request<Booking>(`/bookings/${id}/cancel`,{method:"POST"}),
 favorites:()=>request<{listing_id:number}[]>("/favorites"), addFavorite:(id:number)=>request(`/favorites/${id}`,{method:"POST"}), removeFavorite:(id:number)=>request(`/favorites/${id}`,{method:"DELETE"}),
 reviews:(id:number)=>request<Review[]>(`/listings/${id}/reviews`), createReview:(id:number,b:{rating:number;comment?:string})=>request<Review>(`/listings/${id}/reviews`,{method:"POST",body:JSON.stringify(b)}),
 hostListings:()=>request<ListingCard[]>("/host/listings"), hostBookings:()=>request<Booking[]>("/host/bookings"), hostStats:()=>request<HostStats>("/host/stats"),
 createListing:(b:ListingInput)=>request<ListingDetail>("/listings",{method:"POST",body:JSON.stringify(b)}), updateListing:(id:number,b:Partial<ListingInput>)=>request<ListingDetail>(`/listings/${id}`,{method:"PATCH",body:JSON.stringify(b)}), deleteListing:(id:number)=>request<void>(`/listings/${id}`,{method:"DELETE"}),
 unavailable:(id:number)=>request<{check_in:string;check_out:string}[]>(`/listings/${id}/unavailable-dates`)
};
