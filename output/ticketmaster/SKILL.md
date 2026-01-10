---
name: ticketmaster-api
description: Integrate with Ticketmaster Discovery API to search events, attractions, venues, and classifications. Use when building event discovery apps, ticket platforms, venue finders, or entertainment search features. Access 230K+ events across US, Canada, Mexico, Australia, UK, and Europe. Includes authentication, rate limiting, and comprehensive API examples.
---

## When to Use This Skill

Use this skill when you need to work with Ticketmaster, including:
- Searching for concerts, sports events, and entertainment
- Building event discovery applications
- Integrating ticket information into websites or apps
- Finding venues and their details
- Searching for artists, sports teams, and attractions
- Implementing location-based event search
- Displaying event images and pricing information
- Building event calendars and listings

## Overview

**Ticketmaster Discovery API** provides access to a comprehensive database of over **230,000+ events** across multiple countries including the United States, Canada, Mexico, Australia, New Zealand, United Kingdom, Ireland, and other European countries.

**Key Resources:**
- https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
- https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
- Developer Portal: https://developer.ticketmaster.com/

**Data Sources:**
- Ticketmaster
- Universe
- FrontGate Tickets
- Ticketmaster Resale (TMR)

## API Overview

### Base URL

```
https://app.ticketmaster.com/{package}/{version}/{resource}.json?apikey={YOUR_KEY}
```

**Components:**
- `package`: API package (e.g., discovery, commerce)
- `version`: API version (v1, v2, v3)
- `resource`: Endpoint resource
- `apikey`: Your API key (required)

### Discovery API v2 Base URL

```
https://app.ticketmaster.com/discovery/v2/
```

## Authentication

### Getting an API Key

1. **Register**: Visit https://developer.ticketmaster.com/
2. **Login or Create Account**: Register for an API key
3. **Get API Key**: Available immediately in your dashboard
4. **Use in Requests**: Append as `apikey` query parameter

**Example:**
```
https://app.ticketmaster.com/discovery/v2/events.json?apikey=YOUR_API_KEY
```

### API Key Usage

```bash
# All requests require apikey parameter
curl 'https://app.ticketmaster.com/discovery/v2/events.json?apikey=AbCdEfGh123456'
```

**Error without API key:**
```json
{
  "fault": {
    "faultstring": "Invalid ApiKey",
    "detail": {
      "errorcode": "oauth.v2.InvalidApiKey"
    }
  }
}
```

## Rate Limits

### Default Limits

- **Daily Quota**: 5,000 API calls per day
- **Rate Limit**: 5 requests per second
- **Pagination Limit**: size × page < 1,000

### Monitoring Usage

Response headers indicate your usage:

```http
Rate-Limit: 5000
Rate-Limit-Available: 4723
Rate-Limit-Reset: 1445461429
```

**Headers:**
- `Rate-Limit`: Total daily quota
- `Rate-Limit-Available`: Remaining requests
- `Rate-Limit-Reset`: UTC timestamp when quota resets

### Rate Limit Exceeded

**HTTP 429 Response:**
```json
{
  "fault": {
    "faultstring": "Rate limit quota violation. Quota limit exceeded.",
    "detail": {
      "errorcode": "policies.ratelimit.QuotaViolation"
    }
  }
}
```

### Requesting Higher Limits

To increase limits:
1. Demonstrate Terms of Service compliance
2. Follow brand guidelines
3. Proper data representation
4. Contact Ticketmaster developer support

## Core Endpoints

### 1. Search Events

**Endpoint:** `GET /discovery/v2/events`

Search for events with extensive filtering options.

**Example Request:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/events.json?city=Los+Angeles&classificationName=music&apikey=YOUR_KEY'
```

**Key Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `keyword` | string | Search term for events |
| `attractionId` | string | Filter by performer/attraction |
| `venueId` | string | Filter by venue |
| `city` | array | Filter by city |
| `countryCode` | string | Country code (US, CA, MX, etc.) |
| `stateCode` | string | State/province code |
| `postalCode` | string | ZIP/postal code |
| `classificationName` | array | Genre/segment (e.g., music, sports) |
| `dmaId` | string | Designated Market Area ID |
| `startDateTime` | string | Start date filter (ISO 8601) |
| `endDateTime` | string | End date filter (ISO 8601) |
| `size` | string | Results per page (default: 20) |
| `page` | string | Page number (default: 0) |
| `sort` | string | Sort order |

**Sorting Options:**
- `name,asc` / `name,desc` - Event name
- `date,asc` / `date,desc` - Event date
- `relevance,desc` - Search relevance
- `distance,asc` - Distance from location
- `venueName,asc` / `venueName,desc` - Venue name
- `onSaleStartDate,asc` / `onSaleStartDate,desc` - Sale date
- `random` - Random order

**Response Example:**
```json
{
  "_embedded": {
    "events": [
      {
        "name": "Taylor Swift | The Eras Tour",
        "type": "event",
        "id": "Z7r9jZ1AdFKdo",
        "url": "https://www.ticketmaster.com/event/Z7r9jZ1AdFKdo",
        "locale": "en-us",
        "images": [
          {
            "ratio": "16_9",
            "url": "https://s1.ticketm.net/dam/a/123/abc-def-123.jpg",
            "width": 1024,
            "height": 576
          }
        ],
        "sales": {
          "public": {
            "startDateTime": "2024-11-15T10:00:00Z",
            "endDateTime": "2024-12-01T02:00:00Z"
          }
        },
        "dates": {
          "start": {
            "localDate": "2024-12-01",
            "localTime": "19:00:00"
          },
          "timezone": "America/Los_Angeles"
        },
        "_embedded": {
          "venues": [
            {
              "name": "SoFi Stadium",
              "type": "venue",
              "id": "KovZpZAEAlaA",
              "city": {
                "name": "Inglewood"
              },
              "state": {
                "name": "California",
                "stateCode": "CA"
              },
              "country": {
                "name": "United States Of America",
                "countryCode": "US"
              },
              "location": {
                "longitude": "-118.33778",
                "latitude": "33.95361"
              }
            }
          ],
          "attractions": [
            {
              "name": "Taylor Swift",
              "type": "attraction",
              "id": "K8vZ917Gku7",
              "classifications": [
                {
                  "primary": true,
                  "segment": {
                    "id": "KZFzniwnSyZfZ7v7nJ",
                    "name": "Music"
                  },
                  "genre": {
                    "id": "KnvZfZ7vAeA",
                    "name": "Pop"
                  }
                }
              ]
            }
          ]
        }
      }
    ]
  },
  "page": {
    "size": 20,
    "totalElements": 1523,
    "totalPages": 77,
    "number": 0
  }
}
```

### 2. Get Event Details

**Endpoint:** `GET /discovery/v2/events/{id}`

Retrieve detailed information about a specific event.

**Example:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/events/Z7r9jZ1AdFKdo.json?apikey=YOUR_KEY'
```

### 3. Get Event Images

**Endpoint:** `GET /discovery/v2/events/{id}/images`

Retrieve all images associated with an event.

**Example:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/events/Z7r9jZ1AdFKdo/images.json?apikey=YOUR_KEY'
```

**Response:**
```json
{
  "type": "event",
  "id": "Z7r9jZ1AdFKdo",
  "images": [
    {
      "ratio": "16_9",
      "url": "https://s1.ticketm.net/dam/a/123/abc-def-123.jpg",
      "width": 2048,
      "height": 1152,
      "fallback": false
    },
    {
      "ratio": "3_2",
      "url": "https://s1.ticketm.net/dam/a/456/def-ghi-456.jpg",
      "width": 1024,
      "height": 683,
      "fallback": false
    }
  ]
}
```

### 4. Search Attractions

**Endpoint:** `GET /discovery/v2/attractions`

Find artists, sports teams, and performers.

**Example:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/attractions.json?keyword=Taylor+Swift&apikey=YOUR_KEY'
```

### 5. Search Venues

**Endpoint:** `GET /discovery/v2/venues`

Search for venues and locations.

**Example:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/venues.json?city=New+York&apikey=YOUR_KEY'
```

### 6. Get Classifications

**Endpoint:** `GET /discovery/v2/classifications`

Browse event categories, genres, and segments.

**Example:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/classifications.json?apikey=YOUR_KEY'
```

**Response Structure:**
```json
{
  "_embedded": {
    "classifications": [
      {
        "segment": {
          "id": "KZFzniwnSyZfZ7v7nJ",
          "name": "Music"
        },
        "_embedded": {
          "genres": [
            {
              "id": "KnvZfZ7vAeA",
              "name": "Pop"
            },
            {
              "id": "KnvZfZ7vAv6",
              "name": "Rock"
            }
          ]
        }
      }
    ]
  }
}
```

### 7. Search Suggestions

**Endpoint:** `GET /discovery/v2/suggest`

Get autocomplete suggestions for event search.

**Example:**
```bash
curl 'https://app.ticketmaster.com/discovery/v2/suggest.json?keyword=swift&apikey=YOUR_KEY'
```

## Common Use Cases

### Use Case 1: Find Events by Location

**Search events in a specific city:**

```javascript
const axios = require('axios');

async function findEventsByCity(city, apiKey) {
  const response = await axios.get(
    'https://app.ticketmaster.com/discovery/v2/events.json',
    {
      params: {
        city: city,
        size: 10,
        apikey: apiKey
      }
    }
  );

  return response.data._embedded.events;
}

// Usage
findEventsByCity('San Francisco', 'YOUR_API_KEY')
  .then(events => {
    events.forEach(event => {
      console.log(`${event.name} - ${event.dates.start.localDate}`);
    });
  });
```

### Use Case 2: Geographic Radius Search

**Find events within a radius:**

```python
import requests

def find_events_nearby(postal_code, radius, api_key):
    """Find events within radius of postal code"""

    url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    params = {
        'postalCode': postal_code,
        'radius': radius,
        'unit': 'miles',  # or 'km'
        'sort': 'distance,asc',
        'apikey': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['_embedded']['events']
    else:
        raise Exception(f"API Error: {response.status_code}")

# Usage
events = find_events_nearby('90210', '25', 'YOUR_API_KEY')

for event in events:
    venue = event['_embedded']['venues'][0]
    print(f"{event['name']} at {venue['name']}")
```

### Use Case 3: Filter by Classification

**Search for specific event types:**

```python
import requests

def search_music_events(genre, city, api_key):
    """Search for music events by genre"""

    params = {
        'classificationName': 'music',
        'genreId': genre,
        'city': city,
        'sort': 'date,asc',
        'apikey': api_key
    }

    response = requests.get(
        'https://app.ticketmaster.com/discovery/v2/events.json',
        params=params
    )

    return response.json()

# Example: Find Pop concerts in Los Angeles
results = search_music_events('KnvZfZ7vAeA', 'Los Angeles', 'YOUR_API_KEY')
```

### Use Case 4: Date Range Search

**Find events in a specific timeframe:**

```javascript
async function findEventsByDateRange(startDate, endDate, apiKey) {
  const params = new URLSearchParams({
    startDateTime: startDate,  // ISO 8601: 2024-12-01T00:00:00Z
    endDateTime: endDate,
    sort: 'date,asc',
    size: 20,
    apikey: apiKey
  });

  const response = await fetch(
    `https://app.ticketmaster.com/discovery/v2/events.json?${params}`
  );

  const data = await response.json();
  return data._embedded.events;
}

// Find events in December 2024
findEventsByDateRange(
  '2024-12-01T00:00:00Z',
  '2024-12-31T23:59:59Z',
  'YOUR_API_KEY'
);
```

### Use Case 5: Event Details with Images

**Get complete event information:**

```python
import requests

class TicketmasterClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://app.ticketmaster.com/discovery/v2'

    def get_event_details(self, event_id):
        """Get detailed event information"""
        url = f'{self.base_url}/events/{event_id}.json'

        response = requests.get(url, params={'apikey': self.api_key})
        return response.json()

    def get_event_images(self, event_id):
        """Get all images for an event"""
        url = f'{self.base_url}/events/{event_id}/images.json'

        response = requests.get(url, params={'apikey': self.api_key})
        return response.json()

    def get_high_res_image(self, event_id):
        """Get highest resolution image"""
        images_data = self.get_event_images(event_id)

        # Find largest image
        largest = max(
            images_data['images'],
            key=lambda img: img['width'] * img['height']
        )

        return largest['url']

# Usage
client = TicketmasterClient('YOUR_API_KEY')
event = client.get_event_details('Z7r9jZ1AdFKdo')
image_url = client.get_high_res_image('Z7r9jZ1AdFKdo')

print(f"Event: {event['name']}")
print(f"Image: {image_url}")
```

## Best Practices

### 1. API Key Security

```python
# ✅ Good: Use environment variables
import os
API_KEY = os.getenv('TICKETMASTER_API_KEY')

# ❌ Bad: Hardcode API key
API_KEY = 'AbCdEfGh123456'
```

### 2. Rate Limit Management

```python
import time
import requests

class RateLimitedClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.requests_this_second = 0
        self.last_request_time = time.time()

    def make_request(self, url, params):
        """Make request with rate limiting"""

        # Wait if we've hit 5 requests this second
        current_time = time.time()

        if current_time - self.last_request_time < 1:
            if self.requests_this_second >= 5:
                time.sleep(1 - (current_time - self.last_request_time))
                self.requests_this_second = 0
                self.last_request_time = time.time()
        else:
            self.requests_this_second = 0
            self.last_request_time = current_time

        params['apikey'] = self.api_key
        response = requests.get(url, params=params)

        self.requests_this_second += 1

        # Check response headers
        if 'Rate-Limit-Available' in response.headers:
            remaining = int(response.headers['Rate-Limit-Available'])
            if remaining < 100:
                print(f"Warning: Only {remaining} requests remaining today")

        return response
```

### 3. Error Handling

```python
def safe_api_call(url, params, api_key):
    """Make API call with comprehensive error handling"""

    params['apikey'] = api_key

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 401:
            raise ValueError("Invalid API key")

        elif response.status_code == 429:
            raise ValueError("Rate limit exceeded")

        elif response.status_code == 404:
            return None  # Resource not found

        else:
            raise Exception(f"API error: {response.status_code}")

    except requests.exceptions.Timeout:
        raise Exception("Request timeout")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
```

### 4. Pagination

```python
def get_all_results(base_url, params, api_key, max_pages=10):
    """Retrieve all results with pagination"""

    all_events = []
    page = 0
    params['apikey'] = api_key

    while page < max_pages:
        params['page'] = page

        response = requests.get(base_url, params=params)
        data = response.json()

        if '_embedded' not in data or 'events' not in data['_embedded']:
            break

        events = data['_embedded']['events']
        all_events.extend(events)

        # Check if there are more pages
        page_info = data['page']
        if page >= page_info['totalPages'] - 1:
            break

        page += 1

    return all_events

# Usage
events = get_all_results(
    'https://app.ticketmaster.com/discovery/v2/events.json',
    {'city': 'Chicago', 'size': 20},
    'YOUR_API_KEY',
    max_pages=5
)
```

### 5. Caching

```python
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=128)
def cached_search(search_params_json):
    """Cache API results to reduce calls"""
    params = json.loads(search_params_json)
    # Make API call
    return fetch_events(params)

# Usage with immutable parameters
params = json.dumps({'city': 'Boston', 'size': 10}, sort_keys=True)
results = cached_search(params)
```

## Advanced Features

### 1. Location-Based Search with Coordinates

```javascript
// Search using latitude/longitude
const params = {
  latlong: '34.0522,-118.2437',  // Los Angeles
  radius: '50',
  unit: 'miles',
  sort: 'distance,asc',
  apikey: API_KEY
};
```

### 2. Negative Filtering

```javascript
// Exclude specific classifications
const params = {
  city: 'New York',
  classificationName: '-sports,-theatre',  // Exclude sports and theatre
  apikey: API_KEY
};
```

### 3. Multi-City Search

```javascript
// Search across multiple cities
const params = {
  city: ['Los Angeles', 'San Francisco', 'San Diego'],
  stateCode: 'CA',
  apikey: API_KEY
};
```

### 4. Source Filtering

```javascript
// Filter by data source
const params = {
  source: 'ticketmaster',  // or 'universe', 'frontgate', 'tmr'
  apikey: API_KEY
};
```

## Response Format

### HAL Format

All responses use HAL (Hypertext Application Language):

```json
{
  "_links": {
    "self": {
      "href": "/discovery/v2/events?page=0&size=20"
    },
    "next": {
      "href": "/discovery/v2/events?page=1&size=20"
    }
  },
  "_embedded": {
    "events": [...]
  },
  "page": {
    "size": 20,
    "totalElements": 500,
    "totalPages": 25,
    "number": 0
  }
}
```

### Image Formats

Images are available in multiple aspect ratios:
- `16_9`: Widescreen (1920×1080, 1024×576, etc.)
- `3_2`: Standard (1024×683, 640×427, etc.)
- `4_3`: Traditional (800×600, 640×480, etc.)

## Troubleshooting

### Issue 1: Invalid API Key

**Error:**
```json
{
  "fault": {
    "faultstring": "Invalid ApiKey"
  }
}
```

**Solutions:**
1. Verify API key in developer portal
2. Check apikey parameter spelling
3. Ensure no extra spaces in key
4. Regenerate API key if needed

### Issue 2: Rate Limit Exceeded

**Error:**
```json
{
  "fault": {
    "faultstring": "Rate limit quota violation"
  }
}
```

**Solutions:**
1. Check `Rate-Limit-Available` header
2. Implement rate limiting in code
3. Cache responses to reduce calls
4. Request higher limits if needed

### Issue 3: No Results Found

**Solutions:**
1. Broaden search criteria
2. Check date ranges
3. Verify location parameters
4. Remove overly restrictive filters
5. Check for typos in keywords

### Issue 4: Pagination Limit

**Error:** No results beyond page 50 with size=20

**Solution:**
```python
# Pagination limit: size × page < 1000
# Use smaller page size to go deeper
params = {
    'size': 10,  # Smaller size allows more pages
    'page': 95,  # Can now go to page 95 (10 × 95 < 1000)
    'apikey': API_KEY
}
```

## Integration Examples

### React Component

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function EventSearch() {
  const [events, setEvents] = useState([]);
  const [city, setCity] = useState('');
  const API_KEY = process.env.REACT_APP_TICKETMASTER_KEY;

  const searchEvents = async () => {
    const response = await axios.get(
      'https://app.ticketmaster.com/discovery/v2/events.json',
      {
        params: {
          city: city,
          size: 10,
          apikey: API_KEY
        }
      }
    );

    setEvents(response.data._embedded?.events || []);
  };

  return (
    <div>
      <input
        type="text"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="Enter city"
      />
      <button onClick={searchEvents}>Search</button>

      <div>
        {events.map(event => (
          <div key={event.id}>
            <h3>{event.name}</h3>
            <p>{event.dates.start.localDate}</p>
            <img src={event.images[0]?.url} alt={event.name} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Node.js Express API

```javascript
const express = require('express');
const axios = require('axios');
const app = express();

const API_KEY = process.env.TICKETMASTER_API_KEY;

app.get('/api/events', async (req, res) => {
  try {
    const { city, keyword, startDate, endDate } = req.query;

    const response = await axios.get(
      'https://app.ticketmaster.com/discovery/v2/events.json',
      {
        params: {
          city,
          keyword,
          startDateTime: startDate,
          endDateTime: endDate,
          sort: 'date,asc',
          apikey: API_KEY
        }
      }
    );

    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

## Resources

### Official Documentation
- **Main Docs**: https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
- **Discovery API**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
- **Developer Portal**: https://developer.ticketmaster.com/
- **API Console**: https://developer.ticketmaster.com/api-explorer/

### API Coverage
- **230K+ Events** across multiple countries
- **Countries**: US, Canada, Mexico, Australia, New Zealand, UK, Ireland, Europe

### Related APIs
- **Commerce API**: Event offers and pricing
- **Partner API**: Advanced transaction capabilities
- **International Discovery**: Region-specific endpoints

### Support
- Developer Forum: https://developer-support.ticketmaster.com/
- Email: developersupport@ticketmaster.com

## Version Information

**Last Updated**: 2025-12-15
**Skill Version**: 1.0.0
**API Version**: Discovery API v2

---

*Note: Always refer to the latest official Ticketmaster documentation for up-to-date information on API changes, new features, and best practices.*
