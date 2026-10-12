# Moon ADM Alpha Vantage Endpoint Entitlement Audit

Date: 2026-10-12  
Status: Documentation review only; no live request performed

## Question

Does the selected `TIME_SERIES_MONTHLY_ADJUSTED` endpoint appear in Alpha Vantage's official documentation as a premium-only endpoint, which could block the planned live contract check with an otherwise valid API key?

## Finding

The official Alpha Vantage API documentation describes `TIME_SERIES_MONTHLY_ADJUSTED` as a monthly adjusted series with last-trading-day-of-month labels and fields including adjusted close and monthly dividend. The endpoint section lists `apikey` as required but does not label this endpoint as premium-only. By contrast, the adjacent `TIME_SERIES_DAILY_ADJUSTED` section explicitly labels that endpoint premium.

This supports retaining the monthly adjusted endpoint for the pilot rather than switching to the daily adjusted endpoint solely due to entitlement assumptions. It does **not** guarantee that every account/key has access, that rate limits will permit all requests, or that the live response will match the expected contract. The live check remains the evidence required for the current key.

## Consequences for the planned live check

- Keep the existing endpoint and request shape unchanged.
- The script makes one request each for VTI, VEU, and SGOV, sequentially, without retries.
- If the provider returns `Note`, `Information`, or `Error Message`, the provider fails closed and the script reports a sanitized failure.
- Do not change endpoint, subscription, retry policy, or provider selection based on this documentation-only review.
- A successful response-shape check does not validate price accuracy, adjustment methodology, publication timing, historical revisions, or ADM suitability.

## Source

Alpha Vantage official API documentation: https://www.alphavantage.co/documentation/  
Relevant sections: `TIME_SERIES_DAILY_ADJUSTED` and `TIME_SERIES_MONTHLY_ADJUSTED`.

## Explicit non-actions

No network call, credential access, provider code change, investment-methodology change, signal assembly, strategy activation, Runtime integration, or persistence change was performed.
