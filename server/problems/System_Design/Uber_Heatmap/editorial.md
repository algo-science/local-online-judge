# System Design Breakdown: Uber Driver Heatmap

## 1. High-Level Architecture
We use a **Lambda Architecture** to handle the two distinct access patterns (Hot Path vs Cold Path).

### Ingestion Layer
*   **Gateway Service:** Receives WebSocket/HTTP2 pings from drivers.
*   **Message Broker (Kafka/Kinesis):** Acts as the durable "Source of Truth" buffer.
    *   Throughput: ~10k events/sec.

## 2. Scenario A: Near Real-Time (Hot Path)
*   **Stream Processor (Flink/Spark Streaming):** 
    *   Consumes from Kafka.
    *   **Logic:** Converts (Lat, Long) -> **H3 Grid Index**.
    *   **Aggregation:** Sliding Window (20 mins), incrementing counts per GridID. Uses **HyperLogLog (HLL)** for unique driver counts to save memory.
*   **Storage (Redis):**
    *   Stores `Key: {CityID}_{Window}_{GridID} -> Value: Count`.
    *   TTL: 30 minutes (self-cleaning).

## 3. Scenario B: Historical (Cold Path)
*   **Archival:** Kafka Connect dumps raw logs to **S3/GCS** (Data Lake) in Parquet format.
*   **Batch Processing (Spark):** Runs hourly.
    *   Performs **exact deduplication** (Count Distinct).
    *   Maps coords to H3 Grid IDs.
*   **Storage (OLAP - ClickHouse/Druid):**
    *   Optimized for time-series aggregation queries.
    *   Stores `Timestamp (Hour), CityID, GridID, UniqueCount`.

## 4. Trade-offs
*   **Real-time:** Optimized for low latency, accepts approximate results (HLL).
*   **Historical:** Optimized for accuracy and ad-hoc queries, accepts high latency (24hr).
