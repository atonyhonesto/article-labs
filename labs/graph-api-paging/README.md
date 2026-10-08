<sub>[← all labs](../../README.md)</sub>

# Reading huge SharePoint lists through Microsoft Graph

> 25,000 items is 5× the list view threshold. Index, filter, page, back off and then only ask for what changed.

`Python` · `stdlib`

**Companion to:**
- [Managing Huge Data Sets in SharePoint Online](https://www.linkedin.com/pulse/managing-huge-data-sets-sharepoint-online-tony-honesto-nazyc/)
- [SharePoint — More Than Just File Storage](https://www.linkedin.com/pulse/sharepoint-more-than-just-file-storage-tony-honesto-p2eic/)

## What it shows

- An unfiltered query over the 5,000-item threshold fails, as it does in SharePoint Online.
- Filtering on an indexed column and following `@odata.nextLink` page by page.
- Honouring HTTP 429 `Retry-After` instead of hammering the service.
- Delta queries: the next sync returns only changed items via `@odata.deltaLink`.

## Run it

```bash
bash labs/graph-api-paging/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Unfiltered query on 25,000 items -> Graph error 400: listViewThreshold
Filtered on an indexed column: 20,000 items in 24 calls, 3 throttles honoured (waited 6 s)
Next sync via delta query: 3 changed items instead of 25,000
```

## What's in here

| File | Purpose |
|---|---|
| `graph.py` | Fake Graph endpoint, retry, paging and delta client |
| `demo.py` | Threshold error, full read, then delta sync |
| `tests/` | Paging, throttling and delta tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| FakeGraph | `https://graph.microsoft.com/v1.0/sites/{id}/lists/{id}/items` with MSAL auth |
| Injected sleep | Real waits, plus `$top` and `$select` to keep pages small |
| Delta token in memory | Delta link persisted between runs |
