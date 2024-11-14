
# Post-Rate Project Documentation

## Overview

The `post-rate` project is a backend application designed to enable users to view a list of posts and rate them. The project is implemented using Django Rest Framework (DRF), PostgreSQL, Redis, and Kafka.


## Architecture

### Models

1. **Post**:
    - Fields: `title`, `content`, `created_by`.
    - Represents individual posts to be rated.

2. **Rating**:
    - Fields: `post`, `user`, `score`.
    - Links users to their ratings for specific posts.

### Database Design

- **PostgreSQL**:
  - Used as the main relational database for storing posts and ratings.
  - Chosen for its robust support for relational data.
- **Redis**:
  - Stores real-time statistics for each post, including the total ratings and their count.
  - Enables fast read and write operations for performance-critical tasks.

### Messaging System

- **Kafka**:
  - Handles rating updates asynchronously to avoid race conditions and ensure efficient updates to Redis.
  - Enables batch processing for enhanced performance.


## Main Endpoints

1. **Post - List**:
    - Provides a paginated list of posts with:
      - Title, content, and creator of the post.
      - The number of users who rated the post.
      - Average rating.
      - The requesting user's rating (if available).

2. **Rate - Create**:
    - Allows users to submit a rating (0-5) for a post.
    - Updates are idempotent, meaning users can change their rating, and only the latest value is stored.


## How It Works

1. **Rating a Post**:
    - When a user rates a post, the rating is saved in PostgreSQL.
    - A Kafka message is produced with the `post_id` and updated rating details.
    - A Kafka consumer processes these messages to update Redis with:
      - Total ratings.
      - Sum of all rating scores.

2. **Fetching Post List**:
    - Post data (title, content, ...) is fetched from PostgreSQL.
    - Redis is queried for average and total ratings.
      - Incorporates a 5-minute caching mechanism for post statistics to mitigate the impact of sudden, emotionally-driven rating spikes.
    - If a user rating exists, it is retrieved from PostgreSQL.


## How to Use

1. Clone the repository:
    ```bash
    git clone https://github.com/amirh-khali/post-rate.git
    cd post-rate
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Setup Redis using Docker:
    ```bash
    docker run --name redis -p 6379:6379 -d redis
    ```

4. Run database migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the application:
    ```bash
    python manage.py runserver
    ```

6. Start the Kafka consumer for Rating updates:
    ```bash
    python manage.py kafka_consumer.py
    ```


## Design Considerations

1. **Performance Under Load**:
    - Leveraged Redis for real-time stats to minimize database queries.
    - 5-minute cache for post statistics smooths out fluctuations from emotional or orchestrated rating surges.

2. **Data Consistency**:
    - Kafka ensures isolate updates to Redis by processing messages sequentially.

3. **Scalability**:
    - Kafka allows horizontal scaling by enabling multiple consumers for batch updates.
    - Redis provides a low-latency data store for scaling read operations.
