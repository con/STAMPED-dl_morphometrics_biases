# Poster-derived result targets

## Evidence and scope

The OHBM 2025 poster, “Age dependent volume estimation biases in recon-all clinical and recon-any,” defines the historical claim set to reconstruct. The inspected one-page [PDF](reference/recon_all_recon_any_poster_ohbm2025.pdf) is registered by exact annex key and checksum in [the evidence manifest](evidence-manifest.tsv). Its persistent public source is [OSF DOI 10.17605/OSF.IO/P3KNS](https://doi.org/10.17605/OSF.IO/P3KNS); OSF file version 1 exactly matches the annexed bytes. The OSF node does not declare an explicit licence, so S.2/D.3 remain gaps despite the recorded redistribution authorization.

The objective is scientific reconstruction through newly tracked inputs, exact runtimes, operations, and outputs—not pixel-identical recreation of poster artwork. The source commit audited in [the source inventory](source-inventory.tsv) is current historical source evidence, not a known result-generating commit.

The historical poster labels its version comparison only as “FS7” and “FS8.” FreeSurfer 7.4.1 and 8.2.0 are deliberate reconstruction targets from the conversion plan; 8.2.0 is not asserted to be the unidentified historical FS8 runtime.

## Evidence classes

Every target below has two manifest instances:

- pilot-ds007116--TARGET-ID proves engineering and scientific interfaces on all eligible open ds007116 scans; it is never claim-bearing.
- claim-abcd--TARGET-ID is reserved for the controlled ABCD reconstruction after the release, query, access, and cohort identities are fixed.

PENDING identifies work or evidence not yet produced, UNRESOLVED identifies a missing scientific or technical decision, PLANNED prefixes a declared future path, task, or specification, and NA means intentionally inapplicable with a recorded reason.

No ABCD input, derivative, log, table, statistic, or figure is assumed redistributable. Its eventual availability class must follow the applicable DUC and derivative/publication policy; authorized retrieval does not imply public distribution.

## Reference design

- Historical cohort description: 1,000 unrelated ABCD participants evenly sampled from four waves.
- Reconstruction reference: FreeSurfer 7.4.1 recon-all with high-resolution T1w and T2w.
- Compared tools: recon-all-clinical and recon-any.
- Compared conditions: native T1w and T1w resampled to 1×1×5 mm.
- Global measures: cortical gray-matter volume and cerebellar white-matter volume.
- Regional question: association between age-related bias and published regional age at peak gray-matter volume.
- Version question: FreeSurfer 7.4.1 versus the intended 8.2.0 reconstruction runtime.

The old balanced_scans.csv is historical evidence only. The ABCD campaign must replace it with a tracked cohort operation against an exact permitted release and query.

## Stable target registry

### Global agreement and age residuals

Each age-residual figure combines both declared global measures. Every figure consumes a tracked value table; statistics are independently addressable results.

| Target ID | Artifact | Expected inputs | Expected output |
|---|---|---|---|
| global-racl-native-cort-gmv-agreement-figure | figure | reference and recon-all-clinical native cortical GMV rows | agreement scatter |
| global-racl-native-cort-gmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-racl-native-cereb-wmv-agreement-figure | figure | reference and recon-all-clinical native cerebellar WMV rows | agreement scatter |
| global-racl-native-cereb-wmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-racl-native-age-residual-figure | figure | age plus both native percent-difference measures | age-residual panel |
| global-racl-1x1x5-cort-gmv-agreement-figure | figure | reference and recon-all-clinical 1×1×5 cortical GMV rows | agreement scatter |
| global-racl-1x1x5-cort-gmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-racl-1x1x5-cereb-wmv-agreement-figure | figure | reference and recon-all-clinical 1×1×5 cerebellar WMV rows | agreement scatter |
| global-racl-1x1x5-cereb-wmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-racl-1x1x5-age-residual-figure | figure | age plus both 1×1×5 percent-difference measures | age-residual panel |
| global-rany-native-cort-gmv-agreement-figure | figure | reference and recon-any native cortical GMV rows | agreement scatter |
| global-rany-native-cort-gmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-rany-native-cereb-wmv-agreement-figure | figure | reference and recon-any native cerebellar WMV rows | agreement scatter |
| global-rany-native-cereb-wmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-rany-native-age-residual-figure | figure | age plus both native percent-difference measures | age-residual panel |
| global-rany-1x1x5-cort-gmv-agreement-figure | figure | reference and recon-any 1×1×5 cortical GMV rows | agreement scatter |
| global-rany-1x1x5-cort-gmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-rany-1x1x5-cereb-wmv-agreement-figure | figure | reference and recon-any 1×1×5 cerebellar WMV rows | agreement scatter |
| global-rany-1x1x5-cereb-wmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| global-rany-1x1x5-age-residual-figure | figure | age plus both 1×1×5 percent-difference measures | age-residual panel |
| global-panel-values-table | table | keyed cohort, runtime, condition, age, reference, and compared-tool measures | values and inclusion flags for every global panel |

The poster's approximate cortical/cerebellar R² observations are respectively 0.95/0.98, 0.93/0.97, 0.93/0.97, and 0.87/0.95 for clinical-native, clinical-1×1×5, recon-any-native, and recon-any-1×1×5. They are diagnostics, not acceptance thresholds.

### Regional developmental bias

| Target ID | Artifact | Expected inputs | Expected output |
|---|---|---|---|
| regional-peak-gmv-age-surface-figure | figure | pinned milestone table, atlas mapping, and surface resources | multi-view peak-age surface |
| regional-age-bias-coefficient-surface-figure | figure | declared tool/condition, regional model table, atlas mapping, and surfaces | multi-view coefficient surface |
| regional-peak-age-vs-age-bias-scatter-figure | figure | included rows of the regional values table | peak-age versus coefficient scatter |
| regional-peak-age-vs-age-bias-r-stat | statistic | same included rows and declared correlation method | machine-readable correlation coefficient |
| regional-peak-age-vs-age-bias-p-stat | statistic | same included rows and declared inference method | machine-readable p value |
| regional-analysis-values-table | table | atlas, hemisphere, region, milestone, model, uncertainty, inclusion, and citation records | complete regional analysis table |

The poster reports approximately r = -0.39, p = 0.02; these are diagnostic references. The exact compared tool/condition, atlas, milestone table, model, exclusions, uncertainty, and multiplicity policy remain UNRESOLVED gates.

### FreeSurfer version comparison

| Target ID | Artifact | Expected inputs | Expected output |
|---|---|---|---|
| version-fs741-vs-fs820-cort-gmv-agreement-figure | figure | matched FreeSurfer 7.4.1 and intended 8.2.0 cortical GMV rows | agreement scatter |
| version-fs741-vs-fs820-cort-gmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| version-fs741-vs-fs820-cereb-wmv-agreement-figure | figure | matched FreeSurfer 7.4.1 and intended 8.2.0 cerebellar WMV rows | agreement scatter |
| version-fs741-vs-fs820-cereb-wmv-r2-stat | statistic | same rows and declared R² definition | machine-readable R² |
| version-fs741-vs-fs820-age-residual-figure | figure | age plus both percent-difference measures | combined age-residual panel |

The near-perfect agreement shown on the poster is a diagnostic observation, not a hard-coded conclusion.

### Accounting

| Target ID | Artifact | Expected inputs | Expected output |
|---|---|---|---|
| accounting-cohort-flow-table | table | candidate, inclusion, exclusion, and ordered cohort records | cohort flow by participant/session |
| accounting-campaign-outcomes-table | table | attempt, failure, retry, completion, and acceptance records | campaign outcomes and reasons |
| accounting-input-characteristics-table | table | acquisition, resolution, and availability metadata | exact input characteristics |
| accounting-runtime-identities-table | table | accepted SIF, annex, hash, tool, wrapper, and architecture records | runtime identity table |
| accounting-metric-completeness-table | table | extraction results and expected metric schema | per-case metric completeness |
| accounting-result-row-lineage-table | table | result IDs and exact contributing row identities | rows entering every statistic and figure |

### Scientific derivatives

| Target ID | Artifact | Expected inputs | Expected output |
|---|---|---|---|
| derivative-t1w-1x1x5 | derivative | declared native T1w and qualified resampling operation | independently described 1×1×5 mm T1w derivative with grid and interpolation metadata |
| derivative-reconall-fs741-native | derivative | declared native T1w/T2w and accepted 7.4.1 SIF | independently described reconstruction derivative |
| derivative-reconall-fs820-native | derivative | declared native T1w/T2w and accepted 8.2.0 BIDS App SIF | independently described reconstruction derivative |
| derivative-racl-native | derivative | native T1w and accepted clinical SIF/weights | independently described reconstruction derivative |
| derivative-racl-1x1x5 | derivative | tracked 1×1×5 T1w and accepted clinical SIF/weights | independently described reconstruction derivative |
| derivative-rany-native | derivative | native T1w and accepted recon-any SIF/weights | independently described reconstruction derivative |
| derivative-rany-1x1x5 | derivative | tracked 1×1×5 T1w and accepted recon-any SIF/weights | independently described reconstruction derivative |

## Unresolved scientific specifications

Before a result may become authoritative, resolve and version:

- exact ABCD release/query, unrelatedness rule, wave balance, and age-table identity;
- exact recon-any and recon-all-clinical releases, builds, weights, interfaces, architectures, and terms;
- 1×1×5 resampling software, orientation, grid, interpolation, and anti-aliasing;
- exact source fields for cortical GMV and cerebellar WMV;
- percent-difference sign and denominator, R² definition, model formulas, covariates, exclusions, uncertainty, missingness, and seeds;
- regional tool/condition, atlas, mapping/exclusion rules, and exact milestone resource;
- ds007116 T1w/T2w, age, and metadata eligibility.

Material disagreement with poster observations must be reported and attributed to explicit cohort, input, runtime, or model differences rather than tuned away.
