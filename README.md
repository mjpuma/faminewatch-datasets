<p align="center"><img src="assets/faminewatch-datasets-logo.png" width="700" alt="FamineWatch Datasets logo showing a wheat stalk, global network and historical time-series" /></p>

# FamineWatch Datasets (v0.2, beta)

A curated, citable compilation of documented famines and severe food-system disruptions, from historical literature and humanitarian assessments, **plus the regional famine-year chronology for medieval and early modern Europe (1250–1800)** used in recent climate–famine research, and **openly licensed famine datasets for other world regions** (global 1846–2011, India, Korea, Japan, Qing China).

## Licence

**Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** · **Code: MIT.** See [`LICENSE-DATA.md`](LICENSE-DATA.md) for full terms and attributions.

This dataset includes records from the following openly licensed sources. Each keeps its own licence and must be credited when you reuse its records:

| Source | What it contributes | Licence |
|---|---|---|
| **Ljungqvist, Seim & Collet (2024)**, *WIREs Climate Change* 15(1): e859, [doi:10.1002/wcc.859](https://doi.org/10.1002/wcc.859) | European regional famine years, 1250–1800 (Table A1), revised and expanded from Alfani & Ó Gráda (2017, 2018) | **CC BY 4.0** |
| **Hasell & Roser (2017)**, *Our World in Data*, ["Famines"](https://ourworldindata.org/the-our-world-in-data-dataset-of-famines) | Global famines with excess mortality, 1846–2011 | **CC BY 4.0** |
| **Mishra & Aadhar (2021)**, *npj Climate and Atmospheric Science* 4: 59, [doi:10.1038/s41612-021-00219-1](https://doi.org/10.1038/s41612-021-00219-1) | India, major drought famines 1344–1900 | **CC BY 4.0** |
| **Kim (2025)**, *Climate of the Past* 21: 1521–1531, [doi:10.5194/cp-21-1521-2025](https://doi.org/10.5194/cp-21-1521-2025) | Korea, famines of 1809–10 and 1814–15 | **CC BY 4.0** |
| **Lin et al. (2020)**, *Climate of the Past* 16: 911–931; REACHES data from **NOAA's public data archive** ([World Data Service for Paleoclimatology](https://www.ncei.noaa.gov/access/paleo-search/study/29472)) | Qing China, yearly famine-record counts 1644–1911 | NOAA public data (cite publication and online resource); paper CC BY 4.0 |

The changes we made to each source (transcription, splitting multi-year cells, one flagged correction kept alongside the printed value) are listed in `LICENSE-DATA.md`.

**Explore it in your browser:** open [`docs/index.html`](docs/index.html) (or the GitHub Pages site once Pages is enabled for the `/docs` folder). The explorer has an interactive region × year famine heatmap for Europe, a global timeline, a searchable/filterable table with CSV/JSON download of any filtered subset, and the full source list and change log.

---

## What's in the repository

| File | Contents |
|---|---|
| `data/faminewatch_events.csv` / `.json` | **All records** (629): the beta compilation (379 after removing 2), v0.2 additions (3), the European regional famine episodes 1250–1800 (236), and Alfani & Ó Gráda's 1800–1900 regional entries (11). One row per event. |
| `data/europe_famine_episodes_1250-1800_LjungqvistEtAl2024.csv` | European famine episodes by region (236), as printed in Ljungqvist et al. (2024), Table A1, with regional sources and notes. |
| `data/europe_famine_region_year_1250-1800_LjungqvistEtAl2024.csv` | The same chronology as a long region × year table (9 regions × 551 years; `famine` = 1/0 as printed; `famine_corrected` applies the Italy 1539–40 fix). |
| `data/europe_famine_episodes_1800-1900_AlfaniOGrada2017_Table1-1.csv` | 19th-century regional famine years from Alfani & Ó Gráda (2017), Table 1.1 (major multi-region famines only). |
| `data/europe_famine_region_year_wide_1250-1800_LjungqvistEtAl2024.csv` | Wide year × region 0/1 matrix — ready for time-series analysis. |
| `data/raw/owid_famines_hasell_roser_2017.csv` | Our World in Data famine dataset (77 famines, 1846–2011, with low/mid/high excess-mortality estimates), as published. |
| `data/raw/reaches_qing_1644-1911_counts.csv` | Qing China (1644–1911): yearly counts of historical records and sites reporting famine, drought, locusts, crop failure and unrest (REACHES; Lin et al. 2020). |
| `data/references.csv` | Full citations (corrected beta reference list + v0.2 sources). |
| `data/changelog_v0.2.csv` | Every correction applied in v0.2 (old → new value, reason) and every item flagged for review. |
| `famine_database_v0.2.xlsx` | All of the above as one workbook. |
| `famine_database_beta.xlsx` | The original beta workbook, kept unchanged for provenance. |
| `docs/index.html` | Self-contained interactive explorer (no server or install needed). |
| `scripts/` | `build.py` regenerates every file above from the beta workbook and `data/raw/`; `make_xlsx.py` builds the workbook. |

### Event table columns (`faminewatch_events.csv`)

| Column | Description |
|---|---|
| `event_id` | Stable ID. `FW-####` for compilation records (numbered chronologically); `LJ24-<region>-<start>` for European episodes. |
| `source_dataset` | Which compilation the record comes from. |
| `start_year`, `end_year` | Integer years; negative = BCE. |
| `year_label` | Period as written in the source. |
| `area` | Place as reported (country, province, city, or multi-region). |
| `macro_region` | Europe; South Asia; East Asia; Southeast Asia; Middle East & North Africa; Sub-Saharan Africa; Americas; Oceania; Multi-region / global. |
| `event_type` | Famine / food crisis · Famine (regional famine years) · Volcanic eruption (climate forcing) · Production shock (drought) · Climate anomaly. |
| `primary_cause`, `environmental_category` | Drivers as recorded in the beta compilation. |
| `description` | Impacts: mortality, crop losses, prices, displacement, quoted historical reports. |
| `references` | Short-form citations (full forms in `references.csv`). |
| `verification_status` | `as compiled (beta); not yet re-verified` · `corrected in v0.2` · `flagged for review` · `transcribed from published table (v0.2)` · `added in v0.2 (source-checked)`. |
| `qc_notes` | What was changed or why a record is flagged. |

---

## European famine chronology, 1250–1800

The European records are the regional famine-year list of **Ljungqvist, Seim & Collet (2024)**, Appendix Table A1, which revises and expands the lists of **Alfani & Ó Gráda (2017, 2018)**. Nine regions: Italy, Spain, France, Central Europe, the Low Countries, Great Britain, Ireland, the Nordic countries, and Russia/Ukraine.

* The list records **only the presence of famine conditions** in a region in a given year. It says nothing about severity or geographic extent within the region; for most pre-19th-century famines that information does not exist.
* Regional sources used by Ljungqvist et al. to revise each region are listed per episode (`regional_sources`) and in `references.csv`. Please cite them along with the chronology.
* The article is open access under CC BY 4.0; the table is redistributed here with attribution.

**Transcription and checks.** Table A1 was extracted from the published PDF using text positions. Checks: (1) the extracted sequence of 1,507 characters of year values matches the PDF text exactly; (2) Central Europe has 22 famine periods in 1500–1800, matching the count reported by Esmaili et al. (preprint); (3) years with famine in ≥ 4 regions match Ljungqvist et al.'s Table A2, apart from three discrepancies that are internal to the published tables (see below).

**Known issues in the published table (kept as printed, flagged):**
* Italy `1539–49` overlaps the separate Italy `1544–45` entry and is almost certainly a typesetting error for `1539–40`: the Alfani & Ó Gráda (2018) replication data code Italian famine years as 1539–1540. `end_year` keeps the printed value; `end_year_corrected` and `famine_corrected` apply the fix (636 → 629 region-years). Treated as printed, the 1500–1800 total is 161 regional episodes; merging the overlap gives 160.
* Table A2 (years with famine in ≥ 4 regions) lists 1556 (Table A1 gives only 3 regions that year) and omits 1629 and 1630 (Table A1 gives 4 regions each).
* Comma-separated years in one cell (Russia/Ukraine `1279, 1282`; `1468, 1472`; `1674, 1677`) are split into separate episodes.

---

## Other famine datasets added in v0.2

Only sources whose licence allows redistribution, or individual dated facts cited to a published study, are included.

| Source | Coverage | Records | Licence |
|---|---|---|---|
| Hasell & Roser (2017), *Our World in Data* famine dataset | Global, 1846–2011; excess mortality (low/mid/high) | 77 events | CC BY 4.0 |
| Mishra & Aadhar (2021), *npj Climate and Atmospheric Science* 4:59 | India, major drought famines 1344–1900 | 9 events | CC BY 4.0 |
| Kim (2025), *Climate of the Past* 21:1521–1531 | Korea, famines of 1809–10 and 1814–15, with mortality estimates | 2 events | CC BY 4.0 |
| Bassino (2007); Nakatsuka (PAGES Magazine) | Japan: Kanshō (1459–60), Kyōhō (1731–33), Tenmei (1783–86), Tenpō (1833–38) famines | 4 events | dated facts with citation |
| Lin et al. (2020), REACHES via NOAA/WDS Paleoclimatology | Qing China 1644–1911, yearly famine-record counts (index, not events) | 268 years | CC BY 4.0 paper; NOAA open data |

Note on REACHES: the per-variable "Total number" lines in NOAA's file headers are swapped between the *records* and *sites* files. The data columns themselves are consistent (records ≥ sites every year, and the column sums match the totals printed in the other file).

**Not included, and why:**
* **World Peace Foundation Historic Famines dataset** (1870–present, the most comprehensive modern catalogue): the files carry an "all rights reserved" notice and no reuse licence. Worth asking WPF (worldpeacefoundation@tufts.edu) for permission.
* **EM-DAT** (drought and famine disasters): its terms do not allow redistribution.
* **Saito (2010) chronology of Japanese famines** (281 famines, 6th–19th c.): published in a book that prohibits reproduction without the authors' permission.
* **Chosŏn (Korea) famine series** from the *Veritable Records* (e.g., the 1670–71 Kyŏngsin and 1695–96 Ŭlbyŏng famines): published studies were not yet checked for licence and figures.
* **Africa before 1860**: chronologies (Pankhurst for Ethiopia; Nicholson's documentary database for the continent) are not available as open event lists; Nicholson's data are on NOAA/WDS and could be added as an index.

## Corrections and flags in v0.2

Selected corrections (all in `changelog_v0.2.csv`):

* **Somalia 2010–12:** excess mortality was **258,000** (244,000–273,000), Oct 2010–Apr 2012 (Checchi & Robinson 2013); the beta had 0.285 million.
* **43 BCE eruption:** now attributed to **Okmok II (Alaska)**, early 43 BCE (McConnell et al. 2020), not Etna.
* **Eldgjá:** began in **939 CE** and continued to at least 940 (Oppenheimer et al. 2018), not 934.
* **Tarawera:** erupted on 10 June **1886**, not 1885.
* "Puma et al. (in press)" → **Puma, Chon & Wada (2015)**, *PAGES Magazine* 23(2), 66–67.
* Book titles on the Chinese famine were swapped (*Tombstone* is Yang 2012; *Mao's Great Famine* is Dikötter 2010); Robock (2000) and Jordan (1996) citations reconciled; encoding errors in the reference list fixed; a stray text fragment removed from the 1813 Poland entry; assorted typos.

* **Soviet famine 1931–33:** beta excess mortality (1.2 million) replaced: at least 5 million famine deaths across the USSR in 1931–34, including ~3.9 million excess deaths in Ukraine (~13% of its population); published range 5.5–10.8 million (Ó Gráda 2009; Applebaum 2017; HURI MAPA; Markevich, Naumenko & Qian 2021).
* **Yemen:** restated on the IPC scale. No area was classified in Famine; in Dec 2018–Jan 2019 ~63,500 people were in IPC Phase 5 (Catastrophe), 238,000 without humanitarian food assistance (IPC 2018).
* **Dates:** Ethiopia 1983–85 (with the higher ~0.8 million estimate from the World Peace Foundation added); North Korea 1995–98; Henan 1942–43.
* **1450s eruption:** no longer attributed to Kuwae. Ice cores show a Northern Hemisphere eruption in 1452/53 and a Southern Hemisphere eruption in 1457/58, and the 1458/59 glass is chemically distinct from Kuwae (Sigl et al. 2015; Hartman et al. 2019; Abbott et al. 2021).
* **Agung 1963:** VEI 5 (Smithsonian GVP).
* **Walford entries:** the duplicate 1586 England row and the "twenty-three years' famine" of 1286–1308 were removed (both modern chronologies rule out a continuous famine, and Walford's individual dearth years in that span remain). Walford's 1594 quotation about the siege of Paris was moved to its own 1590 Paris entry; the 1594 England/Hungary famine stays.
* Dando (2012) added to the reference list.

Still flagged: the source of the 536 CE eruption remains unidentified.

**v0.2 additions:** Sudan 2024–present (IPC Famine Review Committee confirmed Famine in Zamzam camp, Aug 2024, and in El Fasher and Kadugli, Sep 2025 analysis) and the Gaza Strip 2025 (IPC FRC confirmed Famine in Gaza Governorate, Aug 2025).

**Cross-check data:** the Alfani & Ó Gráda (2018) replication dataset (openICPSR, doi:10.3886/E120551V1; Italy, France and England famine indicators, 1290–1901) was used to check the Italy 1539–40 correction and the Walford 1286–1308 entry. It is not redistributed here.

## Known gaps (next steps)

* Walford (1878) Table 1 entries for **1832–1878** have not yet been transcribed.
* Alfani & Ó Gráda (2017) chapter-level regional chronologies (e.g., Table 8.1 Ireland, 9.1 Nordic) would add single-region 19th-century famines beyond Table 1.1.
* Mortality figures are stored as text; numeric excess-mortality fields with low/high bounds would make the data easier to analyse.
* Severity and extent are absent for most records; IPC phase classifications could be added for post-2004 crises.

## Status and use

This is a **select compilation**, not an exhaustive global list. It is intended for **research, teaching, and method development** and **should not be used for operational early warning** without contextual validation.

## Citation

> Puma, M. J., & Chon, S. (2026). *FamineWatch Datasets: Compilation of Select Famines and Food Disruptions Around the World* (v0.2, beta). Center for Climate Systems Research, Columbia Climate School, Columbia University at NASA Goddard Institute for Space Studies. https://github.com/mjpuma/faminewatch-datasets

When using the European famine years, **please also cite Ljungqvist et al. (2024)**, whose Table A1 is the source of these records, and the works it builds on:

> Ljungqvist, F. C., Seim, A., & Collet, D. (2024). Famines in medieval and early modern Europe—Connecting climate and society. *WIREs Climate Change*, 15(1), e859. https://doi.org/10.1002/wcc.859
>
> Alfani, G., & Ó Gráda, C. (Eds.) (2017). *Famine in European History*. Cambridge University Press. https://doi.org/10.1017/9781316841235
>
> Alfani, G., & Ó Gráda, C. (2018). The timing and causes of famines in Europe. *Nature Sustainability*, 1, 283–288. https://doi.org/10.1038/s41893-018-0078-0

See also: Esmaili, E., Puma, M. J., Ludlow, F., et al. *El Niño amplified food insecurity in early modern Europe* (uses this chronology). Preprint: https://doi.org/10.21203/rs.3.rs-7812038/v1

## Contact

Contributions, corrections, and archival additions are welcome — open an issue or email **mjp38@columbia.edu**.
