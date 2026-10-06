"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import SearchBar from "../components/SearchBar";
import Categories from "../components/Categories";
import ListingCard from "../components/ListingCard";
import { api, ListingCard as Listing } from "../lib/api";

function HomeContent() {
  const params = useSearchParams();

  const [items, setItems] = useState<Listing[]>([]);
  const [category, setCategory] = useState("All");
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");

    api
      .listings({
        page,
        page_size: 12,
        location: params.get("location") || "",
        guests: params.get("guests") || "",
        property_type: category === "All" ? "" : category,
      })
      .then((r) => {
        setItems(r.items);
        setPages(r.pages || 1);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [page, category, params]);

  return (
    <div>
      <section className="hero">
        <div className="hero-inner">
          <p className="eyebrow">FIND YOUR NEXT STAY</p>
          <h1>Stay somewhere you’ll love.</h1>
          <p>Beautiful homes, trusted hosts and simple booking.</p>
          <SearchBar />
        </div>
      </section>

      <div className="content">
        <Categories
          value={category}
          onChange={(v) => {
            setCategory(v);
            setPage(1);
          }}
        />

        <div className="section-heading">
          <div>
            <h2>Explore stays</h2>
            <p>
              {params.get("location")
                ? `Results for ${params.get("location")}`
                : "Handpicked places for your next trip"}
            </p>
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading stays…</div>
        ) : error ? (
          <div className="error-box">{error}</div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <h2>No stays found</h2>
            <p>Try another location or category.</p>
          </div>
        ) : (
          <>
            <div className="listing-grid">
              {items.map((x) => (
                <ListingCard key={x.id} item={x} />
              ))}
            </div>

            <div className="pagination">
              <button
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
              >
                Previous
              </button>

              <span>
                Page {page} of {pages}
              </span>

              <button
                disabled={page >= pages}
                onClick={() => setPage(page + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<div className="loading">Loading stays…</div>}>
      <HomeContent />
    </Suspense>
  );
}
