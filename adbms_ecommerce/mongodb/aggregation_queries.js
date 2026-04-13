// =====================================================
// MongoDB Aggregation Pipeline Queries
// ADBMS: Demonstrates NoSQL aggregation capabilities
// =====================================================

// 1. Top-Rated Products (Average Rating DESC)
db.products.aggregate([
  { $match: { "ratings_summary.review_count": { $gte: 10 } } },
  {
    $project: {
      product_id: 1, name: 1, brand: 1, category: 1,
      avg_rating: "$ratings_summary.avg_rating",
      review_count: "$ratings_summary.review_count"
    }
  },
  { $sort: { avg_rating: -1 } },
  { $limit: 10 }
]);

// 2. Category-wise Average Rating and Product Count
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      total_products: { $sum: 1 },
      avg_price: { $avg: "$price" },
      avg_rating: { $avg: "$ratings_summary.avg_rating" },
      total_reviews: { $sum: "$ratings_summary.review_count" }
    }
  },
  { $sort: { total_reviews: -1 } }
]);

// 3. Brand-wise Revenue Potential (Price × Review Count proxy)
db.products.aggregate([
  {
    $group: {
      _id: "$brand",
      product_count: { $sum: 1 },
      avg_price: { $avg: "$price" },
      total_reviews: { $sum: "$ratings_summary.review_count" },
      max_discount: { $max: "$discount_percent" }
    }
  },
  { $sort: { total_reviews: -1 } }
]);

// 4. Price Distribution by Category (Bucket analysis)
db.products.aggregate([
  {
    $bucket: {
      groupBy: "$price",
      boundaries: [0, 1000, 2000, 3000, 5000, 10000],
      default: "10000+",
      output: {
        count: { $sum: 1 },
        products: { $push: "$name" },
        avg_rating: { $avg: "$ratings_summary.avg_rating" }
      }
    }
  }
]);

// 5. Most Helpful Reviews per Product
db.reviews.aggregate([
  { $sort: { helpful_votes: -1 } },
  {
    $group: {
      _id: "$product_id",
      top_review: { $first: "$$ROOT" },
      total_reviews: { $sum: 1 },
      avg_rating: { $avg: "$rating" }
    }
  },
  { $sort: { avg_rating: -1 } }
]);

// 6. User Activity Analysis from Logs
db.logs.aggregate([
  {
    $group: {
      _id: { user_id: "$user_id", event_type: "$event_type" },
      count: { $sum: 1 },
      last_activity: { $max: "$timestamp" }
    }
  },
  {
    $group: {
      _id: "$_id.user_id",
      activities: {
        $push: {
          event: "$_id.event_type",
          count: "$count",
          last: "$last_activity"
        }
      },
      total_events: { $sum: "$count" }
    }
  },
  { $sort: { total_events: -1 } }
]);

// 7. Products with tags containing specific term (text search)
db.products.aggregate([
  { $match: { tags: { $in: ["wireless", "bluetooth"] } } },
  {
    $project: {
      product_id: 1, name: 1, brand: 1, price: 1,
      tag_count: { $size: "$tags" },
      avg_rating: "$ratings_summary.avg_rating"
    }
  }
]);

// 8. Monthly Review Trend
db.reviews.aggregate([
  {
    $addFields: {
      month: { $month: { $toDate: "$created_at" } },
      year: { $year: { $toDate: "$created_at" } }
    }
  },
  {
    $group: {
      _id: { year: "$year", month: "$month" },
      review_count: { $sum: 1 },
      avg_rating: { $avg: "$rating" }
    }
  },
  { $sort: { "_id.year": 1, "_id.month": 1 } }
]);
