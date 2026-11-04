# Caratteristiche spaziali e degli stati di trattamento nell'adenocarcinoma polmonare EGFR-mutato

## Abstract

### Contesto

La resistenza agli inibitori tirosin-chinasici dell'EGFR può coinvolgere evoluzione molecolare, plasticita cellulare e riorganizzazione spaziale. Un'analisi riproducibile richiede stati di trattamento documentati e pazienti come unita di replicazione.

### Metodi

Abbiamo assemblato risorse pubbliche GEO e cBioPortal relative all'adenocarcinoma polmonare EGFR-mutato. Le coorti principali sono GSE342824, Xenium in situ con sezioni appaiate trattamento-naive/progressive da cinque pazienti, e GSE292469, single-nucleus con metadata TN/MRD/PD. Abbiamo verificato campioni, annotazioni cellulari, mutazioni e qualita. Abbiamo congelato sei firme panel-aware e usato proxy metadata solo quando i conteggi gene-level non erano disponibili. Le analisi sono esplorative.

### Risultati

GSE342824 contiene 1.400.257 cellule annotate, incluse 465.959 cellule marcate come tumorali, in cinque coppie TN/PD. GSE292469 contiene 457.724 nuclei: 28 TN, 14 MRD e 31 PD. I metadata Xenium mostrano una riduzione media di 1,10 nello score alveolare tumorale da TN a PD e un aumento di 0,40 nello score neuroendocrino. I metadata includono mutazioni EGFR, compresa C797S, concentrata in un paziente PD.

### Conclusioni

Le coorti e la pipeline supportano un pilot riproducibile sulla biologia spaziale degli stati di trattamento. Score gene-level, validazione clinica esterna e inferenza terapeutica sono necessari prima di qualsiasi claim clinico.

## Introduzione

L'adenocarcinoma polmonare EGFR-mutato è un modello utile per studiare la resistenza alle terapie mirate. La singola cellula non costituisce un paziente indipendente: l'unita di replicazione e il campione o il paziente.

Questo studio verifica se metadata spaziali e single-nucleus pubblici possano rivelare cambiamenti riproducibili nello stato epiteliale, nel contesto EGFR/MAPK e nella composizione tumorale tra TN, MRD e PD.

Lo studio non e una regola clinica. Un pattern spaziale puo generare un'ipotesi senza dimostrare un santuario farmacologico, predire la recidiva o provare l'efficacia del trattamento.

## Materiali e metodi

### Coorti

- GSE342824: dieci sezioni Xenium da cinque pazienti con LUAD EGFR-mutato, appaiate TN/PD.
- GSE292469: 74 librerie che rappresentano 73 specimen TN/MRD/PD, con annotazioni cliniche e metadata MSK-IMPACT.

GSE301973 e GSE189487 sono stati usati per QC e replicazione biologica. TCGA-LUAD e TRACERx sono contesto molecolare/prognostico, non coorti di efficacia osimertinib-specifica.

### Elaborazione e QC

I metadata sono stati scaricati da NCBI GEO e analizzati con script versionati. I campi cellulari sono stati riassunti a livello di campione e paziente. Il gate strutturale richiedeva cinque coppie Xenium TN/PD complete, tutti e tre gli stati snRNA e localizzazione coerente di C797S.

I report derivati e gli script sono nel repository. I raw GEO di grandi dimensioni non sono inclusi.

### Firme congelate

`resistance-signatures-v1` contiene sei firme: identita epiteliale/tumorale, plasticita basale, plasticita neuroendocrina, resistenza EGFR/MAPK, ipossia/stress e accesso vascolare. Tutti i geni richiesti sono nel pannello Xenium GSE342824. I proxy metadata sono indicati come proxy; senza conteggi gene-level non vengono calcolati score di espressione.

### Statistica

Per Xenium, TN e PD sono stati appaiati per paziente. Le differenze sono PD meno TN, con Wilcoxon esatto e bootstrap a seme fisso come sintesi esplorativa. Per snRNA, i gruppi TN/MRD/PD a livello di campione sono stati riassunti con Kruskal-Wallis. Cellule e nuclei non sono stati trattati come pazienti indipendenti.

## Risultati

### Struttura della coorte

GSE342824 contiene 1.400.257 cellule, di cui 465.959 marcate come tumorali; 917.430 sono TN e 482.827 PD. Cinque pazienti hanno coppie complete.

GSE292469 contiene 457.724 nuclei: 266.448 TN, 60.013 MRD e 131.263 PD. Sono disponibili nove annotazioni cellulari, tra cui tumorale, fibroblastica, endoteliale, mieloide, linfoide, plasmacellulare, epiteliale e mastocitaria. I nuclei tumorali sono 166.112.

### Differenze tra stati

Nell'analisi Xenium appaiata, lo score alveolare tumorale medio diminuisce di 1,10 da TN a PD, mentre lo score neuroendocrino aumenta di 0,40. Questi valori descrivono cinque coppie e non stimano un effetto terapeutico di popolazione.

L'etichetta C797S e concentrata in un paziente PD. Il dato e coerente con un'osservazione associata alla resistenza, ma non dimostra causalita.

I gruppi snRNA sono non appaiati e osservazionali. La frazione endoteliale media e 2,6% in TN e 6,6% in PD, con FDR esplorativo 0,024. La frazione epiteliale e massima in MRD, ma non rimane significativa dopo correzione multipla. Questi risultati possono riflettere campionamento e cellularita.

### Replicazione e benchmark

GSE189487 fornisce sei campioni spaziali indipendenti AIS/MIA/IAC. Le caratteristiche stromali ed epiteliali/EGFR sono rilevabili tra dataset, mentre ipossia e vascolarita sono piu sensibili alla piattaforma. GSE301973 e un singolo caso appaiato usato per QC.

Il baseline TCGA-LUAD include 301 casi completi e 89 eventi DFS. Il Cox penalizzato stima per EGFR HR 1,06 (IC95% 0,61-1,84; p=0,84) dopo aggiustamento per eta, stadio, TP53 e RB1. E un benchmark molecolare, non un'analisi di efficacia osimertinib.

## Discussione

Il contributo principale e un workflow evidence-linked che separa struttura delle coorti, provenienza e interpretazione biologica. Le coorti di resistenza offrono una base piu forte per studiare gli stati di trattamento perché contengono sezioni TN/PD appaiate o metadata TN/MRD/PD espliciti.

Le osservazioni Xenium supportano ulteriori studi sulla plasticita di linea durante la progressione, ma non dimostrano un santuario farmacologico. La concentrazione di C797S in un singolo paziente PD non costituisce un meccanismo generale.

Le firme congelate sono un contratto di riproducibilita: impediscono di sostituire geni non misurati e di chiamare score di espressione semplici metadata.

## Limiti

- La pubblicazione primaria collegata e un preprint bioRxiv.
- La coorte Xenium contiene cinque coppie paziente.
- Gli stati snRNA sono non appaiati e osservazionali.
- I count gene-level non sono inclusi per le dimensioni dei file; alcune firme non sono quindi calcolate numericamente.
- Non esiste un endpoint completo di recidiva osimertinib-specifico collegato alle misure spaziali.
- Batch, qualita tissutale, dettagli terapeutici e confondimento clinico richiedono ulteriori analisi.
- I risultati non supportano raccomandazioni terapeutiche o predizioni di rischio individuale.

## Figure

![Metadata Xenium TN/PD appaiati.](xenium_paired_resistance_metadata.png)

![Metadata snRNA e QC per stato.](snrna_state_metadata_qc.png)

## Disponibilita di dati e codice

Codice, report derivati, test, figure e materiali sono archiviati in:

- GitHub: https://github.com/Lukecele/spatial-continuum-translational
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.23956445

Il repository originale spatial-continuum-oncology e conservato separatamente e non e stato modificato.

## Riferimenti principali

1. PMID 40654861. *Complementary modes of resistance to EGFR TKI in lung adenocarcinoma through MAPK activation and cellular plasticity.* bioRxiv, 2025.
2. PMID 36434043. *Delineating the dynamic evolution from preneoplasia to invasive lung adenocarcinoma by integrating single-cell RNA sequencing and spatial transcriptomics.* Experimental & Molecular Medicine, 2022.
3. PMID 41152910. *IFITM3-MET interaction drives osimertinib resistance through AKT pathway activation in EGFR-mutant non-small cell lung cancer.* Molecular Cancer, 2025.
4. PMID 28445112. *Tracking the Evolution of Non-Small-Cell Lung Cancer.* The New England Journal of Medicine, 2017.
5. PMID 28445469. *Phylogenetic ctDNA analysis depicts early-stage lung cancer evolution.* Nature, 2017.
