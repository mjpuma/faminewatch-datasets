# Data licence

**The data in this repository are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).**
Full legal code: https://creativecommons.org/licenses/by/4.0/legalcode

This covers everything in `data/`, `famine_database_v0.2.xlsx` and `famine_database_beta.xlsx`, and the data embedded in `docs/index.html`.
The code (`scripts/` and the explorer page's code in `docs/`) is licensed separately under the MIT License (see `LICENSE`).

Compilation © 2025–2026 Michael J. Puma and S. Chon, Center for Climate Systems Research, Columbia Climate School.

You may share and adapt the data for any purpose, provided you give appropriate credit, link to the licence, and indicate if changes were made. **Appropriate credit means citing this dataset *and* the original source of the records you use**, as listed below.

---

## Third-party data included, and their licences

Several parts of this dataset reproduce or adapt data published by other researchers. We are grateful to them. Their work keeps its own licence and attribution requirements, which apply to anyone reusing those records from this repository.

### 1. European famine years, 1250–1800 — Ljungqvist, Seim & Collet (2024)

> Ljungqvist, F. C., Seim, A., & Collet, D. (2024). Famines in medieval and early modern Europe—Connecting climate and society. *WIREs Climate Change*, 15(1), e859. https://doi.org/10.1002/wcc.859

* **Licence:** CC BY 4.0 (open-access article).
* **What we use:** the regional famine years in Appendix **Table A1** ("Updated list of famine years over the 1250–1800 period modified and expanded from Alfani & Ó Gráda, 2017, 2018"), for nine regions: Italy, Spain, France, Central Europe, the Low Countries, Great Britain, Ireland, the Nordic countries and Russia/Ukraine.
* **Where:** `data/europe_famine_episodes_1250-1800_LjungqvistEtAl2024.csv`, the two `europe_famine_region_year_*` files, the `LJ24-*` rows of `data/faminewatch_events.csv`, and the Europe view of the explorer.
* **This compilation is the work of Ljungqvist, Seim & Collet.** It revises and expands the lists of Alfani & Ó Gráda (2017, 2018) using the regional sources named in the note to Table A1, which are listed for every record in the `regional_sources` column. Please cite Ljungqvist et al. (2024), and those regional sources where relevant, whenever you use these famine years.
* **Changes we made** (as CC BY requires us to state):
  1. Transcribed the table from the published PDF into machine-readable form; the printed values are kept in the `as_printed` column.
  2. Split cells that list separate years with commas (Russia/Ukraine 1279, 1282; 1468, 1472; 1674, 1677) into separate episodes.
  3. Added an `end_year_corrected` column and a `famine_corrected` flag for one probable typesetting error (Italy "1539–49", which overlaps the separate Italy 1544–45 entry; Alfani & Ó Gráda's data give 1539–40). The printed value is unchanged in `end_year` and `famine`.
  4. Derived a region × year presence table (1 = famine recorded) from the episodes.
  No famine years were added to or removed from the published table.

### 2. Global famines, 1846–2011 — Our World in Data

> Hasell, J., & Roser, M. (2017). Famines. *Our World in Data*. https://ourworldindata.org/the-our-world-in-data-dataset-of-famines

* **Licence:** CC BY 4.0 (all data produced by Our World in Data).
* **What we use:** the 77-event "Our World in Data Dataset of Famines" table (years, country, excess-mortality midpoint, lower and upper estimates, and the original source of each estimate).
* **Where:** `data/raw/owid_famines_hasell_roser_2017.csv` (as published) and the corresponding rows of `data/faminewatch_events.csv`.
* **Changes we made:** parsed year ranges into start and end years, assigned macro-regions, and stored the mortality figures as numeric columns. The original source of each estimate is kept with every record.

### 3. India, major drought famines 1344–1900 — Mishra & Aadhar (2021)

> Mishra, V., & Aadhar, S. (2021). Famines and likelihood of consecutive megadroughts in India. *npj Climate and Atmospheric Science*, 4, 59. https://doi.org/10.1038/s41612-021-00219-1

* **Licence:** CC BY 4.0 (open-access article).
* **What we use:** the nine major famines caused by summer-monsoon droughts that the authors identify for 1200–2018.
* **Changes we made:** recorded each as an event with start and end years.

### 4. Korea, famines of 1809–1810 and 1814–1815 — Kim (2025)

> Kim, S. W. (2025). Two severe famines (1809–1810, 1814–1815) in Korea during the last stage of the Little Ice Age. *Climate of the Past*, 21, 1521–1531. https://doi.org/10.5194/cp-21-1521-2025

* **Licence:** CC BY 4.0 (open-access article).
* **What we use:** dates, regions, numbers of starving people and the author's mortality estimates for the two famines.
* **Changes we made:** summarised as two event records.

### 5. Qing China, yearly famine records 1644–1911 — REACHES (NOAA public data archive)

> Lin, K.-H. E., Wang, P. K., Pai, P.-L., Lin, Y.-S., & Wang, C.-W. (2020). Historical droughts in the Qing dynasty (1644–1911) of China. *Climate of the Past*, 16, 911–931. https://doi.org/10.5194/cp-16-911-2020
>
> Data: NOAA/World Data Service for Paleoclimatology, "REACHES Chinese Historical Climate Database Qing Dynasty Drought Series." https://www.ncei.noaa.gov/access/paleo-search/study/29472

* **Licence:** the data come from NOAA's public data archive (World Data Service for Paleoclimatology), which makes them freely available for use with citation of the publication and the online resource; the paper is CC BY 4.0.
* **What we use:** yearly counts of historical records and of sites reporting famine, drought, locusts, crop failure and socio-economic turmoil.
* **Where:** `data/raw/reaches_qing_1644-1911_counts.csv` and the China chart in the explorer.
* **Changes we made:** merged NOAA's *records* and *sites* files into one table. (NOAA's file headers list the per-variable totals of the two files the other way round; the data columns are unchanged.)

---

## Other sources

* **Alfani & Ó Gráda (2017),** *Famine in European History*, Cambridge University Press, Table 1.1: the regional famine years for 1800–1900 (11 records) are cited facts from this table.
* **Walford (1878)** and the chroniclers he quotes are in the public domain.
* All other records cite the published studies or humanitarian reports (e.g., IPC) their facts come from; see `data/references.csv`.
