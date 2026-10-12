# Kubernetes display-query performance

Measured 2026-10-11/12 on Windows amd64, Go 1.26.5, Intel Xeon (Skylake, IBRS),
GOMAXPROCS=16. These are local fake-client/HTTP-handler measurements, not live
Kubernetes API-server, etcd, network, or production-memory measurements.

## Reproduce

From `control_panel/backend`:

```powershell
go test ./internal/api -run '^TestKubernetesDisplayListingFixture$' -count=1 -v
go test ./internal/api -run '^$' -bench '^BenchmarkKubernetesDisplayListing$' -benchmem -benchtime=3x -count=3
```

The fixture matrix contains 1,000/10,000 Pods, PVCs and PVs, 10/100 namespaces,
100 Workers with inventory snapshots, and 10 Services per namespace. Half of
Pods are Notebooks with bound NFS claims; the other half are ordinary Pods with
non-NFS claims. Every namespace contains both groups. Service fixtures cover
managed/unmanaged, notebook-only, ordinary-only, mixed selectors and no matches.

Benchmarks exercise authenticated HTTP GET endpoints for NFS hosts, Notebook
Pods and Services. Setup, token generation, request construction, fake action
history clearing, response decoding and correctness assertions are outside the
timer. Allocation metrics cover the timed handler/fake-client execution. Fake
action history is cleared every iteration, preventing accumulation from
artificially increasing benchmark memory. Each sample uses three requests;
three samples are a small local baseline, not a percentile/SLO measurement.

The integrity test verifies result counts and matching states, excludes ordinary
Pods from Notebook responses, verifies managed/deletable flags including mixed
selectors, and separately verifies the existing eight-call Service-list
concurrency limit. It uses no real worker, Kubernetes cluster or development DB.

## Measurements after request-local optimization

Ranges are min/max across three samples. MB means decimal bytes allocated per
operation (`B/op / 1,000,000`), not retained heap, peak RSS or transferred bytes.

| Total Pods/PVCs/PVs | Namespaces | Endpoint | ms/request | Allocated MB/request | API list calls/request |
|---:|---:|---|---:|---:|---:|
| 1,000 | 10 | NFS hosts | 20.73–22.78 | 12.625 | 3 |
| 1,000 | 10 | Notebook Pods | 19.51–23.27 | 12.981–13.331 | 3 |
| 1,000 | 10 | Services | 10.95–12.97 | 9.041–9.214 | 11 |
| 1,000 | 100 | NFS hosts | 20.53–24.66 | 12.450–12.625 | 3 |
| 1,000 | 100 | Notebook Pods | 21.85–25.19 | 13.330–13.332 | 3 |
| 1,000 | 100 | Services | 22.41–26.54 | 13.201–13.219 | 101 |
| 10,000 | 10 | NFS hosts | 216.94–231.85 | 119.648 | 3 |
| 10,000 | 10 | Notebook Pods | 235.37–259.07 | 129.868–129.870 | 3 |
| 10,000 | 10 | Services | 115.22–128.01 | 92.973–92.974 | 11 |
| 10,000 | 100 | NFS hosts | 227.58–244.50 | 119.648–119.649 | 3 |
| 10,000 | 100 | Notebook Pods | 264.74–277.04 | 129.867–129.868 | 3 |
| 10,000 | 100 | Services | 119.58–121.42 | 91.089–91.090 | 101 |

At 10,000 objects, the unoptimized baseline allocated about 125.00 MB per NFS
host request and 135.11–135.13 MB per Notebook Pod request. The optimized version
allocates about 119.65 MB and 129.87 MB respectively: about 5.35 MB (4.3%) and
5.25 MB (3.9%) less. Service allocation is unchanged as a control; no Service
production logic was modified by this optimization.

No latency improvement is claimed. The later run was slower across both the
changed mount endpoints and the unchanged Service control. These runs occurred
at different times and were not a controlled statistical comparison. The
baseline mount requests were about 0.19–0.22 seconds at 10,000 objects; the later
run was about 0.22–0.28 seconds. Response sizes can differ slightly between
fixtures because collected-at timestamps use current fractional precision;
response fields, relationship counts and safety flags are asserted separately.

## Changes and preserved behavior

1. The request-local PVC/PV lookup maps now retain only claims referenced by
   selected Notebook Pods and volumes bound to those claims, instead of copying
   unrelated PVC/PV objects into additional large maps. Namespaces are part of
   the key. Shared/duplicate references, pending claims, missing claims and
   missing PV states keep their existing semantics.
2. The NFS-host response reuses the inventory snapshot already parsed for mount
   associations, rather than unmarshalling every snapshot twice in one request.
   This is request-local reuse, not a persistent cache.
3. The old refresh test's router now injects its test collector explicitly. The
   unavailable-queue tests still require HTTP 503; production behavior was not
   weakened to obtain a passing suite.

The endpoints still perform fresh request-time display queries: one full Pods,
PVCs and PVs list each for mount associations, and one full Pods list plus a
namespaced Service list per Notebook namespace for Services. Display list
requests use ResourceVersion=0, as before. Counts remain 3 or 1+N respectively.
The eight-way Service fan-out remains bounded. The full-cluster reads and
namespace-dependent Service request count are measured costs that remain, not
costs this change claims to eliminate.

Separate deletion/reclamation checks retain their fresh reads, protected paths,
UID/resource-version checks and fail-closed unknown-source behavior. No
cross-request Kubernetes cache was introduced or used as deletion evidence.

## Deployment validation still required

Before applying a production latency target, measure these endpoints in an
owner-authorized staging cluster at the actual Pod/PVC/PV/namespace counts.
Record API-server list latency, payload sizes, request concurrency, p50/p95,
process heap/RSS and cluster/API-server load separately. The local fake deep
copies and response encoding do not reproduce network, watch-cache or etcd
behavior. An informer cache or namespace discovery policy is a separate design,
not justified solely by this local benchmark.

See [remaining risk decisions and exposure review](2026-10-11-remaining-risk-decisions.md)
for the accepted shared-identity/cross-namespace boundaries and secret-scan scope.
